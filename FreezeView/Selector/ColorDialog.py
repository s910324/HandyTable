import os
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
import inspect
import numbers
import re
sys.path.append("../")
from uiplus import HBox, VBox, BoxLayout


class ColorSelector(QWidget):
    valueChanged = pyqtSignal(list)
    def __init__(self, parent=None):
        super(ColorSelector, self).__init__(parent)
        x, y  = 0, -18

        self._color_hex_list = [
            [ -90 + x,  -54 + y, '#008104'], [ -90 + x,  -36 + y, '#0F8100'], [ -90 + x,  -18 + y, '#278100'], [ -90 + x,    0 + y, '#408100'], [ -90 + x,   18 + y, '#5A8100'], [ -90 + x,   36 + y, '#718100'], [ -90 + x,   54 + y, '#817C00'], [ -75 + x,  -63 + y, '#008118'], 
            [ -75 + x,  -45 + y, '#00C507'], [ -75 + x,  -27 + y, '#1EC500'], [ -75 + x,   -9 + y, '#4BC500'], [ -75 + x,    9 + y, '#7AC500'], [ -75 + x,   27 + y, '#A7C500'], [ -75 + x,   45 + y, '#C5BE00'], [ -75 + x,   63 + y, '#816800'], [ -60 + x,  -72 + y, '#00812E'], 
            [ -60 + x,  -54 + y, '#00C52C'], [ -60 + x,  -36 + y, '#0AFF14'], [ -60 + x,  -18 + y, '#3DFF0A'], [ -60 + x,    0 + y, '#84FF0A'], [ -60 + x,   18 + y, '#CCFF0A'], [ -60 + x,   36 + y, '#FFF50A'], [ -60 + x,   54 + y, '#C59900'], [ -60 + x,   72 + y, '#815200'], 
            [ -45 + x,  -81 + y, '#008145'], [ -45 + x,  -63 + y, '#00C555'], [ -45 + x,  -45 + y, '#0AFF4D'], [ -45 + x,  -27 + y, '#4EFF55'], [ -45 + x,   -9 + y, '#84FF4E'], [ -45 + x,    9 + y, '#C9FF4E'], [ -45 + x,   27 + y, '#FFF84E'], [ -45 + x,   45 + y, '#FFBB0A'], 
            [ -45 + x,   63 + y, '#C57000'], [ -45 + x,   81 + y, '#813C00'], [ -30 + x,  -90 + y, '#00815B'], [ -30 + x,  -72 + y, '#00C57E'], [ -30 + x,  -54 + y, '#0AFF8D'], [ -30 + x,  -36 + y, '#4EFF8E'], [ -30 + x,  -18 + y, '#93FF97'], [ -30 + x,    0 + y, '#C9FF93'], 
            [ -30 + x,   18 + y, '#FFFA93'], [ -30 + x,   36 + y, '#FFBF4E'], [ -30 + x,   54 + y, '#FF7C0A'], [ -30 + x,   72 + y, '#C54700'], [ -30 + x,   90 + y, '#812500'], [ -15 + x,  -99 + y, '#00816F'], [ -15 + x,  -81 + y, '#00C5A4'], [ -15 + x,  -63 + y, '#0AFFCB'], 
            [ -15 + x,  -45 + y, '#4EFFCB'], [ -15 + x,  -27 + y, '#93FFCC'], [ -15 + x,   -9 + y, '#D7FFD8'], [ -15 + x,    9 + y, '#FFFDD7'], [ -15 + x,   27 + y, '#FFC593'], [ -15 + x,   45 + y, '#FF824E'], [ -15 + x,   63 + y, '#FF3E0A'], [ -15 + x,   81 + y, '#C52000'], 
            [ -15 + x,   99 + y, '#811100'], [   0 + x, -108 + y, '#008181'], [   0 + x,  -90 + y, '#00C5C5'], [   0 + x,  -72 + y, '#0AFFFF'], [   0 + x,  -54 + y, '#4EFFFF'], [   0 + x,  -36 + y, '#93FFFF'], [   0 + x,  -18 + y, '#D7FFFF'], [   0 + x,    0 + y, '#FFFFFF'], 
            [   0 + x,   18 + y, '#FFD7D7'], [   0 + x,   36 + y, '#FF9393'], [   0 + x,   54 + y, '#FF4E4E'], [   0 + x,   72 + y, '#FF0A0A'], [   0 + x,   90 + y, '#C50000'], [   0 + x,  108 + y, '#820011'], [  15 + x,  -99 + y, '#006F81'], [  15 + x,  -81 + y, '#00A4C5'], 
            [  15 + x,  -63 + y, '#0ACBFF'], [  15 + x,  -45 + y, '#4ECBFF'], [  15 + x,  -27 + y, '#93CCFF'], [  15 + x,   -9 + y, '#D7D8FF'], [  15 + x,    9 + y, '#FFD7FD'], [  15 + x,   27 + y, '#FF93C5'], [  15 + x,   45 + y, '#FF4E82'], [  15 + x,   63 + y, '#FF0A3E'], 
            [  15 + x,   81 + y, '#C50020'], [  15 + x,   99 + y, '#810011'], [  30 + x,  -90 + y, '#005B81'], [  30 + x,  -72 + y, '#007EC5'], [  30 + x,  -54 + y, '#0A8DFF'], [  30 + x,  -36 + y, '#4E8EFF'], [  30 + x,  -18 + y, '#9397FF'], [  30 + x,    0 + y, '#C993FF'], 
            [  30 + x,   18 + y, '#FF93FA'], [  30 + x,   36 + y, '#FF4EBF'], [  30 + x,   54 + y, '#FF0A7C'], [  30 + x,   72 + y, '#C50047'], [  30 + x,   90 + y, '#810025'], [  45 + x,  -81 + y, '#004581'], [  45 + x,  -63 + y, '#0055C5'], [  45 + x,  -45 + y, '#0A4DFF'], 
            [  45 + x,  -27 + y, '#4E55FF'], [  45 + x,   -9 + y, '#844EFF'], [  45 + x,    9 + y, '#C94EFF'], [  45 + x,   27 + y, '#FF4EF8'], [  45 + x,   45 + y, '#FF0ABB'], [  45 + x,   63 + y, '#C50070'], [  45 + x,   81 + y, '#81003C'], [  60 + x,  -72 + y, '#002E81'], 
            [  60 + x,  -54 + y, '#002CC5'], [  60 + x,  -36 + y, '#0A14FF'], [  60 + x,  -18 + y, '#3D0AFF'], [  60 + x,    0 + y, '#840AFF'], [  60 + x,   18 + y, '#CC0AFF'], [  60 + x,   36 + y, '#FF0AF5'], [  60 + x,   54 + y, '#C50099'], [  60 + x,   72 + y, '#810052'], 
            [  75 + x,  -63 + y, '#001881'], [  75 + x,  -45 + y, '#0007C5'], [  75 + x,  -27 + y, '#1E00C5'], [  75 + x,   -9 + y, '#4B00C5'], [  75 + x,    9 + y, '#7A00C5'], [  75 + x,   27 + y, '#A700C5'], [  75 + x,   45 + y, '#C500BE'], [  75 + x,   63 + y, '#810068'], 
            [  90 + x,  -54 + y, '#000481'], [  90 + x,  -36 + y, '#0F0081'], [  90 + x,  -18 + y, '#270081'], [  90 + x,    0 + y, '#400081'], [  90 + x,   18 + y, '#5A0081'], [  90 + x,   36 + y, '#710081'], [  90 + x,   54 + y, '#81007C']]

        x, y = 0, 18
        self._grayscale_hex_list = [
            [ -90 + x,   54 + y, '#FFFFFF'], [ -75 + x,   63 + y, '#E9E9E9'], [ -60 + x,   72 + y, '#D4D4D4'], [ -45 + x,   81 + y, '#BFBFBF'], [ -30 + x,   90 + y, '#AAAAAA'], [ -15 + x,   99 + y, '#949494'], [   0 + x,  108 + y, '#7F7F7F'], [  15 + x,   99 + y, '#6A6A6A'], 
            [  30 + x,   90 + y, '#555555'], [  45 + x,   81 + y, '#3F3F3F'], [  60 + x,   72 + y, '#2A2A2A'], [  75 + x,   63 + y, '#151515'], [  90 + x,   54 + y, '#000000']]

        self._value          = None
        self._clicked_pos    = None
        self._selected_hex   = None
        self._selected_color = None
        self._circle_brush   = QBrush(QColor("#FFFFFF"), Qt.Dense2Pattern)
        self._circle_pen     = QPen(QColor("#C8C8C8"))
        self._hex_pen        = QPen(Qt.NoPen)        
        self._selected_pen   = QPen(QColor("#DD3399"))
        self._selected_brush = QBrush(Qt.NoBrush)
        self._selected_pen.setWidth(3)

    def mousePressEvent(self, event):
        self._clicked_pos =  event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        if self._clicked_pos:
            self._clicked_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self,  event):
        self._clicked_pos = None

    def resizeEvent(self, event):
        self._clicked_pos  = None
        self._selected_hex = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, vals):
        if len(vals)==3 and all([ 0 <= val <= 255 for val in vals ]):
            if not(vals == self._value):
                self._value = vals
                self.valueChanged.emit(vals)

    def paintEvent(self, event):
        scale   = min(self.width()/295, self.height()/295)
        cx, cy  = self.width()/2, self.height()/2 
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True) 

        painter.setBrush(self._circle_brush)
        painter.setPen(self._circle_pen)

        l_hex = self.genVHex(cx, cy, 210 * scale)
        painter.drawPolygon(l_hex)

        painter.setPen(self._hex_pen)
        for i in (self._color_hex_list + self._grayscale_hex_list):
            x, y, color = i
            hex_poly    = self.genHHex(cx + (x * scale), cy + (y * scale), 15 * scale)
            painter.setBrush(QColor(color))
            painter.drawPolygon(hex_poly)  
            if self._clicked_pos and hex_poly.containsPoint(self._clicked_pos, Qt.OddEvenFill):
                self._selected_hex   = hex_poly
                self._selected_color = color
                self.value           = [QColor(color).red(), QColor(color).green(), QColor(color).blue()]

        if self._selected_hex:
            x, y, color = i
            painter.setPen(self._selected_pen)
            painter.setBrush(self._selected_brush)
            painter.drawPolygon(self._selected_hex)
        painter.end()        

    def genHHex(self, x, y, size):
        l        = (size/2)*1.39
        sl, ml   = (0.5 * l), (l * (3**0.5) / 2 )
        hex_poly = QPolygonF()        
        hex_poly.append(QPointF(x + l, y))
        hex_poly.append(QPointF(x + sl, y + ml))
        hex_poly.append(QPointF(x - sl, y + ml))
        hex_poly.append(QPointF(x - l, y))
        hex_poly.append(QPointF(x - sl, y - ml))
        hex_poly.append(QPointF(x + sl, y - ml))
        return hex_poly

    def genVHex(self, x, y, size):
        l        = (size/2)*1.39
        sl, ml   = (0.5 * l), (l * (3**0.5) / 2 )
        hex_poly = QPolygonF()        
        hex_poly.append(QPointF(x, y + l))
        hex_poly.append(QPointF(x - ml, y + sl))
        hex_poly.append(QPointF(x - ml, y - sl))
        hex_poly.append(QPointF(x, y - l))
        hex_poly.append(QPointF(x + ml, y - sl))
        hex_poly.append(QPointF(x + ml, y + sl))
        return hex_poly

