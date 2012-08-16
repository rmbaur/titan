from PyQt4 import QtCore, QtGui

from ..analysis.processors import *


class ProcPane(QtGui.QWidget):

	def __init__(self):
		super(ProcPane, self).__init__()

		self.preprocs = [Rescaler(), BkgSubtractor()]
		self.prebox = ProcBox('Preprocessing', self.preprocs)

		self.fitprocs = [FFTFitter(), PCAFitter(), GPSAFitter()]
		self.fitbox = ProcBox('Fitting', self.fitprocs)

		self.postprocs = [Normalizer()]
		self.postbox = ProcBox('Postprocessing', self.postprocs)

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.prebox)
		layout.addWidget(self.fitbox)
		layout.addWidget(self.postbox)
		self.setLayout(layout)


class ProcBox(QtGui.QGroupBox):

	def __init__(self, title, procs):
		super(ProcBox, self).__init__()

		self.setTitle(title)

		self.procs = procs
		items = [proc.shortdesc for proc in self.procs]
		self.current_proc = procs[0]

		self.stack = QtGui.QStackedWidget()
		for proc in procs:
			self.stack.addWidget(proc.widget)

		self.options = QtGui.QComboBox()
		self.options.addItems(items)

		self.go_button = QtGui.QPushButton("Go")

		self.options.currentIndexChanged.connect(self.stack.setCurrentIndex)
		self.options.currentIndexChanged.connect(self.set_current_proc)
		self.go_button.clicked.connect(self.current_proc.compute)

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.options)
		layout.addWidget(self.stack)
		layout.addWidget(self.go_button)
		self.setLayout(layout)

	def set_current_proc(self, idx):
		self.go_button.clicked.disconnect(self.current_proc.compute)
		self.current_proc = self.procs[idx]
		self.go_button.clicked.connect(self.current_proc.compute)