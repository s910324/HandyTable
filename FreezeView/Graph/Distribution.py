
import os
import sys
import math
import numpy           as np
import pandas          as pd
import pyqtgraph       as pg
from   PyQt5.QtWidgets import *
from   PyQt5.QtCore    import *
from   PyQt5.QtGui     import *
from   pyqtgraph.Qt    import QtCore, QtGui

sys.path.append("../")
sys.path.append("../../../AllmightDataProcesser/")
from uiplus   import HBox, VBox, BoxLayout
from allmight import  *

#distribution chart
    #spec line
    #multiple distribution
        #spacing between sub_charts

class DistributionWidget(QWidget):
    valueSelected = pyqtSignal(object)
    def __init__(self,  parent=None):
        super(DistributionWidget, self).__init__(parent)
        self._plot_widget1 = DistributionChartWidget()
        self._plot_widget2 = DistributionChartWidget()
        self._spec_h       = QLineEdit()
        self._spec_tgt     = QLineEdit()
        self._spec_l       = QLineEdit()
        self._pb1          = QPushButton("set")

        self._bar_width    = QLineEdit()
        self._pb2          = QPushButton("set")

        self._bar_offset   = QLineEdit()
        self._pb3          = QPushButton("set")

        self._pb4          = QPushButton("set")

        self.setLayout(
            VBox(
                HBox(self._plot_widget1),#, self._plot_widget2),
                HBox(self._spec_h, self._spec_tgt, self._spec_l, self._pb1),
                HBox(self._bar_width,  self._pb2),
                HBox(self._bar_offset, self._pb3),
                HBox(self._pb4)
                )
            )
        self._pb1.clicked.connect(self.setSpec)
        self._pb2.clicked.connect(self.setBarWidth)
        self._pb3.clicked.connect(self.setBarSpacing)
        self._pb4.clicked.connect(self.setCrosshair)


        csv = pd.read_csv(r'C:\Users\rawr\Downloads\MOCK_DATA (4).csv')
        s1 = Statistic(data = csv.iloc[:, 3], spec_high=30, spec_low=20)
        s2 = Statistic(data = csv.iloc[:, 2], spec_high=30, spec_low=20)
        s3 = Statistic(data = csv.iloc[:, 1], spec_high=30, spec_low=20)
        s4 = Statistic(data = csv.iloc[:, 0], spec_high=30, spec_low=20)
        self._plot_widget1.AddData(self.g(s1))
        self._plot_widget1.AddData(self.g(s2))
        self._plot_widget1.AddData(self.g(s3))
        self._plot_widget1.AddData(self.g(s4))

    def g(self, data):
        d    = (data.frequency_chart(scale = [15, 40, 1]))
        x, y = [ ix for ix, iy in d], [ iy for ix, iy in d]
        return x, y

    def setSpec(self):
        h = float(self._spec_h.text())
        t = float(self._spec_tgt.text())
        l = float(self._spec_l.text())
        self._plot_widget1.Spec = [l, t, h]

    def setBarWidth(self):
        w = float(self._bar_width.text())
        self._plot_widget1.BarWidth = w

    def setBarSpacing(self):
        s = float(self._bar_offset.text())
        self._plot_widget1.BarOffset = s
    
    def setCrosshair(self):
        self._plot_widget1.CrosshairVisible(not(self._plot_widget1._crosshair_visible))

