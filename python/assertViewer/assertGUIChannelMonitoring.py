#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : Configuration file for ASSERT channel display
#-----------------------------------------------------------------------------
# Borrowed from ePixGUI.py (ePixViewer, https://github.com/slaclab/ePixViewer)

import os
import pydm
import numpy as np
import pyqtgraph as pg
from pydm.widgets import PyDMLineEdit, PyDMLabel, PyDMImageView
from qtpy.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout, QSpacerItem, QSizePolicy

import rogue
import pyrogue as pr

def runChannelDisplay(dataReceiver,serverList='localhost:9090',port='9090',root=None,
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
    macrosA['port' ] = port
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
        self.sizeX = macros['sizeX']
        self.sizeY = macros['sizeY']
        self._asics = 8
        self._channels = 64
        self._port = macros['port']
        self.connect_rogue_root()
        self.init_colorbar()
        self.init_crosshair()
        self.setup_main_tab()
        self.set_image_channels()
        self.enable_mouse_cursor()
        
    def connect_rogue_root(self):
        with pr.interfaces.VirtualClient(addr="localhost",port=int(self._port)) as client:
        
           # Get the reference to the root node
           self._root = client.root
        
           # Get a variable value with a read, this returns the native value
           ret = self._root.RogueVersion.get()
           #print(f"Version = {ret}")

    def init_colorbar(self):
        for i in np.arange(1,self._asics+1):
            setattr(self, f'self.img_item_{i}', getattr(self.ui, f'PyDMImageView_{i}').getImageItem())
            setattr(self, f'self.colorbar_{i}', getattr(self.ui, f'PyDMImageView_{i}').getView().addColorBar(getattr(self,f'self.img_item_{i}'),colorMap='inferno',values=(int(self.ui.PyDMLineEdit_2.text()), int(self.ui.PyDMLineEdit_3.text())),label='ADC Counts'))

    def init_crosshair(self):
        for i in np.arange(1,self._asics+1):
            v_name = f'_v_line_img{i}'
            h_name = f'_h_line_img{i}'
            v_val  = pg.InfiniteLine(angle=90, movable=False, pen='g')
            h_val  = pg.InfiniteLine(angle=0,  movable=False, pen='g')
            setattr(self, v_name, v_val)
            setattr(self, h_name, h_val)

        for i in np.arange(1,self._asics+1):
            getattr(self.ui, f'PyDMImageView_{i}').getView().addItem(getattr(self, f'_v_line_img{i}'), ignoreBounds=False)
            getattr(self.ui, f'PyDMImageView_{i}').getView().addItem(getattr(self, f'_h_line_img{i}'), ignoreBounds=False)
        
        self.clear_crosshair()

    def clear_crosshair(self):
        for i in np.arange(1,self._asics+1):
            getattr(self, f'_v_line_img{i}').hide()
            getattr(self, f'_h_line_img{i}').hide()

    def update_crosshair(self, x, y=20, sensor=1):
        getattr(self, f'_v_line_img{sensor}').setPos(x)
        getattr(self, f'_h_line_img{sensor}').setPos(y)
        getattr(self, f'_v_line_img{sensor}').show()
        getattr(self, f'_h_line_img{sensor}').show()

    def setup_main_tab(self):
        self.ui.PyDMLineEdit_1.setChannel(f'{self._dataReceiver}.ASIC0FrameCnt')

        self.ui.PyDMLineEdit_2.setChannel(f'{self._dataReceiver}.MinContrast')
        self.ui.PyDMLineEdit_3.setChannel(f'{self._dataReceiver}.MaxContrast')

        self.ui.PyDMLineEdit_4.setChannel(f'{self._dataReceiver}.MinContrast')
        self.ui.PyDMLineEdit_4.textChanged.connect(self.updateColorMapLimits)

        self.ui.PyDMLineEdit_5.setChannel(f'{self._dataReceiver}.MaxContrast')
        self.ui.PyDMLineEdit_5.textChanged.connect(self.updateColorMapLimits)

        self.ui.PyDMLineEdit_8.setChannel(f'{self._dataReceiver}.BinsStart')
        self.ui.PyDMLineEdit_9.setChannel(f'{self._dataReceiver}.BinsStop')
        self.ui.PyDMLineEdit_10.setChannel(f'{self._dataReceiver}.NumBins')

        self.ui.PyDMLineEdit_11.setChannel(f'{self._dataReceiver}.BinsStart')
        self.ui.PyDMLineEdit_11.textChanged.connect(self.update_histogram_params)

        self.ui.PyDMLineEdit_12.setChannel(f'{self._dataReceiver}.BinsStop')
        self.ui.PyDMLineEdit_12.textChanged.connect(self.update_histogram_params)

        self.ui.PyDMLineEdit_13.setChannel(f'{self._dataReceiver}.NumBins')
        self.ui.PyDMLineEdit_13.textChanged.connect(self.update_histogram_params)

    def set_image_channels(self):
        #self.ui.PyDMImageView_1.setImageChannel(f"{self._dataReceiver}.ASIC0Image")
        #self.ui.PyDMImageView_2.setImageChannel(f"{self._dataReceiver}.ASIC1Image")
        #self.ui.PyDMImageView_3.setImageChannel(f"{self._dataReceiver}.ASIC2Image")
        #self.ui.PyDMImageView_4.setImageChannel(f"{self._dataReceiver}.ASIC3Image")
        #self.ui.PyDMImageView_5.setImageChannel(f"{self._dataReceiver}.ASIC4Image")
        #self.ui.PyDMImageView_6.setImageChannel(f"{self._dataReceiver}.ASIC5Image")
        #self.ui.PyDMImageView_7.setImageChannel(f"{self._dataReceiver}.ASIC6Image")
        #self.ui.PyDMImageView_8.setImageChannel(f"{self._dataReceiver}.ASIC7Image")
        self.updateColorMapLimits()
        for i in np.arange(1,self._asics+1):
            getattr(self.ui, f'PyDMImageView_{i}').setImageChannel(f'{self._dataReceiver}.ASIC{i-1}Image')

        self.ui.pushButton.clicked.connect(self.updateDisplay)

    def enable_mouse_cursor(self):
        # Enable mouse clicks to extract image coordinates
        #self.ui.PyDMImageView_1.scene.sigMouseClicked.connect(self.clickProcessImage1)
        #self.ui.PyDMImageView_2.scene.sigMouseClicked.connect(self.clickProcessImage2)
        #self.ui.PyDMImageView_3.scene.sigMouseClicked.connect(self.clickProcessImage3)
        #self.ui.PyDMImageView_4.scene.sigMouseClicked.connect(self.clickProcessImage4)
        #self.ui.PyDMImageView_5.scene.sigMouseClicked.connect(self.clickProcessImage5)
        #self.ui.PyDMImageView_6.scene.sigMouseClicked.connect(self.clickProcessImage6)
        #self.ui.PyDMImageView_7.scene.sigMouseClicked.connect(self.clickProcessImage7)
        #self.ui.PyDMImageView_8.scene.sigMouseClicked.connect(self.clickProcessImage8)
        for i in np.arange(1,self._asics+1):
            getattr(self.ui, f'PyDMImageView_{i}').scene.sigMouseClicked.connect(getattr(self, f'clickProcessImage{i}'))

    def updateColorMapLimits(self):
        #minContrast = int(self.ui.PyDMLineEdit_2.displayText())
        #maxContrast = int(self.ui.PyDMLineEdit_3.displayText())
        minContrast = int(self.ui.PyDMLineEdit_4.text())
        maxContrast = int(self.ui.PyDMLineEdit_5.text())
        #self.ui.PyDMImageView_1.setColorMapLimits(minContrast, maxContrast)
        #self.ui.PyDMImageView_2.setColorMapLimits(minContrast, maxContrast)
        #self.ui.PyDMImageView_3.setColorMapLimits(minContrast, maxContrast)
        #self.ui.PyDMImageView_4.setColorMapLimits(minContrast, maxContrast)
        #self.ui.PyDMImageView_5.setColorMapLimits(minContrast, maxContrast)
        #self.ui.PyDMImageView_6.setColorMapLimits(minContrast, maxContrast)
        #self.ui.PyDMImageView_7.setColorMapLimits(minContrast, maxContrast)
        #self.ui.PyDMImageView_8.setColorMapLimits(minContrast, maxContrast)

        for i in np.arange(1,self._asics+1):
            getattr(self.ui, f'PyDMImageView_{i}').setColorMapLimits(minContrast, maxContrast)

        for i in np.arange(1,self._asics+1):
            #getattr(self, f'self.colorbar_{i}').setLevels(values=(int(self.ui.PyDMLineEdit_4.text()), int(self.ui.PyDMLineEdit_5.text())))
            getattr(self, f'self.colorbar_{i}').setLevels(values=(minContrast, maxContrast))

    def updateDisplay(self):
        #self.ui.PyDMImageView_1.redrawImage()
        #self.ui.PyDMImageView_2.redrawImage()
        #self.ui.PyDMImageView_3.redrawImage()
        #self.ui.PyDMImageView_4.redrawImage()
        #self.ui.PyDMImageView_5.redrawImage()
        #self.ui.PyDMImageView_6.redrawImage()
        #self.ui.PyDMImageView_7.redrawImage()
        #self.ui.PyDMImageView_8.redrawImage()
        self.updateColorMapLimits()
        for i in np.arange(1,self._asics+1):
            getattr(self.ui, f'PyDMImageView_{i}').redrawImage()

    # def setTimeSpan(self):
    #     self.ui.PyDMTimePlot.setTimeSpan(int(self.ui.lineEdit.text()))

    def clickProcessImage1(self, event):
        pos = self.ui.PyDMImageView_1.getView().getViewBox().mapSceneToView(event.scenePos())
        self.perform_error_checking(pos, 1)

    def clickProcessImage2(self, event):
        pos = self.ui.PyDMImageView_2.getView().getViewBox().mapSceneToView(event.scenePos())
        self.perform_error_checking(pos, 2)

    def clickProcessImage3(self, event):
        pos = self.ui.PyDMImageView_3.getView().getViewBox().mapSceneToView(event.scenePos())
        self.perform_error_checking(pos, 3)

    def clickProcessImage4(self, event):
        pos = self.ui.PyDMImageView_4.getView().getViewBox().mapSceneToView(event.scenePos())
        self.perform_error_checking(pos, 4)

    def clickProcessImage5(self, event):
        pos = self.ui.PyDMImageView_5.getView().getViewBox().mapSceneToView(event.scenePos())
        self.perform_error_checking(pos, 5)

    def clickProcessImage6(self, event):
        pos = self.ui.PyDMImageView_6.getView().getViewBox().mapSceneToView(event.scenePos())
        self.perform_error_checking(pos, 6)

    def clickProcessImage7(self, event):
        pos = self.ui.PyDMImageView_7.getView().getViewBox().mapSceneToView(event.scenePos())
        self.perform_error_checking(pos, 7)

    def clickProcessImage8(self, event):
        pos = self.ui.PyDMImageView_8.getView().getViewBox().mapSceneToView(event.scenePos())
        self.perform_error_checking(pos, 8)

    def perform_error_checking(self, pos, sensor):
        if int(pos.x()) >= self._channels:
            x = self._channels - 1
        elif int(pos.x()) < 0:
            x = 0
        else:
            x = int(pos.x())

        self.clear_crosshair()
        self.update_crosshair(x,sensor=sensor)

        self.ui.PyDMLineEdit_6.setText(str(x))
        self.ui.PyDMLineEdit_7.setText(str(sensor))
        
        self.update_channel_timeplot(sensor,x)
        self.update_channel_histogram(sensor,x)
        self.update_all_channels_plot(sensor)

    def update_channel_timeplot(self, sensor, channel):
        self.ui.PyDMWaveformPlot_1.clearCurves()
        self.ui.PyDMWaveformPlot_1.addChannel(y_channel = f'{self._dataReceiver}.ASIC{sensor-1}CntHist{channel}',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts")

    def update_channel_histogram(self, sensor, channel):
        bin_start = self._root.AsicSampleProcessor.BinsStart.get()
        bin_stop  = self._root.AsicSampleProcessor.BinsStop.get()
        num_bins  = self._root.AsicSampleProcessor.NumBins.get()
        vals = getattr(self._root.AsicSampleProcessor, f'ASIC{sensor-1}CntHist{channel}').get()
        y, x = np.histogram(vals, bins=np.linspace(bin_start, bin_stop, num_bins))
        self._root.AsicSampleProcessor.Bins.set(x, write = True)
        self._root.AsicSampleProcessor.Frequencies.set(y, write = True)
        self.ui.PyDMWaveformPlot_2.clearCurves()
        self.ui.PyDMWaveformPlot_2.addChannel(y_channel = f'{self._dataReceiver}.Frequencies',x_channel = f'{self._dataReceiver}.Bins',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "Frequencies") 

    def update_all_channels_plot(self, sensor):
        self.ui.PyDMWaveformPlot_3.clearCurves()
        self.ui.PyDMWaveformPlot_3.addChannel(y_channel = f'{self._dataReceiver}.ASIC{sensor-1}Sig',x_channel = f'{self._dataReceiver}.IndexChannels',plot_style = "Line",color = "orange",lineWidth = 3,yAxisName = "ADC Counts") 

    def update_histogram_params(self):
        bin_start = int(self.ui.PyDMLineEdit_11.text())
        bin_stop  = int(self.ui.PyDMLineEdit_12.text())
        num_bins  = int(self.ui.PyDMLineEdit_13.text())
        self._root.AsicSampleProcessor.BinsStart.set(bin_start, write = True)
        self._root.AsicSampleProcessor.BinsStop.set(bin_stop, write = True)
        self._root.AsicSampleProcessor.NumBins.set(num_bins, write = True)
        self.update_channel_histogram(int(self.ui.PyDMLineEdit_7.text()),int(self.ui.PyDMLineEdit_6.text()))
 
    def ui_filename(self):
        # Point to the UI file
        return 'ui/assertViewerPyDM_StripMonitoring.ui'

    def ui_filepath(self):
        # Return the full path to the UI file
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), self.ui_filename())
