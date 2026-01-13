#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : Configuration file for ASSERT particle display
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

def runParticleDisplay(dataReceiver,serverList='localhost:9090',port='9090',root=None,
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
        title = "Assert Live Particle Display: {}".format(os.getenv('ROGUE_SERVERS'))

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

class assertGUIParticleMonitoring(pydm.Display):
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
           print(f"Version = {ret}")
       
    def setup_plots(self):
        # Add legends
        self.ui.graphicsView_1.addLegend()
        self.ui.graphicsView_2.addLegend()
        self.ui.graphicsView_3.addLegend()
        self.ui.graphicsView_4.addLegend()
        self.ui.graphicsView_5.addLegend()
        self.ui.graphicsView_6.addLegend()
        self.ui.graphicsView_7.addLegend()
        self.ui.graphicsView_8.addLegend()

        # Add error bars
        x=np.zeros(64)
        y=np.zeros(64)
        err=np.zeros(64)
        self._error_bars_1 = pg.ErrorBarItem(beam=0.5, pen={'color': 'w', 'width': 1})
        self._error_bars_2 = pg.ErrorBarItem(beam=0.5, pen={'color': 'w', 'width': 1})
        self._error_bars_3 = pg.ErrorBarItem(beam=0.5, pen={'color': 'w', 'width': 1})
        self._error_bars_4 = pg.ErrorBarItem(beam=0.5, pen={'color': 'w', 'width': 1})
        self._error_bars_5 = pg.ErrorBarItem(beam=0.5, pen={'color': 'w', 'width': 1})
        self._error_bars_6 = pg.ErrorBarItem(beam=0.5, pen={'color': 'w', 'width': 1})
        self._error_bars_7 = pg.ErrorBarItem(beam=0.5, pen={'color': 'w', 'width': 1})
        self._error_bars_8 = pg.ErrorBarItem(beam=0.5, pen={'color': 'w', 'width': 1})
        self.ui.graphicsView_1.addItem(self._error_bars_1)
        self.ui.graphicsView_2.addItem(self._error_bars_2)
        self.ui.graphicsView_3.addItem(self._error_bars_3)
        self.ui.graphicsView_4.addItem(self._error_bars_4)
        self.ui.graphicsView_5.addItem(self._error_bars_5)
        self.ui.graphicsView_6.addItem(self._error_bars_6)
        self.ui.graphicsView_7.addItem(self._error_bars_7)
        self.ui.graphicsView_8.addItem(self._error_bars_8)
        self._error_bars_1.setData(x=x,y=y,top=err,bottom=err)
        self._error_bars_2.setData(x=x,y=y,top=err,bottom=err)
        self._error_bars_3.setData(x=x,y=y,top=err,bottom=err)
        self._error_bars_4.setData(x=x,y=y,top=err,bottom=err)
        self._error_bars_5.setData(x=x,y=y,top=err,bottom=err)
        self._error_bars_6.setData(x=x,y=y,top=err,bottom=err)
        self._error_bars_7.setData(x=x,y=y,top=err,bottom=err)
        self._error_bars_8.setData(x=x,y=y,top=err,bottom=err)

        # Show grid
        self.ui.graphicsView_1.showGrid(x=True, y=True)
        self.ui.graphicsView_2.showGrid(x=True, y=True)
        self.ui.graphicsView_3.showGrid(x=True, y=True)
        self.ui.graphicsView_4.showGrid(x=True, y=True)
        self.ui.graphicsView_5.showGrid(x=True, y=True)
        self.ui.graphicsView_6.showGrid(x=True, y=True)
        self.ui.graphicsView_7.showGrid(x=True, y=True)
        self.ui.graphicsView_8.showGrid(x=True, y=True)

        # Add x-axis labels
        self.ui.graphicsView_1.setLabel("bottom", "Channel Index")
        self.ui.graphicsView_2.setLabel("bottom", "Channel Index")
        self.ui.graphicsView_3.setLabel("bottom", "Channel Index")
        self.ui.graphicsView_4.setLabel("bottom", "Channel Index")
        self.ui.graphicsView_5.setLabel("bottom", "Channel Index")
        self.ui.graphicsView_6.setLabel("bottom", "Channel Index")
        self.ui.graphicsView_7.setLabel("bottom", "Channel Index")
        self.ui.graphicsView_8.setLabel("bottom", "Channel Index")

        # Create plot items
        self._plot_item_1 = self.ui.graphicsView_1.plot(x=[], y=[], symbol='+', pen=None, symbolPen={'color': 'm', 'width': 2}, symbolBrush="m", symbolSize=8, name="Plane 1 particles", title="Particles per channel")
        self._plot_item_2 = self.ui.graphicsView_2.plot(x=[], y=[], symbol='+', pen=None, symbolPen={'color': 'm', 'width': 2}, symbolBrush="m", symbolSize=8, name="Plane 2 particles", title="Particles per channel")
        self._plot_item_3 = self.ui.graphicsView_3.plot(x=[], y=[], symbol='+', pen=None, symbolPen={'color': 'm', 'width': 2}, symbolBrush="m", symbolSize=8, name="Plane 3 particles", title="Particles per channel")
        self._plot_item_4 = self.ui.graphicsView_4.plot(x=[], y=[], symbol='+', pen=None, symbolPen={'color': 'm', 'width': 2}, symbolBrush="m", symbolSize=8, name="Plane 4 particles", title="Particles per channel")
        self._plot_item_5 = self.ui.graphicsView_5.plot(x=[], y=[], symbol='+', pen=None, symbolPen={'color': 'm', 'width': 2}, symbolBrush="m", symbolSize=8, name="Plane 5 particles", title="Particles per channel")
        self._plot_item_6 = self.ui.graphicsView_6.plot(x=[], y=[], symbol='+', pen=None, symbolPen={'color': 'm', 'width': 2}, symbolBrush="m", symbolSize=8, name="Plane 6 particles", title="Particles per channel")
        self._plot_item_7 = self.ui.graphicsView_7.plot(x=[], y=[], symbol='+', pen=None, symbolPen={'color': 'm', 'width': 2}, symbolBrush="m", symbolSize=8, name="Plane 7 particles", title="Particles per channel")
        self._plot_item_8 = self.ui.graphicsView_8.plot(x=[], y=[], symbol='+', pen=None, symbolPen={'color': 'm', 'width': 2}, symbolBrush="m", symbolSize=8, name="Plane 8 particles", title="Particles per channel")

        # Set titles
        self.ui.graphicsView_1.setTitle("Particles per channel")
        self.ui.graphicsView_2.setTitle("Particles per channel")
        self.ui.graphicsView_3.setTitle("Particles per channel")
        self.ui.graphicsView_4.setTitle("Particles per channel")
        self.ui.graphicsView_5.setTitle("Particles per channel")
        self.ui.graphicsView_6.setTitle("Particles per channel")
        self.ui.graphicsView_7.setTitle("Particles per channel")
        self.ui.graphicsView_8.setTitle("Particles per channel")

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
        self.ui.PyDMCheckbox_photons.setChecked(True)
        self.ui.PyDMCheckbox_electrons.setChecked(False)
        self.ui.PyDMCheckbox_LET.setChecked(False)

        self.ui.PyDMCheckbox_photons.clicked.connect(self.onClick_checkPhotons)
        self.ui.PyDMCheckbox_electrons.clicked.connect(self.onClick_checkElectrons)
        self.ui.PyDMCheckbox_LET.clicked.connect(self.onClick_checkLET)

    def onClick_checkPhotons(self):
        self.ui.PyDMCheckbox_photons.setChecked(True)
        self.ui.PyDMCheckbox_electrons.setChecked(False)
        self.ui.PyDMCheckbox_LET.setChecked(False)
        self.updatePlots()

    def onClick_checkElectrons(self):
        self.ui.PyDMCheckbox_photons.setChecked(False)
        self.ui.PyDMCheckbox_electrons.setChecked(True)
        self.ui.PyDMCheckbox_LET.setChecked(False)
        self.updatePlots()

    def onClick_checkLET(self):
        self.ui.PyDMCheckbox_photons.setChecked(False)
        self.ui.PyDMCheckbox_electrons.setChecked(False)
        self.ui.PyDMCheckbox_LET.setChecked(True)
        self.updatePlots()

    def get_attribute_dynamically(self, attribute_name):
        # Accessing an instance variable dynamically
        instance_attr = getattr(self, attribute_name, "Attribute not found")
        return instance_attr

    def update_asic_photons(self):
        # Get Rogue ADC counts
        counts1 = self._root.AsicSampleProcessor.ASIC0Sig.get()
        counts2 = self._root.AsicSampleProcessor.ASIC1Sig.get()
        counts3 = self._root.AsicSampleProcessor.ASIC2Sig.get()
        counts4 = self._root.AsicSampleProcessor.ASIC3Sig.get()
        counts5 = self._root.AsicSampleProcessor.ASIC4Sig.get()
        counts6 = self._root.AsicSampleProcessor.ASIC5Sig.get()
        counts7 = self._root.AsicSampleProcessor.ASIC6Sig.get()
        counts8 = self._root.AsicSampleProcessor.ASIC7Sig.get()

        # Compute photons
        rng = np.random.default_rng()
        photons1 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        photons2 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        photons3 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        photons4 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        photons5 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        photons6 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        photons7 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        photons8 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
 
        # Update plot items
        channels = np.arange(1, 65, 1)
        self._plot_item_1.setData(x=channels, y=photons1)
        self._plot_item_2.setData(x=channels, y=photons2)
        self._plot_item_3.setData(x=channels, y=photons3)
        self._plot_item_4.setData(x=channels, y=photons4)
        self._plot_item_5.setData(x=channels, y=photons5)
        self._plot_item_6.setData(x=channels, y=photons6)
        self._plot_item_7.setData(x=channels, y=photons7)
        self._plot_item_8.setData(x=channels, y=photons8)
       
        # Add y-axis labels 
        self.ui.graphicsView_1.setLabel("left", "Photons")
        self.ui.graphicsView_2.setLabel("left", "Photons")
        self.ui.graphicsView_3.setLabel("left", "Photons")
        self.ui.graphicsView_4.setLabel("left", "Photons")
        self.ui.graphicsView_5.setLabel("left", "Photons")
        self.ui.graphicsView_6.setLabel("left", "Photons")
        self.ui.graphicsView_7.setLabel("left", "Photons")
        self.ui.graphicsView_8.setLabel("left", "Photons")

        # Add error bars
        err = np.full(64,2)
        self._error_bars_1.setData(x=channels, y=photons1, top=err, bottom=err)
        self._error_bars_2.setData(x=channels, y=photons2, top=err, bottom=err)
        self._error_bars_3.setData(x=channels, y=photons3, top=err, bottom=err)
        self._error_bars_4.setData(x=channels, y=photons4, top=err, bottom=err)
        self._error_bars_5.setData(x=channels, y=photons5, top=err, bottom=err)
        self._error_bars_6.setData(x=channels, y=photons6, top=err, bottom=err)
        self._error_bars_7.setData(x=channels, y=photons7, top=err, bottom=err)
        self._error_bars_8.setData(x=channels, y=photons8, top=err, bottom=err)

    def update_asic_electrons(self):
        # Get Rogue ADC counts
        counts1 = self._root.AsicSampleProcessor.ASIC0Sig.get()
        counts2 = self._root.AsicSampleProcessor.ASIC1Sig.get()
        counts3 = self._root.AsicSampleProcessor.ASIC2Sig.get()
        counts4 = self._root.AsicSampleProcessor.ASIC3Sig.get()
        counts5 = self._root.AsicSampleProcessor.ASIC4Sig.get()
        counts6 = self._root.AsicSampleProcessor.ASIC5Sig.get()
        counts7 = self._root.AsicSampleProcessor.ASIC6Sig.get()
        counts8 = self._root.AsicSampleProcessor.ASIC7Sig.get()

        # Compute electrons
        rng = np.random.default_rng()
        electrons1 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        electrons2 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        electrons3 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        electrons4 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        electrons5 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        electrons6 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        electrons7 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        electrons8 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
 
        # Update plot items
        channels = np.arange(1, 65, 1)
        self._plot_item_1.setData(x=channels, y=electrons1)
        self._plot_item_2.setData(x=channels, y=electrons2)
        self._plot_item_3.setData(x=channels, y=electrons3)
        self._plot_item_4.setData(x=channels, y=electrons4)
        self._plot_item_5.setData(x=channels, y=electrons5)
        self._plot_item_6.setData(x=channels, y=electrons6)
        self._plot_item_7.setData(x=channels, y=electrons7)
        self._plot_item_8.setData(x=channels, y=electrons8)
       
        # Add y-axis labels 
        self.ui.graphicsView_1.setLabel("left", "Electrons")
        self.ui.graphicsView_2.setLabel("left", "Electrons")
        self.ui.graphicsView_3.setLabel("left", "Electrons")
        self.ui.graphicsView_4.setLabel("left", "Electrons")
        self.ui.graphicsView_5.setLabel("left", "Electrons")
        self.ui.graphicsView_6.setLabel("left", "Electrons")
        self.ui.graphicsView_7.setLabel("left", "Electrons")
        self.ui.graphicsView_8.setLabel("left", "Electrons")

        # Add error bars
        err = np.full(64,2)
        self._error_bars_1.setData(x=channels, y=electrons1, top=err, bottom=err)
        self._error_bars_2.setData(x=channels, y=electrons2, top=err, bottom=err)
        self._error_bars_3.setData(x=channels, y=electrons3, top=err, bottom=err)
        self._error_bars_4.setData(x=channels, y=electrons4, top=err, bottom=err)
        self._error_bars_5.setData(x=channels, y=electrons5, top=err, bottom=err)
        self._error_bars_6.setData(x=channels, y=electrons6, top=err, bottom=err)
        self._error_bars_7.setData(x=channels, y=electrons7, top=err, bottom=err)
        self._error_bars_8.setData(x=channels, y=electrons8, top=err, bottom=err)

    def update_asic_LET(self):
        # Get Rogue ADC counts
        counts1 = self._root.AsicSampleProcessor.ASIC0Sig.get()
        counts2 = self._root.AsicSampleProcessor.ASIC1Sig.get()
        counts3 = self._root.AsicSampleProcessor.ASIC2Sig.get()
        counts4 = self._root.AsicSampleProcessor.ASIC3Sig.get()
        counts5 = self._root.AsicSampleProcessor.ASIC4Sig.get()
        counts6 = self._root.AsicSampleProcessor.ASIC5Sig.get()
        counts7 = self._root.AsicSampleProcessor.ASIC6Sig.get()
        counts8 = self._root.AsicSampleProcessor.ASIC7Sig.get()

        # Compute electrons
        rng = np.random.default_rng()
        LET1 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        LET2 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        LET3 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        LET4 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        LET5 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        LET6 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        LET7 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
        LET8 = np.full(64, rng.integers(low=0.9e+06, high=1.1e+06))
 
        # Update plot items
        channels = np.arange(1, 65, 1)
        self._plot_item_1.setData(x=channels, y=LET1)
        self._plot_item_2.setData(x=channels, y=LET2)
        self._plot_item_3.setData(x=channels, y=LET3)
        self._plot_item_4.setData(x=channels, y=LET4)
        self._plot_item_5.setData(x=channels, y=LET5)
        self._plot_item_6.setData(x=channels, y=LET6)
        self._plot_item_7.setData(x=channels, y=LET7)
        self._plot_item_8.setData(x=channels, y=LET8)
       
        # Add y-axis labels 
        self.ui.graphicsView_1.setLabel("left", "LET")
        self.ui.graphicsView_2.setLabel("left", "LET")
        self.ui.graphicsView_3.setLabel("left", "LET")
        self.ui.graphicsView_4.setLabel("left", "LET")
        self.ui.graphicsView_5.setLabel("left", "LET")
        self.ui.graphicsView_6.setLabel("left", "LET")
        self.ui.graphicsView_7.setLabel("left", "LET")
        self.ui.graphicsView_8.setLabel("left", "LET")

        # Add error bars
        err = np.full(64,2)
        self._error_bars_1.setData(x=channels, y=LET1, top=err, bottom=err)
        self._error_bars_2.setData(x=channels, y=LET2, top=err, bottom=err)
        self._error_bars_3.setData(x=channels, y=LET3, top=err, bottom=err)
        self._error_bars_4.setData(x=channels, y=LET4, top=err, bottom=err)
        self._error_bars_5.setData(x=channels, y=LET5, top=err, bottom=err)
        self._error_bars_6.setData(x=channels, y=LET6, top=err, bottom=err)
        self._error_bars_7.setData(x=channels, y=LET7, top=err, bottom=err)
        self._error_bars_8.setData(x=channels, y=LET8, top=err, bottom=err)

    def updatePlots(self):
        #print('Update the plots ...\n')

        # Read current plot settings and update plots
        photons_checkbox   = self.ui.PyDMCheckbox_photons
        electrons_checkbox = self.ui.PyDMCheckbox_electrons
        LET_checkbox       = self.ui.PyDMCheckbox_LET

        # Depending on the configuration, update the curves with the appropriate counts
        if photons_checkbox.isChecked():
            # Add labels, legend and update photon plots
            self.update_asic_photons()
        elif electrons_checkbox.isChecked():
            # Add labels, legend and update electron plots
            self.update_asic_electrons()
        elif LET_checkbox.isChecked():
            # Add labels, legend and update LET plots
            self.update_asic_LET()

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
         self.ui.graphicsView_1.clear()
         self.ui.graphicsView_2.clear()
         self.ui.graphicsView_3.clear()
         self.ui.graphicsView_4.clear()
         self.ui.graphicsView_5.clear()
         self.ui.graphicsView_6.clear()
         self.ui.graphicsView_7.clear()
         self.ui.graphicsView_8.clear()

    def ui_filename(self):
        # Point to the UI file
        return 'ui/assertViewerPyQtGraph_Particle.ui'

    def ui_filepath(self):
        # Return the full path to the UI file
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())
