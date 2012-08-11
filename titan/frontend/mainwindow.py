import sys

from PyQt4 import QtGui

from .ui import ui_mainwindow


class MainWindow(ui_mainwindow.Ui_MainWindow, QtGui.QMainWindow):

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.setupUi(self)

	def on_actionImportSpecFile_triggered(self):
		pass

	def on_actionOpenHDF5File_triggered(self):
		pass