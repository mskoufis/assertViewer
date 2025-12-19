#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : Configuration file for ASSERT event display
#-----------------------------------------------------------------------------
# Borrowed from ePixGUI.py (ePixViewer, https://github.com/slaclab/ePixViewer)

import os
import pydm
from qtpy.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout

def runReceiverDisplay(dataReceiver, serverList='localhost:9090', root=None,
                   title=None,sizeX=800,sizeY=1000,maxListExpand=5,maxListSize=100):

    #pyrogue.pydm.runPyDM()

    if root is not None:

        if not root.running:
            raise Exception("Attempt to use pydm with root that has not started")

        os.environ['ROGUE_SERVERS'] = 'localhost:{}'.format(root.serverPort)
    else:
        os.environ['ROGUE_SERVERS'] = serverList

    ui = os.path.abspath(__file__)

    if title is None:
        title = "Assert Live Event Display: {}".format(os.getenv('ROGUE_SERVERS'))

    args = []
    args.append(f"sizeX={sizeX}")
    args.append(f"sizeY={sizeY}")
    args.append(f"title='{title}'")
    args.append(f"maxListExpand={maxListExpand}")
    args.append(f"maxListSize={maxListSize}")

    macrosA = {}
    macrosA['dataReceiver'] = dataReceiver
    macrosA['title'] = title
    macrosA['sizeX'] = sizeX
    macrosA['sizeY'] = sizeY
    app = pydm.PyDMApplication(ui_file=ui,
                               command_line_args=args,
                               macros=macrosA,
                               hide_nav_bar=True,
                               hide_menu_bar=True,
                               hide_status_bar=True)
    app.exec()

class assertGUI(pydm.Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(parent=parent, args=args, macros=macros)
        # print(f'{macros=}')
        self._dataReceiver = macros['dataReceiver']
#        self.ui.PyDMImageView.newImageSignal.connect(self.updateDisplay)
#        self.ui.PyDMImageView.scene.sigMouseClicked.connect(self.clickProcess)
        # self.ui.PyDMLineEdit_3.textChanged.connect(self.resetTimePlot)
        # self.ui.PyDMLineEdit_6.textChanged.connect(self.resetTimePlot)
        # self.ui.lineEdit.textChanged.connect(self.setTimeSpan)
        # self.ui.PyDMCheckbox_15.stateChanged.connect(self.resetTimePlot)
        # self.ui.pushButton.clicked.connect(self.resetTimePlot)
        self.sizeX = macros['sizeX']
        self.sizeY = macros['sizeY']
        self.setup_update()
        self.setup_display()

    def setup_update(self):
        #self.ui.PyDMLineEdit_3.textChanged.connect(self.resetTimePlot)
        #self.ui.PyDMLineEdit.channel=f'{self._dataReceiver}.ASIC0FrameCnt'
        grid_layout=QGridLayout()
        label=QLabel(f'Frame Count 2')
        #lineEdit=PyDMLineEdit(init_channel=f'{self._dataReceiver}.ASIC0FrameCnt')
        #lineEdit=PyDMLineEdit()
        grid_layout.addWidget(label,1,0)
        #grid_layout.addWidget(lineEdit,1,1)
        self.ui.PyDMTabWidget_main.setLayout(grid_layout)
        pass

    def setup_display(self):
        self.ui.PyDMCheckbox_noise.clicked.connect(self.onClick_updatePlots)
        self.ui.PyDMCheckbox_pedestals.clicked.connect(self.onClick_updatePlots)
        self.ui.PyDMCheckbox_cm.clicked.connect(self.onClick_updatePlots)

    def onClick_updatePlots(self):
        # Read current plot settings and update plots
        noise_checkbox     = self.ui.PyDMCheckbox_noise 
        pedestals_checkbox = self.ui.PyDMCheckbox_pedestals
        cm_checkbox        = self.ui.PyDMCheckbox_cm

        # Redraw the ADC counts on all sensor planes
        # Check to see if the frame count has incremented
        # If it has, then reset all plots and redraw the counts
        # Assuming all count combinations exist as rogue variables already
        # And also that the framecount is parsed out and stored in a rogue variable
        # The checkboxes determine which channel we add to the plot each time

        # Depending on the configuration, update the curves with the appropriate counts  
        if noise_checkbox.isChecked() and pedestals_checkbox.isChecked() and cm_checkbox.isChecked():
            pass
        elif noise_checkbox.isChecked() and pedestals_checkbox.isChecked():
            pass
        elif noise_checkbox.isChecked() and cm_checkbox.isChecked():
            pass
        elif pedestals_checkbox.isChecked() and cm_checkbox.isChecked():
            pass
        elif noise_checkbox.isChecked():
            pass
        elif pedestals_checkbox.isChecked():
            pass
        elif cm_checkbox.isChecked():
            pass
        else:
            pass

    def updateDisplay(self):
        pass
#        maxContrast = int(self.ui.PyDMLineEdit_5.displayText())
#        minContrast = int(self.ui.PyDMLineEdit_4.displayText())
#        self.ui.PyDMImageView.setColorMapLimits(minContrast, maxContrast)

    # def setTimeSpan(self):
    #     self.ui.PyDMTimePlot.setTimeSpan(int(self.ui.lineEdit.text()))

    def clickProcess(self, event):
        pass
#        pos = self.ui.PyDMImageView.getView().getViewBox().mapSceneToView(event.scenePos())
#        if self.sizeX != 0 and int(pos.x()) > self.sizeX :
#            x = str(self.sizeX-1)
#        elif int(pos.x()) < 0 :
#            x = str(0)
#        else :
#            x = str(int(pos.x()))
#
#        if self.sizeY != 0 and  int(pos.y()) > self.sizeY :
#            y = str(self.sizeY-1)
#        elif int(pos.y()) < 0 :
#            y = str(0)
#        else :
#            y = str(int(pos.y()))
#
#        self.ui.PyDMLineEdit_2.setText(x)
#        self.ui.PyDMLineEdit_2.send_value()
#        self.ui.PyDMLineEdit_6.setText(y)
#        self.ui.PyDMLineEdit_6.send_value()

    # def resetTimePlot(self):
    #     self.ui.PyDMTimePlot.removeYChannel(self.ui.PyDMTimePlot.findCurve(
    #         f'{self._dataReceiver}.PixelData'))
    #     self.ui.PyDMTimePlot.addYChannel(
    #         y_channel = f'{self._dataReceiver}.PixelData',
    #         name = "Pixel counts",
    #         plot_style = "Line",
    #         color = "white",
    #         lineWidth = 1)

    def ui_filename(self):
        # Point to the UI file
        return 'ui/assertViewerPyDM_ppl.ui'

    def ui_filepath(self):
        # Return the full path to the UI file
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())
