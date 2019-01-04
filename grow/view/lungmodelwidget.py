from PySide import QtGui
from .ui_lungmodelwidget import Ui_LungModelWidget
import os

class LungModelWidget(QtGui.QWidget):
    def __init__(self, model, parent=None):
        super(LungModelWidget, self).__init__(parent)
        self._airwayFilenames = ['', '']
        self._surfaceFilenames = ['', '']
        self._outputFilenames = ['', '']
        self._airwayCallback = None
        self._surfaceCallback = None
        self._generateCallback = None

        self._ui = Ui_LungModelWidget()
        self._ui.setupUi(self)

        self._ui.sceneviewer_widget.setContext(model.getContext())
        self._makeConnections()

    def airwayCallback(self, cb):
        self._airwayCallback = cb

    def surfaceCallback(self, cb):
        self._surfaceCallback = cb

    def generateCallback(self, cb):
        self._generateCallback = cb

    def _makeConnections(self):
        self._ui.sceneviewer_widget.graphicsInitialized.connect(self._graphicsUpdate)
        self._ui.generate_pushButton.clicked.connect(self._generateClicked)
        self._ui.airwayIpnode_pushButton.clicked.connect(self._airwayIpnodeClicked)
        self._ui.airwayIpelem_pushButton.clicked.connect(self._airwayIpelemClicked)
        self._ui.surfaceIpnode_pushButton.clicked.connect(self._surfaceIpnodeClicked)
        self._ui.surfaceIpelem_pushButton.clicked.connect(self._surfaceIpelemClicked)
        self._ui.outputExnode_pushButton.clicked.connect(self._outputExnodeClicked)
        self._ui.outputExelem_pushButton.clicked.connect(self._outputExelemClicked)

    def _graphicsUpdate(self):
        sceneViewer = self._ui.sceneviewer_widget.getSceneviewer()
        if sceneViewer is not None:
            sceneViewer.setLookatParametersNonSkew([1.9, -4.5, 2.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0])
            sceneViewer.setTransparencyMode(sceneViewer.TRANSPARENCY_MODE_SLOW)
            sceneViewer.viewAll()

    def setAirways(self, ipnode, ipelem):
        self._ui.airwayIpnode_lineEdit.setText(os.path.relpath(ipnode, os.getcwd()))
        self._ui.airwayIpelem_lineEdit.setText(os.path.relpath(ipelem, os.getcwd()))
        self._airwayFilenames[0] = str(ipnode)
        self._airwayFilenames[1] = str(ipelem)
        self._airwayChanged()
    
    def _airwayIpnodeClicked(self):
        filename, _ = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open airway ipnode file', dir='.', filter='*.ipnode')
        if filename:
            self._ui.airwayIpnode_lineEdit.setText(os.path.relpath(filename, os.getcwd()))
            self._airwayFilenames[0] = str(filename)
            self._airwayChanged()

    def _airwayIpelemClicked(self):
        filename, _ = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open airway ipelem file', dir='.', filter='*.ipelem')
        if filename:
            self._ui.airwayIpelem_lineEdit.setText(os.path.relpath(filename, os.getcwd()))
            self._airwayFilenames[1] = str(filename)
            self._airwayChanged()

    def _airwayChanged(self):
        if self._airwayCallback and self._airwayFilenames[0] and self._airwayFilenames[1]:
            self._airwayCallback(self._airwayFilenames[0], self._airwayFilenames[1])
            self._graphicsUpdate()

    def setSurfaces(self, ipnode, ipelem):
        self._ui.surfaceIpnode_lineEdit.setText(os.path.relpath(ipnode, os.getcwd()))
        self._ui.surfaceIpelem_lineEdit.setText(os.path.relpath(ipelem, os.getcwd()))
        self._surfaceFilenames[0] = str(ipnode)
        self._surfaceFilenames[1] = str(ipelem)
        self._surfaceChanged()
    
    def _surfaceIpnodeClicked(self):
        filename, _ = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open surface ipnode file', dir='.', filter='*.ipnode')
        if filename:
            self._ui.surfaceIpnode_lineEdit.setText(os.path.relpath(filename, os.getcwd()))
            self._surfaceFilenames[0] = str(filename)
            self._surfaceChanged()

    def _surfaceIpelemClicked(self):
        filename, _ = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open surface ipelem file', dir='.', filter='*.ipelem')
        if filename:
            self._ui.surfaceIpelem_lineEdit.setText(os.path.relpath(filename, os.getcwd()))
            self._surfaceFilenames[1] = str(filename)
            self._surfaceChanged()

    def _surfaceChanged(self):
        if self._surfaceCallback and self._surfaceFilenames[0] and self._surfaceFilenames[1]:
            self._surfaceCallback(self._surfaceFilenames[0], self._surfaceFilenames[1])
            self._graphicsUpdate()

    def setOutputs(self, exnode, exelem):
        self._ui.outputExnode_lineEdit.setText(os.path.relpath(exnode, os.getcwd()))
        self._ui.outputExelem_lineEdit.setText(os.path.relpath(exelem, os.getcwd()))
        self._outputFilenames[0] = str(exnode)
        self._outputFilenames[1] = str(exelem)
    
    def _outputExnodeClicked(self):
        filename, _ = QtGui.QFileDialog.getSaveFileName(parent=self, caption='Save output exnode file', dir='.', filter='*.exnode')
        if filename:
            self._ui.outputExnode_lineEdit.setText(os.path.relpath(filename, os.getcwd()))
            self._outputFilenames[0] = str(filename)

    def _outputExelemClicked(self):
        filename, _ = QtGui.QFileDialog.getSaveFileName(parent=self, caption='Save output exelem file', dir='.', filter='*.exelem')
        if filename:
            self._ui.outputExelem_lineEdit.setText(os.path.relpath(filename, os.getcwd()))
            self._outputFilenames[1] = str(filename)

    def _generateClicked(self):
        options = {
            "gridSize": self._ui.gridSize_doubleSpinBox.value(),
            "startNode": self._ui.startNode_spinBox.value(),
            "angleMax": self._ui.angleMax_doubleSpinBox.value(),
            "angleMin": self._ui.angleMin_doubleSpinBox.value(),
            "branchFraction": self._ui.branchFraction_doubleSpinBox.value(),
            "lengthLimit": self._ui.lengthLimit_doubleSpinBox.value(),
            "shortestLength": self._ui.shortestLength_doubleSpinBox.value(),
            "rotationLimit": self._ui.rotationLimit_doubleSpinBox.value(),
        }

        if self._generateCallback:
            self._generateCallback(options, self._outputFilenames[0], self._outputFilenames[1])
