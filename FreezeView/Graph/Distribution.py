
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
        # pg.setConfigOption('foreground', '#656565')
        x = np.arange(1000)
        y = np.random.normal(size=(3, 1000))
        plot_widget = pg.PlotWidget(title = 'pyqtgraph example: Histogram')
        plot_widget2 = pg.PlotWidget(title = 'pyqtgraph example: Histogram')
        plot_widget.setBackground(QColor("#dddddd"))
        


        vals = np.hstack([np.random.normal(size=500), np.random.normal(size=260, loc=4)])
        plot_widget.setLabel('right', '', units="", color='c', **{'font-size':'12pt', 'font':'Arial'})
        plot_widget.setLabel('top', '', units="", color='c', **{'font-size':'12pt'})
        plot_widget.setLabel('left', 'Current', units="A", color='c', **{'font-size':'10pt'})
        plot_widget.setLabel('bottom', 'Current', units="A", color='c', **{'font-size':'12pt'})
        
        plot_item   = plot_widget.getPlotItem()
        view_box    = plot_item.getViewBox()
        left_axis   = plot_item.getAxis('left')
        right_axis  = plot_item.getAxis('right')
        top_axis    = plot_item.getAxis('top')
        bottom_axis = plot_item.getAxis('bottom')
        
        default_label_style = {'font-size':'12', 'font-family':'Arial', 'color':'#656565'}
        default_tick_style  = {'showValues':  True, 'tickLength': -3, 'tickTextOffset':  5, 'tickFont':'Arial'}
        hidden_tick_style   = {'showValues': False, 'tickLength':  0, 'tickTextOffset':  5, 'tickFont':'Arial'}

        left_axis.setLabel(  'label text', units='V', **default_label_style)
        bottom_axis.setLabel('label text', units='V', **default_label_style)
        left_axis.setStyle(  **default_tick_style)
        right_axis.setStyle( **hidden_tick_style )
        top_axis.setStyle(   **hidden_tick_style )
        bottom_axis.setStyle(**default_tick_style)
        left_axis.setZValue(0)
        bottom_axis.setZValue(0)
        right_axis.setZValue(0)
        top_axis.setZValue(0)

        y,x = np.histogram(vals, bins=np.linspace(-3, 8, 40))

        plot_widget.plot(x, y, stepMode=True, fillLevel=0, brush=(0,0,255,150))

        y = pg.pseudoScatter(vals, spacing=0.15)
        plot_widget2.plot(vals, y, pen=None, symbol='o', symbolSize=5, symbolPen=(255,255,255,200), symbolBrush=(0,0,255,150))
        plot_widget.getPlotItem().getViewBox().setBackgroundColor(QColor("#ffffff"))
        self.setLayout(HBox(plot_widget, plot_widget2))



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