class DistributionChartWidget(pg.PlotWidget):
    def __init__(self,  parent=None):
        super(DistributionChartWidget, self).__init__(parent)
        self._bar_width         = 1
        self._bar_offset        = 0
        self._charts            = []
        self._chart_data        = []
        self._auto_scale        = True
        self._spec_h            = None
        self._target            = None
        self._spec_l            = None
        self._spec_h_line_show  = False
        self._target_line_show  = False
        self._spec_l_line_show  = False      
        self._crosshair_visible = False        
        self._crosshair_label   = pg.TextItem(anchor = (0, 1))
        self._crosshair_hline   = pg.InfiniteLine(angle =  0, movable = False)
        self._crosshair_vline   = pg.InfiniteLine(angle = 90, movable = False)
        self._spec_h_line       = pg.InfiniteLine(angle = 90, movable = False)
        self._target_line       = pg.InfiniteLine(angle = 90, movable = False)
        self._spec_l_line       = pg.InfiniteLine(angle = 90, movable = False)     
        self._color_theme       = [(255, 6, 120, 100), (255, 172, 0, 100), (0, 189, 255, 100), (0, 80, 255, 100), (189, 0, 255, 100), (130, 130, 130, 100)]
        self._init_()
        self.CrosshairVisible()
    
    def _init_(self):
        self.ViewBoxColor    = "#ffffff"
        self.BackgroundColor = "#dddddd"
        default_label_style  = {'font-size':'12', 'font-family':'Arial', 'color':'#656565'}
        default_tick_style   = {'showValues':  True, 'tickLength': -3, 'tickTextOffset':  5, 'tickFont':'Arial'}
        hidden_tick_style    = {'showValues': False, 'tickLength':  0, 'tickTextOffset':  5, 'tickFont':'Arial'}

        for axis, label, tick in [(self.LeftAxis, default_label_style, default_tick_style), (self.BottomAxis, default_label_style, default_tick_style), (self.RightAxis, default_label_style, hidden_tick_style), (self.TopAxis, default_label_style, hidden_tick_style)]:
            axis.setZValue(0)
            axis.setLabel( '', units=None, **label)
            axis.setStyle(**tick)

        for axis in ['left', 'right', 'top', 'bottom']:
            self.PlotItem.showAxis(axis)

    def AddData(self, data):
        x, y  = data
        chart = pg.BarGraphItem(x=np.array(x), height=y, width=self._bar_width, brush = self._color_theme[len(self)], x_offset = 0)
        self.addItem(chart)
        self._charts.append(chart)
        self.AxisRange = [None, None]
        self.CrosshairVisible(self._crosshair_visible)
        self.Spec              = 20, 27, 34
        self.SpecHLineVisible  = True
        self.TargetLineVisible = True
        self.SpecLLineVisible  = True
        return chart

    
    def __len__(self):
        return len(self._charts)
    

    @property
    def BarWidth(self):
        return self._bar_width

    @BarWidth.setter
    def BarWidth(self, width):
        if  (0 < float(width) <= 1):
            self._bar_width = width
            for chart in self._charts:
                chart.setOpts(width= width)

    @property
    def BarOffset(self):
        return self._bar_offset

    @BarOffset.setter
    def BarOffset(self, offset):
        if  (0 < float(offset) <= 1):
            self._bar_offset = offset
            for index, chart in enumerate(self._charts):
                x, old_offset, new_offset = chart.opts['x'], chart.opts['x_offset'], (self._bar_offset * index)
                delta                     = new_offset - old_offset
                chart.setOpts(x = np.array(x) + delta, x_offset = new_offset)

    def CrosshairVisible(self, visible = True):
        self._crosshair_visible = visible
        if (self.Charts and visible):
            region = pg.LinearRegionItem()
            proxy  = pg.SignalProxy(self.PlotItem.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
            self.PlotItem.scene().sigMouseMoved.connect(self.mouseMoved)
            self.PlotItem.addItem(self._crosshair_label)
            for line in [self._crosshair_hline, self._crosshair_vline]:
                line.setPen(pg.mkPen(color = pg.mkColor("#aaaaaa"), style = Qt.DotLine))
                self.PlotItem.addItem(line, ignoreBounds=True)
        else:
            for item in [self._crosshair_label, self._crosshair_hline, self._crosshair_vline]:
                self.PlotItem.removeItem(item)
        

    def mouseMoved(self, pos):
        if self.ViewBox.sceneBoundingRect().contains(pos) and self._crosshair_visible:
            point = self.ViewBox.mapSceneToView(pos)
            self._crosshair_label.setText("(%0.1f, %0.1f)" % (point.x(), point.y()))
            self._crosshair_label.setPos(QPointF(point.x(), point.y()))
            self._crosshair_vline.setPos(point.x())
            self._crosshair_hline.setPos(point.y())
    
    def updateRegion(self, window, viewRange):
        region.setRegion(viewRange[0])

    @property
    def Spec(self):
        return self._spec_l, self._target, self._spec_l

    @Spec.setter
    def Spec(self, spec_list):
        if (len(spec_list) == 3 and all([type(item) in [int, float, type(None)] for item in spec_list])):
            self._spec_l, self._target, self._spec_h = spec_list
            self.SpecHLineVisible  = self._spec_h_line_show
            self.TargetLineVisible = self._target_line_show
            self.SpecLLineVisible  = self._spec_l_line_show
        else:
            raise TypeError("item %s with object type %s is not supported) " % (spec_list, type(spec_list))) 


    @property
    def SpecHLineVisible(self):
        return self._spec_h_line_show
    
    @SpecHLineVisible.setter
    def SpecHLineVisible(self, visible):
        if visible in [True, False]:
            self._spec_h_line_show = visible
            if (not (self._spec_h == None) and (visible == True)):
                self.PlotItem.addItem(self._spec_h_line, ignoreBounds=True)
                self._spec_h_line.setPos(self._spec_h)

    @property
    def TargetLineVisible(self):
        return self._target_line_show
    
    @TargetLineVisible.setter
    def TargetLineVisible(self, visible):
        if visible in [True, False]:
            self._target_line_show = visible
            if (not (self._target == None) and (visible == True)):
                self.PlotItem.addItem(self._target_line, ignoreBounds=True)
                self._target_line.setPos(self._target)
    @property
    def SpecLLineVisible(self):
        return self._spec_l_line_show
    
    @SpecLLineVisible.setter
    def SpecLLineVisible(self, visible):
        if visible in [True, False]:
            self._spec_l_line_show = visible
            if (not (self._spec_l == None) and (visible == True)):
                self.PlotItem.addItem(self._spec_l_line, ignoreBounds=True)
                self._spec_l_line.setPos(self._spec_l)

    @property
    def Charts(self):
        return self._charts

    @property
    def PlotItem(self):
        return self.getPlotItem()

    @property
    def ViewBox(self):
        return self.plotItem.getViewBox()

    @property
    def LeftAxis(self):
        return self.PlotItem.getAxis('left')

    @property
    def RightAxis(self):
        return self.PlotItem.getAxis('right')

    @property
    def TopAxis(self):
        return self.PlotItem.getAxis('top')
    
    @property
    def BottomAxis(self):
        return self.PlotItem.getAxis('bottom')

    @property
    def AxisRange(self):
        return self.XAxisRange, self.YAxisRange

    @AxisRange.setter
    def AxisRange(self, xy_range):
        try:
            xy_range         = [None, None] if xy_range == None else xy_range
            x_range, y_range = xy_range
            self.XAxisRange  = x_range
            self.YAxisRange  = y_range
        except:
            raise TypeError("item %s with object type %s is not supported) " % (xy_range, type(xy_range)))      

    @property
    def XAxisRange(self):
        [x_min, x_max], [y_min, y_max] = self.ViewBox.viewRange()
        return [x_min, x_max]

    @XAxisRange.setter
    def XAxisRange(self, x_range):
        try:
            x_min, x_max = None, None
            if x_range == None:
                self.ViewBox.autoRange(padding = 0, items = self.Charts)
                self.ViewBox.disableAutoRange('x')      
                [x_min, x_max], _ = self.ViewBox.viewRange()
                x_spam            = (x_max - x_min) * 0.05
                x_min, x_max      = (x_min if (x_min - 0) < 0.2  else x_min - x_spam),  x_max + x_spam
            else:            
                x_min, x_max = x_range
            self.ViewBox.setXRange(float(x_min), float(x_max), padding = 0)
        except:
            raise TypeError("item %s with object type %s is not supported) " % (x_range, type(x_range)))

    @property
    def YAxisRange(self):
        [x_min, x_max], [y_min, y_max] = self.ViewBox.viewRange()
        return [y_min, y_max]

    @YAxisRange.setter
    def YAxisRange(self, y_range):
        try:
            y_min, y_max = None, None
            if y_range == None:
                self.ViewBox.autoRange(padding = 0, items = self.Charts)
                self.ViewBox.disableAutoRange('x')      
                _, [y_min, y_max] = self.ViewBox.viewRange()
                y_spam            = (y_max - y_min) * 0.05
                y_min, y_max      = (y_min if (y_min - 0) < 0.2  else y_min - y_spam),  y_max + y_spam
            else:            
                y_min, y_max = y_range            
            self.ViewBox.setYRange(float(y_min), float(y_max), padding = 0)
        except:
            raise TypeError("item %s with object type %s is not supported) " % (y_range, type(y_range)))
    

    @property
    def ViewBoxColor(self):
        return self.ViewBox.state['background'].name()

    @ViewBoxColor.setter
    def ViewBoxColor(self, color):
        self.ViewBox.setBackgroundColor(QColor(color))
 
    @property
    def BackgroundColor(self):
        return self.backgroundBrush().color().name()

    @BackgroundColor.setter
    def BackgroundColor(self, color):
        self.setBackground(QColor(color))


if __name__ == "__main__":
    def Debugger():

        app  = QApplication(sys.argv)
        form = DistributionWidget()
        form.show()
        app.exec_()

    def tester1():
        import pyqtgraph.examples
        pyqtgraph.examples.run()   

    def tester2():
        print(Type(NoneType))

    Debugger()    
    # tester1()
    # tester2()