class ColorChannelBar(QWidget):
    valueChanged = pyqtSignal(float)
    def __init__(self, prim_color = "#FFFFFF", value = 1, orentation = Qt.Vertical, parent=None):
        super(ColorChannelBar, self).__init__(parent)
        self._orentation      = orentation
        self._prim_color      = None
        self._clicked_pos     = None
        self._value           = None
        self._padding         = None
        self._indicator_size  = None
        self._indicator_brush = None
        self._border_pen      = None
        self.orentation       = orentation
        self.prim_color       = prim_color
        self.value            = value
        self.indicator_size   = 7
        self.padding          = [5, 7, 5, 0] if self.orentation == Qt.Horizontal else [0, 5, 7 ,5]
        self.indicator_brush  = QBrush(QColor("#000000"))
        self.border_pen       = QPen(QColor("#c8c8c8"))

    @property
    def prim_color(self):
        return self._prim_color

    @prim_color.setter
    def prim_color(self, prim_color):
        if type(prim_color) == QColor:
            self._prim_color = prim_color
        elif type(prim_color) == str:
            self._prim_color = QColor(prim_color)
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, prim_color))
        self.update()

    def setValue(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if 0 <= value <= 1:
            if not (value == self._value):
                self._value = value
                self.valueChanged.emit(value)
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, value))
        self.update()

    @property
    def orentation(self):
        return self._orentation

    @orentation.setter
    def orentation(self, orentation):
        if orentation in (Qt.Horizontal, Qt.Vertical):
            
            if orentation == Qt.Horizontal and not(self._orentation == orentation):
                self._orentation = orentation
                self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
                if self.padding:
                    pl, pu, pr, pd, = self.padding
                    self.padding    = [pu, pr, pu, pl]
            if orentation == Qt.Vertical and not(self._orentation == orentation):
                self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
                if self.padding:                
                    pl, pu, pr, pd, = self.padding
                    self.padding    = [pu, pr, pd, pl]
            self.update()
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, orentation))

    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, p_list):
        if all([isinstance(p, numbers.Number) and p >=0 for p in p_list ]):
            self._padding = p_list
            self.update()
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, p_list))

    @property
    def indicator_size(self):
        return self._indicator_size

    @indicator_size.setter
    def indicator_size(self, size):
        if isinstance(size, numbers.Number) and size >=0 :
            self._indicator_size = size
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, size))
        self.update()

    @property
    def indicator_brush(self):
        return self._indicator_brush

    @indicator_brush.setter
    def indicator_brush(self, brush):
        if isinstance(brush, QBrush):
            self._indicator_brush = brush
        elif isinstance(brush, QColor):
            self._indicator_brush = QBrush(brush)
        elif isinstance(brush, str):
            self._indicator_brush = QBrush(QColor(brush))
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, brush))
        self.update()

    @property
    def border_pen(self):
        return self._border_pen

    @border_pen.setter
    def border_pen(self, pen):
        if isinstance(pen, QPen):
            self._border_pen = pen
        elif isinstance(pen, QColor):
            self._border_pen = QPen(pen)
        elif isinstance(pen, str):
            self._border_pen = QPen(QColor(pen))
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, brush))
        self.update()

    def paintEvent(self, event):
        pl, pu, pr, pd, = self.padding
        w, h            = (self.width() - pl - pr), (self.height() - pu - pd)
        cx, cy          = self.width()/2, self.height()/2         
        painter         = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True) 

        gradient = QLinearGradient(0, 0, w, 0) if self.orentation == Qt.Horizontal else QLinearGradient(0, h, 0, 0)
        gradient.setColorAt(0, QColor(  0, 0, 0))
        gradient.setColorAt(1, self.prim_color)        
        painter.setPen(self.border_pen)
        painter.setBrush(gradient)
        if (w > 0 and h > 0):
            painter.drawRect(pl, pu, w, h)

        if self.indicator_brush:
            painter.setBrush(self.indicator_brush) 
        if self.orentation == Qt.Horizontal:
            painter.drawPolygon(self.genHTriangle(pl + (w * self.value), pu, self.indicator_size))
        else:    
            painter.drawPolygon(self.genVTriangle(pl + w, pu + ((1-self.value) * h), self.indicator_size))        
        painter.end()        

    def genHTriangle(self, x, y, size):
        sl, ml   = (0.5 * size), (size * (3**0.5) / 2 )
        hex_poly = QPolygonF()        
        hex_poly.append(QPointF(x, y))
        hex_poly.append(QPointF(x - sl, y - ml))
        hex_poly.append(QPointF(x + sl, y - ml))
        return hex_poly    

    def genVTriangle(self, x, y, size):
        sl, ml   = (0.5 * size), (size * (3**0.5) / 2 )
        hex_poly = QPolygonF()        
        hex_poly.append(QPointF(x, y))
        hex_poly.append(QPointF(x + ml, y - sl))
        hex_poly.append(QPointF(x + ml, y + sl))
        return hex_poly

    def mousePressEvent(self, event):
        self.value = self.getCurserVal(event.x(), event.y())

    def mouseMoveEvent(self, event):
        self.value = self.getCurserVal(event.x(), event.y())

    def getCurserVal(self, x, y):
        pl, pu, pr, pd = self.padding
        w, h           = (self.width() - pl - pr), (self.height() - pu - pd)
        x              = pl if x < pl else (pl + w) if x > (pl + w) else x 
        y              = pd if y < pd else (pu + h) if y > (pu + h) else y
        value          = (x - pl)/(w) if self.orentation == Qt.Horizontal else  1- ((y - pu)/(h))
        return value

