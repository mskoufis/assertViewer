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
            for i in np.arange(1,self._asics+1):
                getattr(self.ui, f'PyDMWaveformPlot_{i}').addChannel(y_channel = f'{self._dataReceiver}.ASIC{i-1}SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif noise_checkbox.isChecked() and pedestals_checkbox.isChecked():
            for i in np.arange(1,self._asics+1):
                getattr(self.ui, f'PyDMWaveformPlot_{i}').addChannel(y_channel = f'{self._dataReceiver}.ASIC{i-1}SigNosPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif noise_checkbox.isChecked() and cm_checkbox.isChecked():
            for i in np.arange(1,self._asics+1):
                getattr(self.ui, f'PyDMWaveformPlot_{i}').addChannel(y_channel = f'{self._dataReceiver}.ASIC{i-1}SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif pedestals_checkbox.isChecked() and cm_checkbox.isChecked():
            for i in np.arange(1,self._asics+1):
                getattr(self.ui, f'PyDMWaveformPlot_{i}').addChannel(y_channel = f'{self._dataReceiver}.ASIC{i-1}SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif noise_checkbox.isChecked():
            for i in np.arange(1,self._asics+1):
                getattr(self.ui, f'PyDMWaveformPlot_{i}').addChannel(y_channel = f'{self._dataReceiver}.ASIC{i-1}SigNos',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif pedestals_checkbox.isChecked():
            for i in np.arange(1,self._asics+1):
                getattr(self.ui, f'PyDMWaveformPlot_{i}').addChannel(y_channel = f'{self._dataReceiver}.ASIC{i-1}SigPed',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif cm_checkbox.isChecked():
            # Displaying pure signals for now
            for i in np.arange(1,self._asics+1):
                getattr(self.ui, f'PyDMWaveformPlot_{i}').addChannel(y_channel = f'{self._dataReceiver}.ASIC{i-1}Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        elif not noise_checkbox.isChecked() and not pedestals_checkbox.isChecked() and not cm_checkbox.isChecked():
            for i in np.arange(1,self._asics+1):
                getattr(self.ui, f'PyDMWaveformPlot_{i}').addChannel(y_channel = f'{self._dataReceiver}.ASIC{i-1}Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")
        else:
            pass

    def resetPlots(self):
        for i in np.arange(1,self._asics+1):
            getattr(self.ui, f'PyDMWaveformPlot_{i}').clearCurves()

    def ui_filename(self):
        # Point to the UI file
        return 'ui/assertViewerPyDM_EventMonitoring.ui'

    def ui_filepath(self):
        # Return the full path to the UI file
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())
