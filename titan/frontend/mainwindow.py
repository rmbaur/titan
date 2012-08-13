import sys

from PyQt4 import QtGui

from .ui import ui_mainwindow
from .plotpane import ImshowCanvas, PlotCanvas


class MainWindow(ui_mainwindow.Ui_MainWindow, QtGui.QMainWindow):

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.setupUi(self)

		self.twod_viewer = ImshowCanvas()
		self.oned_viewer = PlotCanvas()

		self.verticallayout1.addWidget(self.twod_viewer)
		self.verticallayout1.addWidget(self.oned_viewer)

	def on_actionImportSpecFile_triggered(self):
		pass

	def on_actionOpenHDF5File_triggered(self):
		pass