class TriColorChannel(QWidget):
    valueChanged = pyqtSignal(list)
    def __init__(self, orentation = Qt.Vertical, parent=None):
        super(TriColorChannel, self).__init__(parent)
        self._red_bar    = ColorChannelBar("#FF0000")
        self._green_bar  = ColorChannelBar("#00FF00")
        self._blue_bar   = ColorChannelBar("#0000FF") 
        self._red_spin   = QSpinBox()
        self._green_spin = QSpinBox()
        self._blue_spin  = QSpinBox()
        self._hex_edit   = ColorHexEdit()
        self._red_box    = VBox(self._red_bar,   self._red_spin)
        self._green_box  = VBox(self._green_bar, self._green_spin)
        self._blue_box   = VBox(self._blue_bar,  self._blue_spin)
        self._tri_box    = HBox(self._red_box, self._green_box, self._blue_box)
        self._main_box   = VBox(self._hex_edit, self._tri_box)
        self._bar_width  = None
        self._orentation = None
        self._spin_width = None
        self._value      = None

        self._red_spin.setRange(0, 255)
        self._green_spin.setRange(0, 255)
        self._blue_spin.setRange(0, 255)        
        self.bind_data()

        self.spin_width  = 40
        self.bar_width   = 18
        self.orentation  = orentation
        self.value       = [255, 255, 255]

        self.setLayout(self._main_box)
        

    def bind_data(self):
        self.valueChanged.connect( lambda val : self._red_spin.setValue(val[0]))
        self.valueChanged.connect( lambda val : self._green_spin.setValue(val[1]))
        self.valueChanged.connect( lambda val : self._blue_spin.setValue(val[2]))
        self.valueChanged.connect( lambda val : self._hex_edit.setValue(val))

        self._hex_edit.valueChanged.connect(lambda  val : self.setValue(val))

        self._red_spin.valueChanged.connect(  lambda val : self.setRed(val))
        self._green_spin.valueChanged.connect(lambda val : self.setGreen(val))
        self._blue_spin.valueChanged.connect( lambda val : self.setBlue(val))     

        self._red_spin.valueChanged.connect(  lambda val : self._red_bar.setValue(val / 255))
        self._green_spin.valueChanged.connect(lambda val : self._green_bar.setValue(val / 255))
        self._blue_spin.valueChanged.connect( lambda val : self._blue_bar.setValue(val / 255))

        self._red_bar.valueChanged.connect(   lambda val : self._red_spin.setValue(int(val * 255)))
        self._green_bar.valueChanged.connect( lambda val : self._green_spin.setValue(int(val * 255)))
        self._blue_bar.valueChanged.connect(  lambda val : self._blue_spin.setValue(int(val * 255)))


    def setValue(self, value):
        self.value = value

    def setRed(self, r):
        self.red = r

    def setGreen(self, g):
        self.green = g
    
    def setBlue(self, b):
        self.blue = b

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, vals):
        if len(vals)==3 and all([ 0 <= val <= 255 for val in vals ]):
            if not(vals == self._value):
                self._value = vals
                self.valueChanged.emit(vals)
        self.update()

    @property
    def red(self):
        return self.value[0]

    @red.setter
    def red(self, r):
        self.value = [r, self.value[1], self.value[2]]

    @property
    def green(self):
        return self.value[1]

    @green.setter
    def green(self, g):
        self.value = [self.value[0], g, self.value[2]]

    @property
    def blue(self):
        return self.value[2]

    @blue.setter
    def blue(self, b):
        self.value = [self.value[0], self.value[1], b]

    @property
    def orentation(self):
        return self._orentation

    @orentation.setter
    def orentation(self, orentation):
        if orentation in [Qt.Vertical, Qt.Horizontal]:
            if not ( orentation == self._orentation):
                if orentation == Qt.Vertical:
                    self._red_bar.orentation   = Qt.Vertical
                    self._green_bar.orentation = Qt.Vertical
                    self._blue_bar.orentation  = Qt.Vertical                      
                    self._red_box.setDirection(QBoxLayout.TopToBottom)
                    self._green_box.setDirection(QBoxLayout.TopToBottom)
                    self._blue_box.setDirection(QBoxLayout.TopToBottom)
                    self._tri_box.setDirection(QBoxLayout.LeftToRight)
                    self._main_box.setDirection(QBoxLayout.TopToBottom)
                    self._red_box.setAlignment(self._red_bar, Qt.AlignHCenter)
                    self._green_box.setAlignment(self._green_bar, Qt.AlignHCenter)
                    self._blue_box.setAlignment(self._blue_bar, Qt.AlignHCenter)
                    self._main_box.setAlignment(self._hex_edit, Qt.AlignHCenter)
                    self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)

                elif orentation == Qt.Horizontal:
                    self._red_bar.orentation   = Qt.Horizontal
                    self._green_bar.orentation = Qt.Horizontal
                    self._blue_bar.orentation  = Qt.Horizontal                    
                    self._red_box.setDirection(QBoxLayout.LeftToRight)
                    self._green_box.setDirection(QBoxLayout.LeftToRight)
                    self._blue_box.setDirection(QBoxLayout.LeftToRight)
                    self._tri_box.setDirection(QBoxLayout.TopToBottom)
                    self._main_box.setDirection(QBoxLayout.LeftToRight)
                    self._red_box.setAlignment(self._red_bar, Qt.AlignVCenter)
                    self._green_box.setAlignment(self._green_bar, Qt.AlignVCenter)
                    self._blue_box.setAlignment(self._blue_bar, Qt.AlignVCenter)           
                    self._main_box.setAlignment(self._hex_edit, Qt.AlignVCenter)
                    self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)              
                self._orentation = orentation
                self.bar_width   = self._bar_width
        self.update()

    @property
    def bar_width(self):
        return self._bar_width

    @bar_width.setter
    def bar_width(self, width):
        if (isinstance(width, numbers.Number) and width > 0):
            bars = [self._red_bar, self._green_bar, self._blue_bar]
            _    = [bar.resize(bar.sizeHint()) for bar in bars]
            self._red_bar.adjustSize()
            if self._orentation == Qt.Vertical:
                _ = [bar.setFixedWidth(width) for bar in bars]
            elif self._orentation == Qt.Horizontal:
                _ = [bar.setFixedHeight(width) for bar in bars]             

            self._bar_width = width
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, width))

    @property
    def spin_width(self):
        return self._spin_width

    @spin_width.setter
    def spin_width(self, width):
        if (isinstance(width, numbers.Number) and width > 0):
            spins = [self._red_spin, self._green_spin, self._blue_spin]
            _     = [spin.setFixedWidth(width) for spin in spins]
            self._spin_width = width
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, width))

