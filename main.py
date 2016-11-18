from PyQt4 import QtGui, QtCore
import sys
from gui import gui
import lib.diff_match_patch as DMP
from socket import AF_INET, SOCK_STREAM, socket
from socket import error as socketError
import threading
import Queue

textA = "the cat in the red hat"
textB = "the feline in the blue hat"

lorem = reduce(lambda x, y: x+y, open('lorem', 'r').readlines())


class GuiApp(QtGui.QMainWindow, gui.Ui_MainWindow):
	# Custom signals
	updateSignal = QtCore.pyqtSignal(str)

	def __init__(self, parent=None):
		super(GuiApp, self).__init__(parent)
		self.setupUi(self)

		# init text
		# self.textEdit_2.setText(lorem)
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

	def textUpdateMethod(self, patchText):
		patch = self.dmp.patch_fromText(patchText)
		oldText = str(self.textEdit.toPlainText())
		newText, result = self.dmp.patch_apply(patch, oldText)
		self.textEdit.setText(newText)
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
			self.statusLabel.setText('Master Document')
			self.newPushButton.setDisabled(True)
		return

	def remoteDocumentMethod(self):
		addr = self.addressLineEdit.text()
		if len(addr) == len('000.000.000.000'):
			port = self.portSpinBox.value()
			self.tcpSocket.connect((addr, port))
			self.textEdit_2.append('Connected to %s:%d' % (addr, port))
			thread = threading.Thread(target=self.sendThread)
			thread.start()
			self.remotePushButton.setDisabled(True)
			self.statusLabel.setText('Slave Document')
		return

	def textChangeMethod(self):
		oldText = self.currentText
		diffText = str(self.textEdit.toPlainText())

		# find diffs
		diffs = self.dmp.diff_main(oldText, diffText)
		# compile patches
		patch = self.dmp.patch_make(oldText, diffText, diffs)
		# create text from patches
		self.sendQueue.put(self.dmp.patch_toText(patch))

		self.currentText = diffText
		return

	def connectionManagerThread(self):
		while True:
			self.emit(QtCore.SIGNAL('updateStatus'), 'Socket is listening on %s:%d' % self.tcpSocket.getsockname())
			self.tcpSocket.listen(5)
			client_socket, client_addr = self.tcpSocket.accept()
			thread = threading.Thread(target=self.connectionThread,
			                          args=(client_socket, client_addr))
			thread.start()
		return

	def connectionThread(self, client_socket, client_addr):
		self.emit(QtCore.SIGNAL('updateStatus'), 'Client connected from %s:%d' % client_socket.getsockname())
		try:
			while True:
				data = client_socket.recv(2**16)
				print "recieved, :\n",data
				self.emit(QtCore.SIGNAL('updateText'), data)
		except socketError, d:
			print socketError, d
		return

	def sendThread(self):
		try:
			while True:
				data = self.sendQueue.get()
				print "sending :\n", data
				self.tcpSocket.send(data)
		except socketError, d:
			print socketError, d
		return


def main():
	app = QtGui.QApplication(sys.argv)
	form = GuiApp()
	form.show()
	app.exec_()


main()