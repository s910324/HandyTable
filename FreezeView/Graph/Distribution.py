
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


class DistributionWidget(QWidget):
    valueSelected = pyqtSignal(object)
    def __init__(self,  parent=None):
        super(DistributionWidget, self).__init__(parent)
        # pg.setConfigOption('background', '#dddddd')
        pg.setConfigOption('foreground', '#656565')
        csv = pd.read_csv(r'C:\Users\rawr\Downloads\MOCK_DATA (4).csv')
        s1 = Statistic(data = csv.iloc[:, 3], spec_high=30, spec_low=20)
        s2 = Statistic(data = csv.iloc[:, 2], spec_high=30, spec_low=20)

        def g(data):
            d    = (data.frequency_chart(scale = [15, 40, 1]))
            x, y = [ ix for ix, iy in d], [ iy for ix, iy in d]
            return x, y


        plot_widget  = pg.PlotWidget()

        plot_item   = plot_widget.getPlotItem()
        view_box    = plot_item.getViewBox()
        title_item  = plot_item.titleLabel
        left_axis   = plot_item.getAxis('left')
        right_axis  = plot_item.getAxis('right')
        top_axis    = plot_item.getAxis('top')
        bottom_axis = plot_item.getAxis('bottom')

        plot_widget.showAxis('right',  show=True)
        plot_widget.showAxis('top',    show=True)
        plot_widget.showAxis('left',   show=True)
        plot_widget.showAxis('bottom', show=True)

        plot_widget.showLabel('right',  show=True)
        plot_widget.showLabel('top',    show=True)
        plot_widget.showLabel('left',   show=True)
        plot_widget.showLabel('bottom', show=True)
        title = pg.TextItem("123")
        title.setAnchor(QPoint(6, 6))
        plot_item.addItem(title)


        left_axis.setZValue(0)
        bottom_axis.setZValue(0)
        right_axis.setZValue(0)
        top_axis.setZValue(0)
        
        plot_widget.setBackground(QColor("#dddddd"))
        view_box.setBackgroundColor(QColor("#ffffff"))


        default_label_style  = {'font-size':'12', 'font-family':'Arial', 'color':'#656565'}
        default_tick_style   = {'showValues':  True, 'tickLength': -3, 'tickTextOffset':  5, 'tickFont':'Arial'}
        hidden_tick_style    = {'showValues': False, 'tickLength':  0, 'tickTextOffset':  5, 'tickFont':'Arial'}


        left_axis.setLabel(  'label text', units='V', **default_label_style)
        bottom_axis.setLabel('label text', units='V', **default_label_style)
        top_axis.setLabel(       **default_label_style)
        right_axis.setLabel( '', **default_label_style)

        left_axis.setStyle(**default_tick_style)
        bottom_axis.setStyle(**default_tick_style)
        top_axis.setStyle(**hidden_tick_style)
        right_axis.setStyle(**hidden_tick_style)


        x, y = g(s1)
        j = pg.BarGraphItem(x=x, height=y, width=0.5, brush=(253,6,200, 100))
        plot_widget.addItem(j)
        x, y = g(s2)
        k = pg.BarGraphItem(x=np.array(x)+0.5, height=y, width=0.5, brush=(6,184,253, 100))
        plot_widget.addItem(k)

        view_box.autoRange(padding = 0, items = [j, k])
        view_box.disableAutoRange('xy')      
        x_range, y_range = view_box.viewRange()
        x_min, x_max     = x_range
        y_min, y_max     = y_range
        y_spam           = (y_max - y_min) * 0.05
        y_min, y_max     = (y_min if (y_min - 0) < 0.2  else y_min - y_spam),  y_max + y_spam

        view_box.setXRange(x_min, x_max, padding = 0)
        view_box.setYRange(y_min, y_max, padding = 0)

        
        self.setLayout(HBox(plot_widget))#, plot_widget2))



        label = pg.TextItem(anchor = (0, 1))
        plot_item.addItem(label)
        def mouseMoved(pos):
            if view_box.sceneBoundingRect().contains(pos):
                point = view_box.mapSceneToView(pos)
                label.setText("(%0.1f, %0.1f)" % (point.x(), point.y()))
                label.setPos(QPointF(point.x(), point.y()))
                vLine.setPos(point.x())
                hLine.setPos(point.y())
        
        def updateRegion(window, viewRange):
            region.setRegion(viewRange[0])

        region = pg.LinearRegionItem()
        vLine  = pg.InfiniteLine(angle=90, movable=False)
        hLine  = pg.InfiniteLine(angle=0,  movable=False)
        proxy  = pg.SignalProxy(plot_item.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
        plot_item.addItem(vLine, ignoreBounds=True)
        plot_item.addItem(hLine, ignoreBounds=True)
        plot_item.scene().sigMouseMoved.connect(mouseMoved)
        vLine.setPen(pg.mkPen(color = pg.mkColor("#aaaaaa"), style = Qt.DotLine))
        hLine.setPen(pg.mkPen(color = pg.mkColor("#aaaaaa"), style = Qt.DotLine))        

if __name__ == "__main__":
    def Debugger():

        app  = QApplication(sys.argv)
        form = DistributionWidget()
        # form = m()
        form.show()
        app.exec_()

    def tester():
        import pyqtgraph.examples
        pyqtgraph.examples.run()        

    Debugger()    
    # tester()