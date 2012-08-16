from PyQt4 import QtCore, QtGui

from .ui import ui_procpane


class ProcPane(ui_procpane.Ui_Form, QtGui.QWidget):

	def __init__(self, parent=None):
		super(ProcPane, self).__init__(parent)

		self.setupUi(self)