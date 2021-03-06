from PyQt4 import QtGui, QtCore
import sys
from gui import gui
import lib.diff_match_patch as DMP
from socket import AF_INET, SOCK_STREAM, socket
from socket import error as socketError
import threading
import Queue
import re

lorem = reduce(lambda x, y: x+y, open('lorem', 'r').readlines())


class GuiApp(QtGui.QMainWindow, gui.Ui_MainWindow):

	def __init__(self, parent=None):
		super(GuiApp, self).__init__(parent)
		self.setupUi(self)

		# init text
		self.textEdit_2.setReadOnly(True)
		self.textEdit.setText(lorem)
		self.currentText = str(self.textEdit.toPlainText())

		# connect methods
		self.textEdit.textChanged.connect(self.textChangeMethod)
		self.newPushButton.clicked.connect(self.newDocumentMethod)
		self.remotePushButton.clicked.connect(self.remoteDocumentMethod)

		self.dmp = DMP.diff_match_patch()

		self.tcpSocket = socket(AF_INET, SOCK_STREAM)

		self.sendQueue = Queue.Queue()

		# Set up signals
		self.connect(self, QtCore.SIGNAL('updateStatus'),
		             self.statusUpdateMethod)

		self.connect(self, QtCore.SIGNAL('updateText'),
		             self.textUpdateMethod)

		self.connect(self, QtCore.SIGNAL('replaceText'),
		             self.replaceTextMethod)

		self.connections = list()

		self.isMaster = False
		self.lastDiffID = ''

	def replaceTextMethod(self, text):
		# save cursor and scrollbar location
		cursor = self.textEdit.textCursor()
		cursorPos = cursor.position()
		scrollPos = self.textEdit.verticalScrollBar().value()

		# resync text
		self.textEdit.blockSignals(True)
		self.textEdit.setText(text)
		self.textEdit.blockSignals(False)

		# restore cursor and scrollbar
		cursor.setPosition(cursorPos)
		self.textEdit.verticalScrollBar().setValue(scrollPos)
		self.textEdit.setTextCursor(cursor)
		return

	def textUpdateMethod(self, patchText):
		# save cursor and scrollbar location
		cursor = self.textEdit.textCursor()
		cursorPos = cursor.position()
		scrollPos = self.textEdit.verticalScrollBar().value()

		# apply patch to text
		patch = self.dmp.patch_fromText(patchText)
		try:
			addLoc = int(patchText.split(' ')[2].split(',')[0])
		except:
			print 'patchtext error: \n', patchText
			self.sendQueue.put(('RESYNC', 'help!'))
			self.emit(QtCore.SIGNAL('updateStatus'),
			          'error %s' % patchText)
			return

		oldText = str(self.textEdit.toPlainText())
		newText, result = self.dmp.patch_apply(patch, oldText)
		cursorDelta = len(newText) - len(oldText)

		if False in result:
			if self.isMaster:
				text = str(self.textEdit.toPlainText())
				self.sendQueue.put(('FULLTEXT', text))
			else:
				self.sendQueue.put(('RESYNC', 'help!'))
				self.emit(QtCore.SIGNAL('updateStatus'),
				          'error %s' % str(result))

		if not self.isMaster:
			self.textEdit.blockSignals(True)
			self.textEdit.setText(newText)
			self.textEdit.blockSignals(False)
		else:
			self.textEdit.setText(newText)

		# restore cursor and scrollbar
		if addLoc < cursorPos and (cursorPos + cursorDelta) > 0:
			cursor.setPosition(cursorPos + cursorDelta)
		else:
			cursor.setPosition(cursorPos)
		self.textEdit.verticalScrollBar().setValue(scrollPos)
		self.textEdit.setTextCursor(cursor)

		return

	def statusUpdateMethod(self, text):
		self.textEdit_2.append(text)
		return

	def newDocumentMethod(self):
		addr = self.addressLineEdit.text()
		if len(addr) == len('000.000.000.000'):
			port = self.portSpinBox.value()
			self.tcpSocket.bind((addr, port))
			thread = threading.Thread(target=self.connectionManagerThread)
			thread.start()
			sendThread = threading.Thread(target=self.serverThread)
			sendThread.start()
			self.statusLabel.setText('Master Document')
			self.newPushButton.setDisabled(True)
			self.isMaster = True
		return

	def remoteDocumentMethod(self):
		addr = self.addressLineEdit.text()
		if len(addr) == len('000.000.000.000'):
			port = self.portSpinBox.value()
			self.tcpSocket.connect((addr, port))
			self.textEdit_2.append('Connected to %s:%d' % (addr, port))
			thread = threading.Thread(target=self.sendThread)
			thread.start()
			connectThread = threading.Thread(target=self.connectionThread,
			                                args=(self.tcpSocket, ''))
			connectThread.start()
			self.remotePushButton.setDisabled(True)
			self.statusLabel.setText('Slave Document')
			self.sendQueue.put(('RESYNC', 'help!'))
		return

	def textChangeMethod(self):
		oldText = self.currentText
		diffText = str(self.textEdit.toPlainText())

		# find diffs
		diffs = self.dmp.diff_main(oldText, diffText)
		# compile patches
		patch = self.dmp.patch_make(oldText, diffText, diffs)
		# create text from patches
		self.sendQueue.put(('DIFF', self.dmp.patch_toText(patch)))

		self.currentText = diffText
		return

	def connectionManagerThread(self):
		while True:
			self.emit(QtCore.SIGNAL('updateStatus'), 'Socket is listening on %s:%d' % self.tcpSocket.getsockname())
			self.tcpSocket.listen(5)
			client_socket, client_addr = self.tcpSocket.accept()
			connectThread = threading.Thread(target=self.connectionThread,
			                                args=(client_socket, client_addr))
			connectThread.start()
			self.connections.append(client_socket)

		return

	def serverThread(self):
		try:
			while True:
				command, data = self.sendQueue.get()
				for connection in self.connections:
					if self.lastDiffID == '%s:%d' % connection.getpeername():
						self.lastDiffID = ''
					else:
						self.emit(QtCore.SIGNAL('updateStatus'),
						          "sending ServerThread :\n%s\n%s" % (command, data[:10] + '...' + data[-10:]))
						connection.sendall(command + ';' + '%s:%d' % self.tcpSocket.getsockname() + ';' + data)
		except socketError, d:
			print socketError, d
		return

	def connectionThread(self, client_socket, client_addr):
		self.emit(QtCore.SIGNAL('updateStatus'), 'Client %s connected to %s:%d' % ((client_addr,) + client_socket.getsockname()))
		try:
			while True:
				data = ''
				while True:
					buf = client_socket.recv(4096)
					data += buf
					if len(buf) < 4096:
						break
				protocolPattern = r'([^;]+)\;([^;]+)\;(.*)'
				match = re.match(protocolPattern, data, flags=re.S)
				if match:
					command, info, value = match.groups()
					self.emit(QtCore.SIGNAL('updateStatus'),
					          "received %s from %s: \n(%s)" % (command, info, data[:10]+'[...]'+data[-10:]))
					if command == 'DIFF':
						self.lastDiffID = info
						self.emit(QtCore.SIGNAL('updateText'), value)
					elif command == 'RESYNC':
						text = str(self.textEdit.toPlainText())
						self.sendQueue.put(('FULLTEXT', text))
					elif command == 'FULLTEXT':
						self.emit(QtCore.SIGNAL('replaceText'), value)
					else:
						self.emit(QtCore.SIGNAL('updateStatus'), 'commanderror :\n%s' % (data))
		except socketError, d:
			self.connections.remove(client_socket)
			print socketError, d
		return

	def sendThread(self):
		try:
			while True:
				command, data = self.sendQueue.get()
				self.emit(QtCore.SIGNAL('updateStatus'), "sending Send Thread:\n%s" % data)
				self.tcpSocket.sendall(command + ';' '%s:%d' % self.tcpSocket.getsockname() + ';' + data)
		except socketError, d:
			print socketError, d
		return


def main():
	app = QtGui.QApplication(sys.argv)
	form = GuiApp()
	form.show()
	app.exec_()

main()