class ColorTextEdit(QLineEdit):
    def __init__(self,  parent=None):
        super(ColorTextEdit, self).__init__(parent)
        self._color_light = QColor("#EEEEEE")
        self._color_dark  = QColor("#333333")
        self._Transparent = QColor(0,0,0,0)
 
        self.setFrame(False)
        self.setAlignment(Qt.AlignCenter)
        self.setInputMask(r"\#>HHHHHH")
        self.setTextMargins(0,0,0,0)
        self.setFixedWidth(55)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setFont(QFont("consolas", weight = 75))
        self.textChanged.connect(lambda : self.update_palette())

    def setText(self, txt):
        QLineEdit.setText(self, txt) 
        self.update_palette()
     
    def update_palette(self):
        palette = QPalette()
        color   = QColor(self.text())
        palette.setColor(QPalette.Text, self._color_light if (color.lightness() < 180) and (max([color.red(), color.green(), color.blue()]) < 250) else self._color_dark)
        palette.setColor(QPalette.Base, self._Transparent)
        self.setPalette(palette)
        self.update()

class ColorHexEdit(QWidget):
    valueChanged = pyqtSignal(list)
    textChanged  = pyqtSignal(str)
    def __init__(self,  parent=None):
        super(ColorHexEdit, self).__init__(parent)
        self._text       = None
        self._value      = None
        self._edit       = ColorTextEdit()
        self._border_pen = QPen(QColor("#DD3399"))
        self._border_pen.setWidth(3)
        self.setLayout(HBox(self._edit))
        self.setFixedSize(80, 80)
        self._edit.textChanged.connect(self.setText)

    @pyqtSlot(str)        
    def setText(self, txt):
        self.text = txt

    @pyqtSlot(list)
    def setValue(self, vals):
        self.value = vals

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, vals):
        if len(vals)==3 and all([ 0 <= val <= 255 for val in vals ]):
            if not(vals == self._value):
                txt         = "#{0:02X}{1:02x}{2:02X}".format(*vals)
                self._value = vals
                self._text  = txt
                self.blockSignals(True)
                self._edit.setText(txt)      
                self.blockSignals(False) 
                self.valueChanged.emit(vals)
                self.textChanged.emit(txt)
        self.update()


    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, txt):
        if re.match(r"^#[0-9A-F]{0,6}$", txt):
            if not (txt == self._text):
                vals        = [QColor(txt).red(), QColor(txt).green(), QColor(txt).blue()]
                self._value = vals
                self._text  = txt
                self.blockSignals(True)
                self._edit.setText(txt)      
                self.blockSignals(False) 
                self.valueChanged.emit(vals)
                self.textChanged.emit(txt)
        self.update()


    def paintEvent(self, event):
        scale   = min(self.width()/298, self.height()/298)
        cx, cy  = self.width()/2, self.height()/2 
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True) 
        painter.setBrush(QColor(self.text if self.text else Qt.NoBrush))
        painter.setPen(self._border_pen)
        l_hex = self.genVHex(cx, cy, 210 * scale)
        painter.drawPolygon(l_hex)
        painter.end()   

    def genVHex(self, x, y, size):
        l        = (size/2)*1.39
        sl, ml   = (0.5 * l), (l * (3**0.5) / 2 )
        hex_poly = QPolygonF()        
        hex_poly.append(QPointF(x, y + l))
        hex_poly.append(QPointF(x - ml, y + sl))
        hex_poly.append(QPointF(x - ml, y - sl))
        hex_poly.append(QPointF(x, y - l))
        hex_poly.append(QPointF(x + ml, y - sl))
        hex_poly.append(QPointF(x + ml, y + sl))
        return hex_poly

