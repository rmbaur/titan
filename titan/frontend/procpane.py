from PyQt4 import QtCore, QtGui

from ..analysis.processors import *


class ProcPane(QtGui.QWidget):

	def __init__(self, parent=None):
		super(ProcPane, self).__init__(parent)

		self.preprocs = [Rescaler(), BkgSubtractor()]
		self.prebox = ProcBox('Preprocessing', self.preprocs)

		self.fitprocs = [FFTFitter(), PCAFitter(), GPSAFitter()]
		self.fitbox = ProcBox('Fitting', self.fitprocs)

		self.postprocs = [Normalizer(), GaussFilter()]
		self.postbox = ProcBox('Postprocessing', self.postprocs)

		self.signal_options = None
		self.axes_options = None

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.prebox)
		layout.addWidget(self.fitbox)
		layout.addWidget(self.postbox)
		self.setLayout(layout)

	def update_options(self):
		self.prebox.update_widgets(self.signal_options, self.axes_options)
		self.fitbox.update_widgets(self.signal_options, self.axes_options)
		self.postbox.update_widgets(self.signal_options, self.axes_options)



class ProcBox(QtGui.QGroupBox):

	def __init__(self, title, procs, parent=None):
		super(ProcBox, self).__init__(parent)

		self.setTitle(title)

		self.procs = procs
		items = [proc.shortdesc for proc in self.procs]
		self.current_proc = self.procs[0]

		self.stack = QtGui.QStackedWidget()
		for proc in self.procs:
			self.stack.addWidget(proc.widget)

		self.options = QtGui.QComboBox()
		self.options.addItems(items)

		self.go_button = QtGui.QPushButton("Go")

		self.options.currentIndexChanged.connect(self.stack.setCurrentIndex)
		self.options.currentIndexChanged.connect(self.set_current_proc)
		self.go_button.clicked.connect(self.compute_called)

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.options)
		layout.addWidget(self.stack)
		layout.addWidget(self.go_button)
		self.setLayout(layout)
		
	def compute_called(self):
		mw = self.parent().parent().parent().parent()
		mw.proxy = self.current_proc.compute(mw.proxy)
		mw.proxy_changed.emit()

	def set_current_proc(self, idx):
		self.go_button.clicked.disconnect(self.compute_called)
		self.current_proc = self.procs[idx]
		self.go_button.clicked.connect(self.compute_called)

	def update_widgets(self, signals, axes):
		for proc in self.procs:
			proc.update_widget(signals, axes)