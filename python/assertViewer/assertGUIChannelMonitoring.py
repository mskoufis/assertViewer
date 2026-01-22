#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : Configuration file for ASSERT channel display
#-----------------------------------------------------------------------------
# Borrowed from ePixGUI.py (ePixViewer, https://github.com/slaclab/ePixViewer)

import os
import pydm
import numpy as np
from pydm.widgets import PyDMLineEdit, PyDMLabel
from qtpy.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy

def runChannelDisplay(dataReceiver, serverList='localhost:9090', root=None,
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
        title = "Assert Live Channel Display: {}".format(os.getenv('ROGUE_SERVERS'))

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

class assertGUIChannelMonitoring(pydm.Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(parent=parent, args=args, macros=macros)
        self._dataReceiver = macros['dataReceiver']
        #print(f'{macros=}')
#        self.ui.PyDMImageView.scene.sigMouseClicked.connect(self.clickProcess)
        # self.ui.PyDMLineEdit_3.textChanged.connect(self.resetPlots)
        # self.ui.PyDMLineEdit_6.textChanged.connect(self.resetPlots)
        # self.ui.lineEdit.textChanged.connect(self.setTimeSpan)
        # self.ui.PyDMCheckbox_15.stateChanged.connect(self.resetPlots)
        # self.ui.pushButton.clicked.connect(self.resetPlots)
        self.sizeX = macros['sizeX']
        self.sizeY = macros['sizeY']
        self._asics = 8
        self.set_image_channels()
        self.setup_main_tab()

    def set_image_channels(self):
        self.ui.PyDMImageView_1.setImageChannel(f"{self._dataReceiver}.ASIC0Image")
        self.ui.PyDMImageView_2.setImageChannel(f"{self._dataReceiver}.ASIC1Image")
        self.ui.PyDMImageView_3.setImageChannel(f"{self._dataReceiver}.ASIC2Image")
        self.ui.PyDMImageView_4.setImageChannel(f"{self._dataReceiver}.ASIC3Image")
        self.ui.PyDMImageView_5.setImageChannel(f"{self._dataReceiver}.ASIC4Image")
        self.ui.PyDMImageView_6.setImageChannel(f"{self._dataReceiver}.ASIC5Image")
        self.ui.PyDMImageView_7.setImageChannel(f"{self._dataReceiver}.ASIC6Image")
        self.ui.PyDMImageView_8.setImageChannel(f"{self._dataReceiver}.ASIC7Image")

        #self.ui.PyDMImageView_1.newImageSignal.connect(self.updateDisplay)

    def setup_main_tab(self):
        self.ui.PyDMLineEdit_1.setChannel(f'{self._dataReceiver}.ASIC0FrameCnt')
        self.ui.PyDMLineEdit_1.textChanged.connect(self.updateDisplay)

        self.ui.PyDMLineEdit_2.setChannel(f'{self._dataReceiver}.MinContrast')
        self.ui.PyDMLineEdit_3.setChannel(f'{self._dataReceiver}.MaxContrast')

        self.ui.PyDMLineEdit_4.setChannel(f'{self._dataReceiver}.MinContrast')
        self.ui.PyDMLineEdit_4.textChanged.connect(self.updateDisplay)

        self.ui.PyDMLineEdit_5.setChannel(f'{self._dataReceiver}.MaxContrast')
        self.ui.PyDMLineEdit_5.textChanged.connect(self.updateDisplay)

    def get_attribute_dynamically(self, attribute_name):
        # Accessing an instance variable dynamically
        instance_attr = getattr(self, attribute_name, "Attribute not found")
        return instance_attr

    def updateDisplay(self):
        minContrast = int(self.ui.PyDMLineEdit_2.displayText())
        maxContrast = int(self.ui.PyDMLineEdit_3.displayText())
        self.ui.PyDMImageView_1.setColorMapLimits(minContrast, maxContrast)
        self.ui.PyDMImageView_2.setColorMapLimits(minContrast, maxContrast)
        self.ui.PyDMImageView_3.setColorMapLimits(minContrast, maxContrast)
        self.ui.PyDMImageView_4.setColorMapLimits(minContrast, maxContrast)
        self.ui.PyDMImageView_5.setColorMapLimits(minContrast, maxContrast)
        self.ui.PyDMImageView_6.setColorMapLimits(minContrast, maxContrast)
        self.ui.PyDMImageView_7.setColorMapLimits(minContrast, maxContrast)
        self.ui.PyDMImageView_8.setColorMapLimits(minContrast, maxContrast)

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

    def ui_filename(self):
        # Point to the UI file
        return 'ui/assertViewerPyDM_StripMonitoring.ui'

    def ui_filepath(self):
        # Return the full path to the UI file
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())
