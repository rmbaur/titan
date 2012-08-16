from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class DataModel(QtCore.QObject):

	imshow_current_changed = QtCore.pyqtSignal()
	plot_changed = QtCore.pyqtSignal()

	def __init__(self):
		super(DataModel, self).__init__()

		self._plotdata = None

		self._imshowdata = None
		self._current = 0
		self._min = 0
		try:
			self.max = len(self._imshowdata) - 1
		except TypeError:
			self._max = 0

	@property
	def imshowdata(self):
		return self._imshowdata

	@imshowdata.setter
	def imshowdata(self, val):
		self._imshowdata = val
		self._current = 0
		self._max = len(self._imshowdata) - 1
		self.imshow_current_changed.emit()

	@property
	def plotdata(self):
		return self._plotdata

	@plotdata.setter
	def plotdata(self, val):
		self._plotdata = val
		self.plot_changed.emit()

	def prev(self):
		if self._current != self._min:
			self._current -= 1
			self.imshow_current_changed.emit()

	def next(self):
		if self._current != self._max:
			self._current += 1
			self.imshow_current_changed.emit()


class DataView(QtGui.QSplitter):

	def __init__(self, model=None):
		super(DataView, self).__init__()
		self._model = model

		self.imageview = ImshowCanvas()
		self.buttons = PrevNextButtons()
		self.plotview = PlotCanvas()

		self.imagewidget = QtGui.QWidget(parent=self)
		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.imageview)
		layout.addWidget(self.buttons)
		self.imagewidget.setLayout(layout)

		self.addWidget(self.imagewidget)
		self.addWidget(self.plotview)

		self.setStretchFactor(0, 3)
		self.setStretchFactor(1, 1)

		self.setOrientation(QtCore.Qt.Vertical)

	def imshow_draw(self):
		self.imageview.update_figure(self._model.imshowdata[self._model._current])

	def plot_draw(self):
		self.plotview.update_figure(self._model.plotdata)


class Canvas(FigureCanvasQTAgg):

	def __init__(self, parent=None):
		fig = Figure()
		self.axes = fig.add_subplot(111)
		self.axes.hold(False)

		FigureCanvasQTAgg.__init__(self, fig)

		FigureCanvasQTAgg.setSizePolicy(self,
										QtGui.QSizePolicy.Expanding,
										QtGui.QSizePolicy.Expanding)
		FigureCanvasQTAgg.updateGeometry(self)

		self.setParent(parent)

	def update_figure():
		pass


class ImshowCanvas(Canvas):

	def update_figure(self, data):
		self.axes.imshow(data, origin='lower')
		self.draw()


class PlotCanvas(Canvas):

	def update_figure(self, data):
		self.axes.plot(data)
		self.draw()


class PrevNextButtons(QtGui.QWidget):

    def __init__(self, parent=None):
        super(PrevNextButtons, self).__init__()

        self.prev = QtGui.QPushButton("<- Prev")
        self.next = QtGui.QPushButton("Next ->")

        buttons = QtGui.QHBoxLayout()
        buttons.addWidget(self.prev)
        buttons.addStretch()
        buttons.addWidget(self.next)

        self.setLayout(buttons)