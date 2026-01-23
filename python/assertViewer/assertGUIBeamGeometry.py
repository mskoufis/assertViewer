#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : Configuration file for ASSERT beam display
#-----------------------------------------------------------------------------
# Borrowed from ePixGUI.py (ePixViewer, https://github.com/slaclab/ePixViewer)

import os
import time
import pydm
import numpy as np
from pydm.widgets import PyDMLineEdit, PyDMLabel
from qtpy.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy

import rogue
import pyrogue as pr
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets

def runBeamDisplay(dataReceiver,serverList='localhost:9090',port='9090',root=None,
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
        title = "Assert Live Beam Geometry Display: {}".format(os.getenv('ROGUE_SERVERS'))

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
    macrosA['port']  = port
    app = pydm.PyDMApplication(ui_file=ui,
                               command_line_args=args,
                               macros=macrosA,
                               hide_nav_bar=True,
                               hide_menu_bar=True,
                               hide_status_bar=True)
    app.exec()

class assertGUIBeamGeometry(pydm.Display):
    def __init__(self, parent=None, args=None, macros=None):
        super().__init__(parent=parent, args=args, macros=macros)
        # print(f'{macros=}')
        self._asics = 8
        self._port = macros['port']
        self._dataReceiver = macros['dataReceiver']
        self.sizeX = macros['sizeX']
        self.sizeY = macros['sizeY']
        self.setup_plots()
        self.setup_main_tab()
        self.setup_config_tab()
        self.connect_rogue_root()
        
    def connect_rogue_root(self):
        with pr.interfaces.VirtualClient(addr="localhost",port=int(self._port)) as client:
        
           # Get the reference to the root node
           self._root = client.root
        
           # Get a variable value with a read, this returns the native value
           ret = self._root.RogueVersion.get()
           #print(f"Version = {ret}")
       
    def setup_plots(self):
        # Add legends
        self.ui.graphicsView_1.addLegend()
        self.ui.graphicsView_2.addLegend()
        self.ui.graphicsView_3.addLegend()
        self.ui.graphicsView_4.addLegend()

        # Add error bars
        x=np.zeros(64)
        y=np.zeros(64)
        err=np.zeros(64)
        self._error_bars_1 = pg.ErrorBarItem(beam=0.5, pen={'color': 'w', 'width': 1})
        self._error_bars_2 = pg.ErrorBarItem(beam=0.5, pen={'color': 'w', 'width': 1})
        self._error_bars_3 = pg.ErrorBarItem(beam=0.5, pen={'color': 'w', 'width': 1})
        self._error_bars_4 = pg.ErrorBarItem(beam=0.5, pen={'color': 'w', 'width': 1})
        self.ui.graphicsView_1.addItem(self._error_bars_1)
        self.ui.graphicsView_2.addItem(self._error_bars_2)
        self.ui.graphicsView_3.addItem(self._error_bars_3)
        self.ui.graphicsView_4.addItem(self._error_bars_4)
        self._error_bars_1.setData(x=x,y=y,top=err,bottom=err)
        self._error_bars_2.setData(x=x,y=y,top=err,bottom=err)
        self._error_bars_3.setData(x=x,y=y,top=err,bottom=err)
        self._error_bars_4.setData(x=x,y=y,top=err,bottom=err)

        # Show grid
        self.ui.graphicsView_1.showGrid(x=True, y=True)
        self.ui.graphicsView_2.showGrid(x=True, y=True)
        self.ui.graphicsView_3.showGrid(x=True, y=True)
        self.ui.graphicsView_4.showGrid(x=True, y=True)

        # Add x-axis labels
        self.ui.graphicsView_1.setLabel("bottom", "X-coordinate")
        self.ui.graphicsView_2.setLabel("bottom", "X-coordinate")
        self.ui.graphicsView_3.setLabel("bottom", "X-coordinate")
        self.ui.graphicsView_4.setLabel("bottom", "X-coordinate")

        # Add y-axis labels 
        self.ui.graphicsView_1.setLabel("left", "Y-coordinate")
        self.ui.graphicsView_2.setLabel("left", "Y-coordinate")
        self.ui.graphicsView_3.setLabel("left", "Y-coordinate")
        self.ui.graphicsView_4.setLabel("left", "Y-coordinate")

        # Set X and Y ranges
        self.ui.graphicsView_1.setXRange(0, 70, padding=0)
        self.ui.graphicsView_1.setYRange(0, 70, padding=0)
        self.ui.graphicsView_2.setXRange(0, 70, padding=0)
        self.ui.graphicsView_2.setYRange(0, 70, padding=0)
        self.ui.graphicsView_3.setXRange(0, 70, padding=0)
        self.ui.graphicsView_3.setYRange(0, 70, padding=0)
        self.ui.graphicsView_4.setXRange(0, 70, padding=0)
        self.ui.graphicsView_4.setYRange(0, 70, padding=0)

        # Create plot items
        self._plot_item_1 = self.ui.graphicsView_1.plot(x=[], y=[], symbol='o', pen=None, symbolPen={'color': 'm', 'width': 2}, symbolBrush="m", symbolSize=8, name="Beam Geometry (sensor planes 1 & 2)")
        self._plot_item_2 = self.ui.graphicsView_2.plot(x=[], y=[], symbol='o', pen=None, symbolPen={'color': 'm', 'width': 2}, symbolBrush="m", symbolSize=8, name="Beam Geometry (sensor planes 3 & 4)")
        self._plot_item_3 = self.ui.graphicsView_3.plot(x=[], y=[], symbol='o', pen=None, symbolPen={'color': 'm', 'width': 2}, symbolBrush="m", symbolSize=8, name="Beam Geometry (sensor planes 5 & 6)")
        self._plot_item_4 = self.ui.graphicsView_4.plot(x=[], y=[], symbol='o', pen=None, symbolPen={'color': 'm', 'width': 2}, symbolBrush="m", symbolSize=8, name="Beam Geometry (sensor planes 7 & 8)")

        # Set titles
        self.ui.graphicsView_1.setTitle("Beam Geometry (Sensor Planes 1 & 2)")
        self.ui.graphicsView_2.setTitle("Beam Geometry (Sensor Planes 3 & 4)")
        self.ui.graphicsView_3.setTitle("Beam Geometry (Sensor Planes 5 & 6)")
        self.ui.graphicsView_4.setTitle("Beam Geometry (Sensor Planes 7 & 8)")

    def setup_main_tab(self):
        grid_layout=QGridLayout()
        spacer_label=QLabel('')
        frame_cnt_label=QLabel(f'Frame Count')
        frame_cnt_line=PyDMLineEdit(init_channel=f'{self._dataReceiver}.ASIC0FrameCnt')
        frame_cnt_line.textChanged.connect(self.updatePlots)
        vertical_spacer=QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        grid_layout.addWidget(spacer_label,0,0)
        grid_layout.addWidget(frame_cnt_label,1,0)
        grid_layout.addWidget(frame_cnt_line,1,1)
        grid_layout.addItem(vertical_spacer,2,0)
        self.ui.PyDMTabWidget_main.setLayout(grid_layout)

    def setup_config_tab(self):
        self.ui.PyDMCheckbox_feature1.setChecked(False)
        self.ui.PyDMCheckbox_feature2.setChecked(False)
        self.ui.PyDMCheckbox_feature3.setChecked(False)

        self.ui.PyDMCheckbox_feature1.clicked.connect(self.onClick_checkFeature1)
        self.ui.PyDMCheckbox_feature2.clicked.connect(self.onClick_checkFeature2)
        self.ui.PyDMCheckbox_feature3.clicked.connect(self.onClick_checkFeature3)

    def onClick_checkFeature1(self):
        self.ui.PyDMCheckbox_feature1.setChecked(True)
        self.ui.PyDMCheckbox_feature2.setChecked(False)
        self.ui.PyDMCheckbox_feature3.setChecked(False)
        self.updatePlots()

    def onClick_checkFeature2(self):
        self.ui.PyDMCheckbox_feature1.setChecked(False)
        self.ui.PyDMCheckbox_feature2.setChecked(True)
        self.ui.PyDMCheckbox_feature3.setChecked(False)
        self.updatePlots()

    def onClick_checkFeature3(self):
        self.ui.PyDMCheckbox_feature1.setChecked(False)
        self.ui.PyDMCheckbox_feature2.setChecked(False)
        self.ui.PyDMCheckbox_feature3.setChecked(True)
        self.updatePlots()

    def get_attribute_dynamically(self, attribute_name):
        # Accessing an instance variable dynamically
        instance_attr = getattr(self, attribute_name, "Attribute not found")
        return instance_attr

    def computeBeamGeometry(self):
        # Get Rogue ADC counts
        counts1 = self._root.AsicSampleProcessor.ASIC0Sig.get()
        counts2 = self._root.AsicSampleProcessor.ASIC1Sig.get()
        counts3 = self._root.AsicSampleProcessor.ASIC2Sig.get()
        counts4 = self._root.AsicSampleProcessor.ASIC3Sig.get()
        counts5 = self._root.AsicSampleProcessor.ASIC4Sig.get()
        counts6 = self._root.AsicSampleProcessor.ASIC5Sig.get()
        counts7 = self._root.AsicSampleProcessor.ASIC6Sig.get()
        counts8 = self._root.AsicSampleProcessor.ASIC7Sig.get()

        # Get indices of strips with the max counts on each sensor plane
        if len(counts1): max_index_1 = np.argmax(np.array(counts1)) + 1 
        if len(counts2): max_index_2 = np.argmax(np.array(counts2)) + 1
        if len(counts3): max_index_3 = np.argmax(np.array(counts3)) + 1
        if len(counts4): max_index_4 = np.argmax(np.array(counts4)) + 1
        if len(counts5): max_index_5 = np.argmax(np.array(counts5)) + 1
        if len(counts6): max_index_6 = np.argmax(np.array(counts6)) + 1
        if len(counts7): max_index_7 = np.argmax(np.array(counts7)) + 1
        if len(counts8): max_index_8 = np.argmax(np.array(counts8)) + 1

        ## Update plot items
        if len(counts1) and len(counts2): self._plot_item_1.setData(x=np.array([max_index_1]), y=np.array([max_index_2]))
        if len(counts3) and len(counts4): self._plot_item_2.setData(x=np.array([max_index_3]), y=np.array([max_index_4]))
        if len(counts5) and len(counts6): self._plot_item_3.setData(x=np.array([max_index_5]), y=np.array([max_index_6]))
        if len(counts7) and len(counts8): self._plot_item_4.setData(x=np.array([max_index_7]), y=np.array([max_index_8]))

        ## Add error bars
        err = np.full(1,3)
        if len(counts1) and len(counts2): self._error_bars_1.setData(x=np.array([max_index_1]), y=np.array([max_index_2]), top=err, bottom=err)
        if len(counts3) and len(counts4): self._error_bars_2.setData(x=np.array([max_index_3]), y=np.array([max_index_4]), top=err, bottom=err)
        if len(counts5) and len(counts6): self._error_bars_3.setData(x=np.array([max_index_5]), y=np.array([max_index_6]), top=err, bottom=err)
        if len(counts7) and len(counts8): self._error_bars_4.setData(x=np.array([max_index_7]), y=np.array([max_index_8]), top=err, bottom=err)

        # Add beam widths (ROI circles)
        d = [20, 20]
        if len(counts1) and len(counts2):
            if getattr(self, '_roi_circle_1', None) is not None: self.ui.graphicsView_1.removeItem(self._roi_circle_1)
            self._roi_circle_1 = pg.CircleROI([max_index_1-10,max_index_2-10], d, pen=pg.mkPen('m', width=1, style=QtCore.Qt.DashLine), movable=False, resizable=False) 
            self.ui.graphicsView_1.addItem(self._roi_circle_1)
            self._roi_circle_1.aspectLocked = True
        if len(counts3) and len(counts4): 
            if getattr(self, '_roi_circle_2', None) is not None: self.ui.graphicsView_2.removeItem(self._roi_circle_2)
            self._roi_circle_2 = pg.CircleROI([max_index_3-10,max_index_4-10], d, pen=pg.mkPen('m', width=1, style=QtCore.Qt.DashLine), movable=False, resizable=False) 
            self.ui.graphicsView_2.addItem(self._roi_circle_2)
            self._roi_circle_2.aspectLocked = True
        if len(counts5) and len(counts6): 
            if getattr(self, '_roi_circle_3', None) is not None: self.ui.graphicsView_3.removeItem(self._roi_circle_3)
            self._roi_circle_3 = pg.CircleROI([max_index_5-10,max_index_6-10], d, pen=pg.mkPen('m', width=1, style=QtCore.Qt.DashLine), movable=False, resizable=False) 
            self.ui.graphicsView_3.addItem(self._roi_circle_3)
            self._roi_circle_3.aspectLocked = True
        if len(counts7) and len(counts8): 
            if getattr(self, '_roi_circle_4', None) is not None: self.ui.graphicsView_4.removeItem(self._roi_circle_4)
            self._roi_circle_4 = pg.CircleROI([max_index_7-10,max_index_8-10], d, pen=pg.mkPen('m', width=1, style=QtCore.Qt.DashLine), movable=False, resizable=False) 
            self.ui.graphicsView_4.addItem(self._roi_circle_4)
            self._roi_circle_4.aspectLocked = True

        # Set X and Y ranges
        self.ui.graphicsView_1.setXRange(0, 70, padding=0)
        self.ui.graphicsView_1.setYRange(0, 70, padding=0)
        self.ui.graphicsView_2.setXRange(0, 70, padding=0)
        self.ui.graphicsView_2.setYRange(0, 70, padding=0)
        self.ui.graphicsView_3.setXRange(0, 70, padding=0)
        self.ui.graphicsView_3.setYRange(0, 70, padding=0)
        self.ui.graphicsView_4.setXRange(0, 70, padding=0)
        self.ui.graphicsView_4.setYRange(0, 70, padding=0)

    def updatePlots(self):
        #print('Update the plots ...\n')

        # Read current plot settings and update plots
        feature1_checkbox = self.ui.PyDMCheckbox_feature1
        feature2_checkbox = self.ui.PyDMCheckbox_feature2
        feature3_checkbox = self.ui.PyDMCheckbox_feature3

        # Depending on the configuration, update the curves with the appropriate counts
        if feature1_checkbox.isChecked():
            # Add labels, legend and update photon plots
            #self.update_asic_photons()
            pass
        elif feature2_checkbox.isChecked():
            # Add labels, legend and update electron plots
            #self.update_asic_electrons()
            pass
        elif feature3_checkbox.isChecked():
            # Add labels, legend and update LET plots
            #self.update_asic_LET()
            pass
        else:
            self.computeBeamGeometry()
            pass

    def ui_filename(self):
        # Point to the UI file
        return 'ui/assertViewerPyQtGraph_BeamGeometry.ui'

    def ui_filepath(self):
        # Return the full path to the UI file
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())
