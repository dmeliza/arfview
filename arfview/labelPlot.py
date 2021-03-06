from PySide.QtGui import *
from PySide.QtCore import *
import sys
import pyqtgraph as pg
import numpy as np
import arfview.utils as utils
import h5py
import arf
import pyqtgraph.functions as fn

class labelRegion(pg.LinearRegionItem):
    '''Labeled region on label plot'''
    def __init__(self, name, start, stop, parent, *args, **kwargs):
        super(labelRegion, self).__init__([start, stop], *args, **kwargs)
        parent.addItem(self)        
        vb = parent.getViewBox()
        self.text = pg.TextItem(name)
        vb.addItem(self.text)
        self.position_text_y()
        self.position_text_x()
        vb.sigXRangeChanged.connect(self.position_text_x)
        vb.sigYRangeChanged.connect(self.position_text_y)
        self.sigRegionChanged.connect(self.position_text_x)
        self.setMovable(False)
        
    def position_text_y(self):
        yrange=self.getViewBox().viewRange()[1]
        self.text.setY(np.mean(yrange))

    def position_text_x(self):
        xmin, xmax = self.getViewBox().viewRange()[0]
        if xmin <= self.getRegion()[0] <= xmax:
            self.text.setX(self.getRegion()[0])
        elif self.getRegion()[0] < xmin < self.getRegion()[1]:
            self.text.setX(xmin)

            
class labelPlot(pg.PlotItem):
    '''Interactive plot for making and displaying labels'''
    
    def __init__(self, lbl, *args, **kwargs):
        super(labelPlot, self).__init__(*args, **kwargs)
        if not utils.is_complex_event(lbl):           
            raise TypeError("Argument must be complex event dataset")
        elif lbl.maxshape != (None,):
            raise TypeError("Argument must have maxshape (None,)")
        else:
             self.lbl = lbl
        self.installEventFilter(self)
        self.getViewBox().enableAutoRange(enable=False)
        self.key = None
        self.dclickedRegion = None
        self.activeLabel = None
        if self.lbl.attrs['units'] == 'ms':
            self.scaling_factor = 1000
        elif self.lbl.attrs['units'] == 'samples':
            self.scaling_factor = self.lbl.attrs['sampling_rate']
        else:
            self.scaling_factor = 1
        for tup in self.lbl:
                self.plot_complex_event(tup)

        self.setMouseEnabled(y=False)

    def plot_complex_event(self, complex_event, with_text=True):
        '''Plots a single event'''
        name = complex_event['name']
        start = complex_event['start'] / self.scaling_factor
        stop = complex_event['stop'] / self.scaling_factor
        region = labelRegion(name, start, stop, self)
        
        return region
        
    def sort_lbl(self):
        '''Sorts lbl dataset by start time'''
        data = self.lbl[:]
        data.sort(order='start')
        self.lbl[:] = data
        
    def keyPressEvent(self, event):
        if event.text().isalpha():
            self.key = event.text().upper()

    def keyReleaseEvent(self, event):
        if event.text().upper() == self.key:
            self.key = None
            
    def mouseClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos=self.getViewBox().mapSceneToView(event.scenePos())
            t = pos.x() * self.scaling_factor
            if self.key and not self.activeLabel:
                arf.append_data(self.lbl, (self.key, t, t))
                self.activeLabel = self.plot_complex_event(self.lbl[-1]) 
                if event.modifiers() != Qt.ShiftModifier:
                    self.sort_lbl()
                    self.activeLabel = None
            elif self.activeLabel:
                if t >= self.lbl[-1]['start']:
                    self.lbl[-1] = (self.lbl[-1]['name'], self.lbl[-1]['start'], t)
                else:
                    self.lbl[-1] =  (self.lbl[-1]['name'], t, self.lbl[-1]['stop'])

                new_region = (np.array([self.lbl[-1]['start'], self.lbl[-1]['stop']])/ 
                              self.scaling_factor)

                self.activeLabel.setRegion(new_region)
                self.activeLabel = None
                self.sort_lbl()
    
        
