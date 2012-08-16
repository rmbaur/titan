import sys
import os

from PyQt4 import QtCore, QtGui
from libtiff import TIFF as tiff
import numpy as np

from praxes.frontend.phynx import FileModel, FileView
from praxes.io.phynx.migration.spec import convert_to_phynx
from praxes.io.phynx.measurement import Measurement
from praxes.io.phynx.dataset import Dataset

from .ui import ui_mainwindow
from .plotpane import DataModel, DataView


class MainWindow(ui_mainwindow.Ui_MainWindow, QtGui.QMainWindow):

	proxy_changed = QtCore.pyqtSignal()

	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		self.setupUi(self)

		self.fileModel = FileModel(self)
		self.fileView = FileView(self.fileModel, self)

		self.dataModel = DataModel()
		self.dataView = DataView()
		self.connect_data_model_view()

		self.splitter.insertWidget(0, self.fileView)
		self.splitter.insertWidget(2, self.dataView)
		self.splitter.setStretchFactor(0, 1)
		self.splitter.setStretchFactor(1, 2)
		self.splitter.setStretchFactor(2, 1)

		self.proxy = None
		self.fileView.clicked.connect(self.get_proxy_from_index)
		self.proxy_changed.connect(self.update_proxy)

	def get_proxy_from_index(self, index):
		self.proxy = self.fileModel.getProxyFromIndex(index).getNode()
		self.proxy_changed.emit()

	def connect_data_model_view(self):
		self.dataView.buttons.prev.clicked.connect(self.dataModel.prev)
		self.dataView.buttons.next.clicked.connect(self.dataModel.next)
		self.dataModel.imshow_current_changed.connect(self.dataView.imshow_draw)
		self.dataModel.plot_changed.connect(self.dataView.plot_draw)

	def update_proxy(self):
		try:
			if np.ndim(self.proxy) == 1:
				self.dataModel.plotdata = self.proxy
			elif np.ndim(self.proxy) > 1:
				self.dataModel.imshowdata = self.proxy
		except ValueError:
			pass

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