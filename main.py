from PyQt4 import QtGui
import sys
from gui import gui
import lib.diff_match_patch as DMP

DELETE = DMP.diff_match_patch.DIFF_DELETE
INSERT = DMP.diff_match_patch.DIFF_INSERT
EQUAL = DMP.diff_match_patch.DIFF_EQUAL

textA = "the cat in the red hat"
textB = "the feline in the blue hat"

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

for dif in diffs:
	operation, text = dif
	if operation == DELETE:
		txt0 += text
	elif operation == INSERT:
		txt1 += text
	elif operation == EQUAL:
		txt0 += text
		txt1 += text
	else:
		raise ValueError(operation)

print txt0, '\n', txt1

patch = dmp.patch_make(textA, textB, diffs)

print dmp.patch_toText(patch)

print dmp.patch_apply(patch, textA)
print textB


class GuiApp(QtGui.QMainWindow, gui.Ui_MainWindow):
	def __init__(self, parent=None):
		super(GuiApp, self).__init__(parent)
		self.setupUi(self)


def main():
	app = QtGui.QApplication(sys.argv)
	form = GuiApp()
	form.show()
	app.exec_()


main()
