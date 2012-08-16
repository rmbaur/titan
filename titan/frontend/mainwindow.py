import sys
import os

from PyQt4 import QtCore, QtGui
from libtiff import TIFF as tiff
import numpy as np

from praxes.frontend.phynx import FileModel, FileView
from praxes.io.phynx.migration.spec import convert_to_phynx
from praxes.io.phynx.measurement import Measurement

from .ui import ui_mainwindow
from .plotpane import ImshowCanvas, PlotCanvas


class MainWindow(ui_mainwindow.Ui_MainWindow, QtGui.QMainWindow):

	proxy_changed = QtCore.pyqtSignal()

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

		self.proxy = None
		self.fileView.clicked.connect(self.get_proxy_from_index)

	def get_proxy_from_index(self, index):
		self.proxy = self.fileModel.getProxyFromIndex(index).getNode()
		self.proxy_changed.emit()

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
				h5file = convert_to_phynx(str(filename), h5_filename=str(h5_filename))
				h5file.close()
				self.fileModel.openFile(str(h5_filename))


	@QtCore.pyqtSignature("")
	def on_actionImportImages_triggered(self):
		if not isinstance(self.proxy, Measurement):
			confirm_import = QtGui.QMessageBox()
			confirm_import.setText("The selected parent group is not a Measurement.")
			confirm_import.setInformativeText("Do you want to import images anyway?")
			confirm_import.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
			confirm_import.setDefaultButton(QtGui.QMessageBox.No)
			choice = confirm_import.exec_()
			if choice == QtGui.QMessageBox.No:
				return

		filenames = QtGui.QFileDialog.getOpenFileNames(
						self,
						"Select images to import",
						os.getcwd(),
						"TIF images (*.tif *.tiff)"
						)

		images = []

		for name in sorted(filenames):
			images.append(tiff.open(str(name), mode='r').read_image())

		self.proxy.create_dataset("images", data=np.array(images))


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