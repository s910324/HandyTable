
import os
import sys
import math
import numpy           as np
import pyqtgraph       as pg
from   PyQt5.QtWidgets import *
from   PyQt5.QtCore    import *
from   PyQt5.QtGui     import *
from   pyqtgraph.Qt    import QtCore, QtGui

sys.path.append("../")
from uiplus import HBox, VBox, BoxLayout

class DistributionWidget(QWidget):
    valueSelected = pyqtSignal(object)
    def __init__(self,  parent=None):
        super(DistributionWidget, self).__init__(parent)
        # pg.setConfigOption('background', '#dddddd')
        pg.setConfigOption('foreground', '#656565')
        x = np.arange(1000)
        y = np.random.normal(size=(3, 1000))
        plot_widget = pg.PlotWidget()
        plot_widget2 = pg.PlotWidget(title = 'pyqtgraph example: Histogram')
        
        


        vals = np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)])

        plot_item   = plot_widget.getPlotItem()
        plot_item2  = plot_widget2.getPlotItem()
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
        # view_box.setYLink(plot_item2.getViewBox())
        view_box.setXLink(plot_item2.getViewBox())
        

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

        y,x = np.histogram(vals, bins=np.linspace(-3, 8, 40))

        plot_widget.plot(x, y, stepMode=True, fillLevel=0, brush=(0,0,255,150))

        y = pg.pseudoScatter(vals, spacing=0.15)
        plot_widget2.plot(vals, y, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        
        self.setLayout(HBox(plot_widget, plot_widget2))



        label = pg.TextItem()
        plot_item.addItem(label)
        def mouseMoved(pos):
            if plot_item.sceneBoundingRect().contains(pos):
                point = view_box.mapSceneToView(pos)
                label.setText("(%0.1f, %0.1f)" % (point.x(), point.y()))
                label.setPos(QPointF(point.x(), point.y() + 3))
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