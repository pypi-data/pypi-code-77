import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QProgressBar, QPushButton, QLineEdit, QLabel, \
    QVBoxLayout, QHBoxLayout, QComboBox, QGroupBox

from .imageViewerWidget import imageViewerWidget
from .opFlowLabWorker import opFlowLabWorker, opFlowLabConfig
from .styleSheet import invalid_stylesheet, valid_stylesheet, stop_button_stylesheet, start_button_stylesheet


class flowDerivativesTab(QWidget):
    killSignal = pyqtSignal()
    messageSignal = pyqtSignal(str, str)

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        self.forwardPathLabel = QLabel("Forward velocity field folder: ")
        self.layout.addWidget(self.forwardPathLabel)

        self.derivativeLayout = QGridLayout()
        self.derivativeLabel = QLabel("Derivative type")
        self.derivativeLayout.addWidget(self.derivativeLabel, 0, 0)
        self.derivativeComboBox = QComboBox()
        self.derivativeList = {"Vorticity": np.array([[1, 0], [0, -1]]),
                               "Divergence": np.array([[1, 0], [0, 1]]),
                               "Simple Shear": np.array([[0, 1], [1, 0]])}
        self.derivativeComboBox.addItems(list(self.derivativeList.keys()))
        self.derivativeLayout.addWidget(self.derivativeComboBox, 0, 1)
        self.derivativeLayout.setColumnStretch(1, 10)
        self.layout.addLayout(self.derivativeLayout)

        self.optionsGroup = QGroupBox("Options")
        self.optionsLayout = QGridLayout()
        self.optionsLayout.setAlignment(Qt.AlignTop)
        self.optionsLayout.addWidget(QLabel("Starting Frame"), 2, 0)
        self.startingFrameLineEdit = QLineEdit("1")
        self.startingFrameLineEdit.setPlaceholderText("Starting Frame")
        self.optionsLayout.addWidget(self.startingFrameLineEdit, 3, 0)
        self.optionsLayout.addWidget(QLabel("Gaussian smoothing sigma [px]"), 2, 1)
        self.smoothingLineEdit = QLineEdit("None")
        self.smoothingLineEdit.setPlaceholderText("Gaussian smoothing Sigma")
        self.optionsLayout.addWidget(self.smoothingLineEdit, 3, 1)

        self.colorizeLabel = QLabel("Save as colorized image")
        self.optionsLayout.addWidget(self.colorizeLabel, 4, 0)
        self.colorMapComboBox = QComboBox()
        self.colorMaps = ["None", 'viridis', 'plasma', 'coolwarm', 'Spectral', 'bwr', 'twilight', 'hsv', 'baker', 'jet', 'rainbow']
        self.colorMapComboBox.addItems(self.colorMaps)
        self.optionsLayout.addWidget(self.colorMapComboBox, 4, 1)

        self.optionsLayout.addWidget(QLabel("Colormap lower bound value"), 5, 0)
        self.colorbarMinLineEdit = QLineEdit("None")
        self.colorbarMinLineEdit.setPlaceholderText("Colormap lower bound value")
        self.optionsLayout.addWidget(self.colorbarMinLineEdit, 6, 0)
        self.colorbarMinLineEdit.setEnabled(False)
        self.optionsLayout.addWidget(QLabel("Colormap upper bound value"), 5, 1)
        self.colorbarMaxLineEdit = QLineEdit("None")
        self.colorbarMaxLineEdit.setPlaceholderText("Colormap upper bound value")
        self.optionsLayout.addWidget(self.colorbarMaxLineEdit, 6, 1)
        self.colorbarMaxLineEdit.setEnabled(False)
        self.optionsGroup.setLayout(self.optionsLayout)
        self.layout.addWidget(self.optionsGroup)

        self.layout.addStretch()

        self.processButton = QPushButton("Plot derivative")
        self.processButton.setEnabled(False)
        self.buttons = QHBoxLayout()
        self.buttons.addWidget(self.processButton)
        self.displayOutput = QPushButton("Display output")
        self.displayOutput.setEnabled(False)
        self.buttons.addWidget(self.displayOutput)
        self.displayColorWheel = QPushButton("Display colour map")
        self.displayColorWheel.setEnabled(False)
        self.buttons.addWidget(self.displayColorWheel)
        self.layout.addLayout(self.buttons)

        self.progressBarLayout = QHBoxLayout()
        self.progressBar = QProgressBar()
        self.progressBarLayout.addWidget(QLabel("Progress:"))
        self.progressBarLayout.addWidget(self.progressBar)
        self.timeLeft = QLabel("Time Left:")
        self.timeLeft.setMinimumWidth(120)
        self.progressBarLayout.addWidget(self.timeLeft)
        self.layout.addLayout(self.progressBarLayout)

        self.imageViewer = imageViewerWidget()
        self.colorWheelViewer = imageViewerWidget()

        self.config = opFlowLabConfig()

        # create thread
        self.thread = QThread()
        # create object which will be moved to another thread
        self.opFlowLabWorker = opFlowLabWorker()

        # move object to another thread
        self.opFlowLabWorker.moveToThread(self.thread)
        self.opFlowLabWorker.progressSignal.connect(self.updateProgressBar)
        self.killSignal.connect(self.opFlowLabWorker.terminateCalculation)
        self.opFlowLabWorker.finishSignal.connect(self.updateToProcessButton)
        self.opFlowLabWorker.updateSignal.connect(self.updateImageViewer)
        self.opFlowLabWorker.timeSignal.connect(self.updateTimeLeft)

        # connect started signal to run method of object in another thread
        self.thread.started.connect(self.opFlowLabWorker.runDerivative)

        self.processButton.clicked.connect(self.onProcessButtonClicked)
        self.displayOutput.clicked.connect(self.onDisplayOutputButtonClicked)
        self.displayColorWheel.clicked.connect(self.onDisplayColorWheelClicked)

        self.startingFrameLineEdit.editingFinished.connect(self.updateStartFrameValue)
        self.smoothingLineEdit.editingFinished.connect(self.updateSmoothingValue)
        self.colorbarMinLineEdit.editingFinished.connect(self.updateColorbarMinValue)
        self.colorbarMaxLineEdit.editingFinished.connect(self.updateColorbarMaxValue)
        self.colorMapComboBox.currentTextChanged.connect(self.updateColormapOptions)

    @pyqtSlot()
    def updateToProcessButton(self):
        print("Calculation has been stopped")
        self.processButton.setStyleSheet(start_button_stylesheet)
        self.processButton.setText("Process flow derivatives")
        self.thread.quit()

    def updateColormapOptions(self):
        if self.colorMapComboBox.currentText() == "None":
            self.colorbarMinLineEdit.setEnabled(False)
            self.colorbarMaxLineEdit.setEnabled(False)
        else:
            self.colorbarMinLineEdit.setEnabled(True)
            self.colorbarMaxLineEdit.setEnabled(True)

    def onProcessButtonClicked(self):
        if self.thread.isRunning():
            self.killSignal.emit()
            self.thread.quit()
        else:
            valid = True

            list_key = self.derivativeComboBox.currentText()
            self.config.derivative = list_key
            self.config.derivative_matrix = self.derivativeList[list_key]
            self.config.colormap = self.colorMapComboBox.currentText()

            valid = valid and self.updateStartFrameValue()
            valid = valid and self.updateSmoothingValue()
            if self.config.colormap != "None":
                valid = valid and self.updateColorbarMinValue()
                valid = valid and self.updateColorbarMaxValue()

            if self.opFlowLabWorker.isImageLoaded() and self.config.forwardFolderPath is not None:
                if valid is True:
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("###################################################", "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("Plotting derivative [{}] with the following parameters:".format(self.config.derivative), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("------------- Folders ------------", "param")
                    self.messageSignal.emit("Image file path: \"{}\"".format(self.config.imageFilePath), "param")
                    self.messageSignal.emit("Forward velocity field folder path: \"{}\"".format(self.config.forwardFolderPath), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("----------- Parameters -----------", "param")
                    self.messageSignal.emit("Starting frame: {}".format(self.config.start_frame+1), "param")
                    self.messageSignal.emit("Gaussian smoothing sigma: {}".format(self.config.smoothing), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("-------- Save parameters ---------", "param")
                    self.messageSignal.emit("Save location: \"{}\"".format(self.config.forwardFolderPath + "/" + self.config.derivative), "param")
                    self.messageSignal.emit("", "param")
                    self.messageSignal.emit("###################################################", "param")
                    # save parameters
                    self.config.saveParameters("FlowDerivative", ["imageFilePath", "forwardFolderPath",
                                                                  "derivative", "start_frame", "smoothing"])
                    # start thread
                    self.thread.start()
                    self.displayOutput.setEnabled(True)
                    self.displayColorWheel.setEnabled(True)
                    self.processButton.setStyleSheet(stop_button_stylesheet)
                    self.processButton.setText("Stop flow derivatives")
                else:
                    self.messageSignal.emit("Please ensure that all inputs are valid", "error")
            else:
                self.messageSignal.emit("Please load image file and forward velocity field folder first!", "error")

    def onFocusUpdate(self):
        self.forwardPathLabel.setText("Forward velocity field folder: {}".format(self.config.forwardFolderPath))
        if self.config.forwardFolderPath is None:
            self.messageSignal.emit("FlowDerivatives can only be performed when the forward velocity field folder is defined.", "warn")
            self.messageSignal.emit("Please ensure this folder is loaded under the 'Load velocity field' tab.", "warn")
            self.processButton.setEnabled(False)
        else:
            self.processButton.setEnabled(True)

    def updateStartFrameValue(self):
        try:
            start_frame = int(self.startingFrameLineEdit.text())
            assert start_frame >= 1
            self.config.start_frame = start_frame-1
            self.startingFrameLineEdit.setStyleSheet(valid_stylesheet)
            return True
        except ValueError:
            self.startingFrameLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Starting frame should be an integer", "error")
            return False
        except AssertionError:
            self.startingFrameLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Starting frame should be a value greater or equal to 1", "error")
            return False

    def updateSmoothingValue(self):
        try:
            smoothing = self.smoothingLineEdit.text()
            if smoothing.lower() == "none":
                smoothing = None
            else:
                smoothing = int(smoothing)
                assert smoothing >= 0
            self.config.smoothing = smoothing
            self.smoothingLineEdit.setStyleSheet(valid_stylesheet)
            return True
        except ValueError:
            self.smoothingLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Smoothing should be an integer or \"None\"", "error")
            return False
        except AssertionError:
            self.smoothingLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Smoothing should be a value greater than 0", "error")
            return False

    def updateColorbarMinValue(self):
        try:
            colorbarMin = self.colorbarMinLineEdit.text()
            if colorbarMin.lower() == "none":
                colorbarMin = None
            else:
                colorbarMin = float(colorbarMin)

            self.config.colorbarMin = colorbarMin
            self.colorbarMinLineEdit.setStyleSheet(valid_stylesheet)
            return True
        except ValueError:
            self.colorbarMinLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Colormap lower bound value should be an integer, float or \"None\"", "error")
            return False

    def updateColorbarMaxValue(self):
        try:
            colorbarMax = self.colorbarMaxLineEdit.text()
            if colorbarMax.lower() == "none":
                colorbarMax = None
            else:
                colorbarMax = float(colorbarMax)

            self.config.colorbarMax = colorbarMax
            self.colorbarMaxLineEdit.setStyleSheet(valid_stylesheet)
            return True
        except ValueError:
            self.colorbarMaxLineEdit.setStyleSheet(invalid_stylesheet)
            self.messageSignal.emit("Colormap upper bound value should be an integer, float or \"None\"", "error")
            return False

    def onDisplayColorWheelClicked(self):
        self.colorWheelViewer.displayImage()
        self.colorWheelViewer.setWindowTitle("Color wheel")
        if self.config.hasInstance():
            self.colorWheelViewer.updateImageViewer(self.config.colormap_vis)

    def onDisplayOutputButtonClicked(self):
        self.imageViewer.displayImage()
        self.imageViewer.setWindowTitle("Flow derivative")
        if self.config.hasInstance():
            self.imageViewer.updateImageViewer(self.config.images)

    def updateImageViewer(self):
        self.imageViewer.updateImageViewer(self.config.images)
        self.colorWheelViewer.updateImageViewer(self.config.colormap_vis)

    @pyqtSlot(int)
    def updateProgressBar(self, value):
        self.progressBar.setValue(value)

    @pyqtSlot(float)
    def updateTimeLeft(self, value):
        if value > 60:
            self.timeLeft.setText("Time Left: {:.2f} mins".format(value/60))
        else:
            self.timeLeft.setText("Time Left: {:.2f} secs".format(value))
