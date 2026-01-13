#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : Configuration file for ASSERT event display
#-----------------------------------------------------------------------------
# Borrowed from ePixGUI.py (ePixViewer, https://github.com/slaclab/ePixViewer)

import os
import pydm
import numpy as np
from pydm.widgets import PyDMLineEdit, PyDMLabel
from qtpy.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy

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
        self._asics = 8
        self._dataReceiver = macros['dataReceiver']
#        self.ui.PyDMImageView.newImageSignal.connect(self.updateDisplay)
#        self.ui.PyDMImageView.scene.sigMouseClicked.connect(self.clickProcess)
        # self.ui.PyDMLineEdit_3.textChanged.connect(self.resetPlots)
        # self.ui.PyDMLineEdit_6.textChanged.connect(self.resetPlots)
        # self.ui.lineEdit.textChanged.connect(self.setTimeSpan)
        # self.ui.PyDMCheckbox_15.stateChanged.connect(self.resetPlots)
        # self.ui.pushButton.clicked.connect(self.resetPlots)
        self.sizeX = macros['sizeX']
        self.sizeY = macros['sizeY']
        self.setup_main_tab()
        self.setup_config_tab()

    def setup_main_tab(self):
        grid_layout=QGridLayout()
        spacer_label=QLabel('')
        frame_cnt_label=QLabel(f'Frame Count')
        frame_cnt_line=PyDMLineEdit(init_channel=f'{self._dataReceiver}.ASIC0FrameCnt')
        frame_cnt_line.textChanged.connect(self.onClick_updatePlots)
        vertical_spacer=QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        grid_layout.addWidget(spacer_label,0,0)
        grid_layout.addWidget(frame_cnt_label,1,0)
        grid_layout.addWidget(frame_cnt_line,1,1)
        grid_layout.addItem(vertical_spacer,2,0)
        self.ui.PyDMTabWidget_main.setLayout(grid_layout)

    def setup_config_tab(self):
        self.ui.PyDMCheckbox_noise.setChecked(True)
        self.ui.PyDMCheckbox_pedestals.setChecked(True)
        self.ui.PyDMCheckbox_cm.setChecked(True)

        self.ui.PyDMCheckbox_noise.clicked.connect(self.onClick_updatePlots)
        self.ui.PyDMCheckbox_pedestals.clicked.connect(self.onClick_updatePlots)
        self.ui.PyDMCheckbox_cm.clicked.connect(self.onClick_updatePlots)

    def get_attribute_dynamically(self, attribute_name):
        # Accessing an instance variable dynamically
        instance_attr = getattr(self, attribute_name, "Attribute not found")
        return instance_attr

    def onClick_updatePlots(self):
        #print('Update the plots ...\n')

        self.resetPlots()

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
            self.ui.PyDMWaveformPlot_1.addChannel(y_channel = f'{self._dataReceiver}.ASIC0SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_2.addChannel(y_channel = f'{self._dataReceiver}.ASIC1SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_3.addChannel(y_channel = f'{self._dataReceiver}.ASIC2SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_4.addChannel(y_channel = f'{self._dataReceiver}.ASIC3SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_5.addChannel(y_channel = f'{self._dataReceiver}.ASIC4SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_6.addChannel(y_channel = f'{self._dataReceiver}.ASIC5SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_7.addChannel(y_channel = f'{self._dataReceiver}.ASIC6SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_8.addChannel(y_channel = f'{self._dataReceiver}.ASIC7SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif noise_checkbox.isChecked() and pedestals_checkbox.isChecked():
            self.ui.PyDMWaveformPlot_1.addChannel(y_channel = f'{self._dataReceiver}.ASIC0SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_2.addChannel(y_channel = f'{self._dataReceiver}.ASIC1SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_3.addChannel(y_channel = f'{self._dataReceiver}.ASIC2SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_4.addChannel(y_channel = f'{self._dataReceiver}.ASIC3SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_5.addChannel(y_channel = f'{self._dataReceiver}.ASIC4SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_6.addChannel(y_channel = f'{self._dataReceiver}.ASIC5SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_7.addChannel(y_channel = f'{self._dataReceiver}.ASIC6SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_8.addChannel(y_channel = f'{self._dataReceiver}.ASIC7SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif noise_checkbox.isChecked() and cm_checkbox.isChecked():
            # Displaying signal with noise for now
            self.ui.PyDMWaveformPlot_1.addChannel(y_channel = f'{self._dataReceiver}.ASIC0SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_2.addChannel(y_channel = f'{self._dataReceiver}.ASIC1SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_3.addChannel(y_channel = f'{self._dataReceiver}.ASIC2SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_4.addChannel(y_channel = f'{self._dataReceiver}.ASIC3SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_5.addChannel(y_channel = f'{self._dataReceiver}.ASIC4SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_6.addChannel(y_channel = f'{self._dataReceiver}.ASIC5SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_7.addChannel(y_channel = f'{self._dataReceiver}.ASIC6SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_8.addChannel(y_channel = f'{self._dataReceiver}.ASIC7SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif pedestals_checkbox.isChecked() and cm_checkbox.isChecked():
            # Displaying signal with pedestals for now
            self.ui.PyDMWaveformPlot_1.addChannel(y_channel = f'{self._dataReceiver}.ASIC0SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_2.addChannel(y_channel = f'{self._dataReceiver}.ASIC1SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_3.addChannel(y_channel = f'{self._dataReceiver}.ASIC2SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_4.addChannel(y_channel = f'{self._dataReceiver}.ASIC3SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_5.addChannel(y_channel = f'{self._dataReceiver}.ASIC4SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_6.addChannel(y_channel = f'{self._dataReceiver}.ASIC5SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_7.addChannel(y_channel = f'{self._dataReceiver}.ASIC6SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_8.addChannel(y_channel = f'{self._dataReceiver}.ASIC7SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif noise_checkbox.isChecked():
            self.ui.PyDMWaveformPlot_1.addChannel(y_channel = f'{self._dataReceiver}.ASIC0SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_2.addChannel(y_channel = f'{self._dataReceiver}.ASIC1SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_3.addChannel(y_channel = f'{self._dataReceiver}.ASIC2SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_4.addChannel(y_channel = f'{self._dataReceiver}.ASIC3SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_5.addChannel(y_channel = f'{self._dataReceiver}.ASIC4SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_6.addChannel(y_channel = f'{self._dataReceiver}.ASIC5SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_7.addChannel(y_channel = f'{self._dataReceiver}.ASIC6SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_8.addChannel(y_channel = f'{self._dataReceiver}.ASIC7SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif pedestals_checkbox.isChecked():
            self.ui.PyDMWaveformPlot_1.addChannel(y_channel = f'{self._dataReceiver}.ASIC0SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_2.addChannel(y_channel = f'{self._dataReceiver}.ASIC1SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_3.addChannel(y_channel = f'{self._dataReceiver}.ASIC2SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_4.addChannel(y_channel = f'{self._dataReceiver}.ASIC3SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_5.addChannel(y_channel = f'{self._dataReceiver}.ASIC4SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_6.addChannel(y_channel = f'{self._dataReceiver}.ASIC5SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_7.addChannel(y_channel = f'{self._dataReceiver}.ASIC6SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_8.addChannel(y_channel = f'{self._dataReceiver}.ASIC7SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif cm_checkbox.isChecked():
            # Displaying pure signals for now
            self.ui.PyDMWaveformPlot_1.addChannel(y_channel = f'{self._dataReceiver}.ASIC0Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_2.addChannel(y_channel = f'{self._dataReceiver}.ASIC1Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_3.addChannel(y_channel = f'{self._dataReceiver}.ASIC2Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_4.addChannel(y_channel = f'{self._dataReceiver}.ASIC3Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_5.addChannel(y_channel = f'{self._dataReceiver}.ASIC4Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_6.addChannel(y_channel = f'{self._dataReceiver}.ASIC5Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_7.addChannel(y_channel = f'{self._dataReceiver}.ASIC6Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_8.addChannel(y_channel = f'{self._dataReceiver}.ASIC7Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif not noise_checkbox.isChecked() and not pedestals_checkbox.isChecked() and not cm_checkbox.isChecked():
            self.ui.PyDMWaveformPlot_1.addChannel(y_channel = f'{self._dataReceiver}.ASIC0Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_2.addChannel(y_channel = f'{self._dataReceiver}.ASIC1Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_3.addChannel(y_channel = f'{self._dataReceiver}.ASIC2Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_4.addChannel(y_channel = f'{self._dataReceiver}.ASIC3Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_5.addChannel(y_channel = f'{self._dataReceiver}.ASIC4Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_6.addChannel(y_channel = f'{self._dataReceiver}.ASIC5Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_7.addChannel(y_channel = f'{self._dataReceiver}.ASIC6Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
            self.ui.PyDMWaveformPlot_8.addChannel(y_channel = f'{self._dataReceiver}.ASIC7Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
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

    def resetPlots(self):
    #     self.ui.PyDMTimePlot.removeYChannel(self.ui.PyDMTimePlot.findCurve(
    #         f'{self._dataReceiver}.PixelData'))
    #     self.ui.PyDMTimePlot.addYChannel(
    #         y_channel = f'{self._dataReceiver}.PixelData',
    #         name = "Pixel counts",
    #         plot_style = "Line",
    #         color = "white",
    #         lineWidth = 1)
         #print('Reset the plots...\n')
         #for asic in np.linspace(1,self._asics,self._asics):
         #   self.ui.get_attribute_dynamically(f'PyDMWaveformPlot_{asic}').clearCurves()
         self.ui.PyDMWaveformPlot_1.clearCurves()
         self.ui.PyDMWaveformPlot_2.clearCurves()
         self.ui.PyDMWaveformPlot_3.clearCurves()
         self.ui.PyDMWaveformPlot_4.clearCurves()
         self.ui.PyDMWaveformPlot_5.clearCurves()
         self.ui.PyDMWaveformPlot_6.clearCurves()
         self.ui.PyDMWaveformPlot_7.clearCurves()
         self.ui.PyDMWaveformPlot_8.clearCurves()

    def ui_filename(self):
        # Point to the UI file
        return 'ui/assertViewerPyDM_ppl.ui'

    def ui_filepath(self):
        # Return the full path to the UI file
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())
