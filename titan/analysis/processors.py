from PyQt4 import QtGui


class Processor(object):

	def __init__(self):
		self.shortdesc = ''
		self.proc_type = ''
		self.widget = QtGui.QWidget()
		self.setup_widget()

	def setup_widget(self):
		pass

	def update_widget(self, signals, axes):
		pass

	def compute(self):
		pass


class Rescaler(Processor):

	def __init__(self):
		super(Rescaler, self).__init__()

		self.shortdesc = 'Rescale'
		self.proc_type = 'pre'

	def setup_widget(self):
		self.counters = QtGui.QComboBox()

		layout = QtGui.QVBoxLayout()
		layout.addWidget(QtGui.QLabel("Select dataset to use for rescaling:"))
		layout.addWidget(self.counters)
		self.widget.setLayout(layout)

	def update_widget(self, signals, axes):
		self.counters.clear()
		for key in signals:
			self.counters.addItems(['%s: %s' % (key, s) for s in signals[key]])

	def compute(self):
		print "Rescale test"


class BkgSubtractor(Processor):

	def __init__(self):
		super(BkgSubtractor, self).__init__()

		self.shortdesc = 'Subtract background'
		self.proc_type = 'pre'

	def setup_widget(self):
		self.bkg = QtGui.QLineEdit()

		layout = QtGui.QVBoxLayout()
		layout.addWidget(QtGui.QLabel("Select background file:"))
		layout.addWidget(self.bkg)
		self.widget.setLayout(layout)

	def compute(self):
		print "Bkg test"


class FFTFitter(Processor):

	def __init__(self):
		super(FFTFitter, self).__init__()

		self.shortdesc = 'FFT'
		self.proc_type = 'fit'

	def setup_widget(self):
		self.periods = QtGui.QSpinBox()
		self.pointsper = QtGui.QSpinBox()

		layout = QtGui.QVBoxLayout()
		layout.addWidget(QtGui.QLabel("Specify number of periods:"))
		layout.addWidget(self.periods)
		layout.addWidget(QtGui.QLabel("Specify points per period:"))
		layout.addWidget(self.pointsper)
		self.widget.setLayout(layout)

	def compute(self):
		print "FFT test"


class PCAFitter(Processor):

	def __init__(self):
		super(PCAFitter, self).__init__()

		self.shortdesc = 'PCA'
		self.proc_type = 'fit'

	def setup_widget(self):
		layout = QtGui.QVBoxLayout()
		layout.addWidget(QtGui.QLabel("No adjustable parameters"))
		self.widget.setLayout(layout)

	def compute(self):
		print "PCA test"


class GPSAFitter(Processor):

	def __init__(self):
		super(GPSAFitter, self).__init__()

		self.shortdesc = 'GPSA'
		self.proc_type = 'fit'

	def setup_widget(self):
		self.axes = QtGui.QComboBox()

		layout = QtGui.QVBoxLayout()
		layout.addWidget(QtGui.QLabel("Select position data:"))
		layout.addWidget(self.axes)
		self.widget.setLayout(layout)

	def update_widget(self, signals, axes):
		self.axes.clear()
		for key in axes:
			self.axes.addItems(['%s: %s' % (key, a) for a in axes[key] ])

	def compute(self):
		print "GPSA test"


class Normalizer(Processor):

	def __init__(self):
		super(Normalizer, self).__init__()

		self.shortdesc = 'Normalize'
		self.proc_type = 'post'

	def setup_widget(self):
		self.ref = QtGui.QComboBox()

		layout = QtGui.QVBoxLayout()
		layout.addWidget(QtGui.QLabel("Select reference dataset:"))
		layout.addWidget(self.ref)
		self.widget.setLayout(layout)

	def compute(self):
		print "Normalize test"


class GaussFilter(Processor):

	def __init__(self):
		super(GaussFilter, self).__init__()

		self.shortdesc = 'Gaussian filter'
		self.proc_type = 'post'

	def setup_widget(self):
		self.filtersize = QtGui.QSpinBox()

		layout = QtGui.QVBoxLayout()
		layout.addWidget(QtGui.QLabel("Select size of blur (pixels):"))
		layout.addWidget(self.filtersize)
		self.widget.setLayout(layout)

	def compute(self):
		print "Gauss test"