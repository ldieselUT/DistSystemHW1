from PyQt4 import QtGui
import sys
from gui import gui
import lib.diff_match_patch as DMP
from socket import AF_INET, SOCK_STREAM, socket

textA = "the cat in the red hat"
textB = "the feline in the blue hat"

lorem = reduce(lambda x,y : x+y ,open('lorem','r').readlines())


class GuiApp(QtGui.QMainWindow, gui.Ui_MainWindow):
	def __init__(self, parent=None):
		super(GuiApp, self).__init__(parent)
		self.setupUi(self)

		# init text
		self.textEdit_2.setText(lorem)
		self.textEdit.setText(lorem)
		self.currentText = str(self.textEdit.toPlainText())

		# connect methods
		self.textEdit.textChanged.connect(self.textChangeMethod)
		self.newPushButton.clicked.connect(self.newDocumentMethod)
		self.remotePushButton.clicked.connect(self.remoteDocumentMethod)

		self.dmp = DMP.diff_match_patch()

		self.tcpSocket = socket(AF_INET, SOCK_STREAM)

	def newDocumentMethod(self):
		addr = self.addressLineEdit.text()
		if len(addr) == len('000.000.000.000'):
			port = self.portSpinBox.value()
			self.tcpSocket.bind((addr, port))
			self.statusLabel.setText('Socket is listening on %s:%d' % self.tcpSocket.getsockname())
			self.tcpSocket.listen(10)
			client_socket, client_addr = self.tcpSocket.accept()
			self.statusLabel.setText('Client connected from %s:%d' % client_socket.getsockname())
		return

	def remoteDocumentMethod(self):
		addr = self.addressLineEdit.text()
		if len(addr) == len('000.000.000.000'):
			port = self.portSpinBox.value()
			self.tcpSocket.connect((addr, port))
			self.statusLabel.setText('Connected to %s:%d' % (addr, port))
		return

	def textChangeMethod(self):

		oldText = self.currentText
		diffText = str(self.textEdit.toPlainText())

		# find diffs
		diffs = self.dmp.diff_main(oldText, diffText)
		# compile patches
		patch = self.dmp.patch_make(oldText, diffText, diffs)
		# create text from patches
		newText, result = self.dmp.patch_apply(patch, str(self.textEdit_2.toPlainText()))

		if False in result:
			print result

		self.textEdit_2.setText(newText)

		self.currentText = newText

		return


def main():
	app = QtGui.QApplication(sys.argv)
	form = GuiApp()
	form.show()
	app.exec_()


main()

# create a diff_match_patch object
dmp = DMP.diff_match_patch()

# Depending on the kind of text you work with, in term of overall length
# and complexity, you may want to extend (or here suppress) the
# time_out feature
dmp.Diff_Timeout = 0  # or some other value, default is 1.0 seconds

# All 'diff' jobs start with invoking diff_main()
diffs = dmp.diff_main(textA, textB)

# diff_cleanupSemantic() is used to make the diffs array more "human" readable
dmp.diff_cleanupSemantic(diffs)

print diffs
# and if you want the results as some ready to display HMTL snippet
htmlSnippet = dmp.diff_prettyHtml(diffs)

print htmlSnippet

txt0 = ''
txt1 = ''

patch = dmp.patch_make(textA, textB, diffs)

print dmp.patch_toText(patch)

print dmp.patch_apply(patch, textA)
print textB
