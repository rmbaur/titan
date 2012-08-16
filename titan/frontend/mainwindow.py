import sys
import os

from PyQt4 import QtCore, QtGui
from praxes.frontend.phynx import FileModel, FileView
from praxes.io.phynx.migration.spec import convert_to_phynx

from .ui import ui_mainwindow
from .plotpane import ImshowCanvas, PlotCanvas


class MainWindow(ui_mainwindow.Ui_MainWindow, QtGui.QMainWindow):

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.setupUi(self)

		self.fileModel = FileModel(self)
		self.fileView = FileView(self.fileModel, self)

		self.twod_viewer = ImshowCanvas()
		self.oned_viewer = PlotCanvas()

		self.splitter.insertWidget(0, self.fileView)

		self.verticallayout1.addWidget(self.twod_viewer)
		self.verticallayout1.addWidget(self.oned_viewer)

	@QtCore.pyqtSignature("")
	# Slimmed down version from Praxes
	def on_actionImportSpecFile_triggered(self, filename=None):
		if filename is None:
			filename = QtGui.QFileDialog.getOpenFileName(
						self,
						"Select spec file to import",
						os.getcwd(),
						"Spec files (*.dat *)"
						)
		if filename:
			h5_filename = QtGui.QFileDialog.getSaveFileName(
							self,
							"Save to which file",
							os.getcwd(),
							"HDF files (*.h5 *.hdf *.hdf5)",
							)
			if h5_filename:
				h5file = convert_to_phynx(filename, h5_filename=h5_filename)
				h5file.close()
				self.openFile(h5_filename)


	@QtCore.pyqtSignature("")  # Magic that prevents double signal-emits
	def on_actionOpenHDF5File_triggered(self, filename=None):
		if filename is None:
			filename = QtGui.QFileDialog.getOpenFileName(
						self,
						"Select HDF5 file to open",
						os.getcwd(),
						"HDF files (*.h5 *.hdf *.hdf5)"
						)
		if filename:
			self.fileModel.openFile(str(filename))