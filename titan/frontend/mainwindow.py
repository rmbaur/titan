import sys
import os

from PyQt4 import QtCore, QtGui

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

	@QtCore.pyqtSignature("")  # Magic that prevents double signal-emits
	def on_actionOpenHDF5File_triggered(self, filename=None):
		if filename:
			print "Not implemented yet"
		else:
			filename = QtGui.QFileDialog.getOpenFileName(
						self,
						"Select HDF5 file to open",
						os.getcwd(),
						"HDF files (*.h5, *.hdf, *.hdf5)"
						)