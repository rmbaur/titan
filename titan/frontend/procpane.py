from PyQt4 import QtCore, QtGui

from .ui import ui_procpane
from ..analysis.processors import Rescaler, BkgSubtractor


class ProcPane(ui_procpane.Ui_Form, QtGui.QWidget):

	def __init__(self, parent=None):
		super(ProcPane, self).__init__(parent)

		self.setupUi(self)

		self.preprocs = [Rescaler(), BkgSubtractor()]

		self.prebox_items = [proc.shortdesc for proc in self.preprocs]
		self.preOptions.addItems(self.prebox_items)

		self.preStack = QtGui.QStackedWidget()
		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.preStack)
		for proc in self.preprocs:
			self.preStack.addWidget(proc.widget)

		print self.preStack.count()

		self.current_preproc = self.preprocs[0]
		self.preStackBox.setLayout(layout)
		self.preStack.setCurrentWidget(self.current_preproc.widget)
		self.preOptions.currentIndexChanged.connect(self.preStack.setCurrentIndex)
		self.preOptions.currentIndexChanged.connect(self.set_current_preproc)

	def set_current_preproc(self, idx):
		self.current_preproc = self.preprocs[idx]