class ColorDialog(QWidget):
    valueChanged = pyqtSignal(list)
    def __init__(self,  parent=None):
        super(ColorDialog, self).__init__(parent)
        self._value            = None
        self.color_selector    = ColorSelector()
        self.tri_color_channel = TriColorChannel(orentation = Qt.Horizontal)
        self.confirm_pb        = QPushButton("OK")
        self.cancel_pb         = QPushButton("Cancle")

        v1                     = VBox(self.color_selector, self.tri_color_channel)
        h1                     = HBox( -1, self.confirm_pb, self.cancel_pb)
        v2                     = VBox(v1, h1)

        self.color_selector.valueChanged.connect(self.setValue)
        self.tri_color_channel.valueChanged.connect(self.setValue)
        self.valueChanged.connect(self.tri_color_channel.setValue)
        self.confirm_pb.clicked.connect(self.close)
        self.cancel_pb.clicked.connect(self.close)

        self.setLayout(v2)
        self.resize(400, 500)

    @pyqtSlot(list)
    def setValue(self, vals):
        self.value = vals

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, vals):
        if len(vals) == 3 and all([ 0<= val <=255 for val in vals]):
            if not(vals == self._value):
                self._value = vals
                self.valueChanged.emit(vals)
                self.update()
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, vals))

    def closeEvent(self, e):
        e.accept()
        return self._value

if __name__ == "__main__":
    def Debugger():

        app  = QApplication(sys.argv)
        form = ColorDialog()
        form.show()
        app.exec_()

    Debugger()