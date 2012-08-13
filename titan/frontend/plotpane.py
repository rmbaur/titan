from PyQt4 import QtCore, QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


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
		self.axes.imshow(data)
		self.draw()


class PlotCanvas(Canvas):

	def update_figure(self, data):
		self.axes.plot(data)
		self.draw()