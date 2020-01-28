import os
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
import inspect
class ColorSelector(QWidget):
    def __init__(self, parent=None):
        super(ColorSelector, self).__init__(parent)
        x, y = 0, -18
        self.color_hex_list = [
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
        self.grayscale_hex_list = [
            [ -90 + x,   54 + y, '#FFFFFF'], [ -75 + x,   63 + y, '#E9E9E9'], [ -60 + x,   72 + y, '#D4D4D4'], [ -45 + x,   81 + y, '#BFBFBF'], [ -30 + x,   90 + y, '#AAAAAA'], [ -15 + x,   99 + y, '#949494'], [   0 + x,  108 + y, '#7F7F7F'], [  15 + x,   99 + y, '#6A6A6A'], 
            [  30 + x,   90 + y, '#555555'], [  45 + x,   81 + y, '#3F3F3F'], [  60 + x,   72 + y, '#2A2A2A'], [  75 + x,   63 + y, '#151515'], [  90 + x,   54 + y, '#000000']]

        self.clicked_pos    = None
        self.selected_hex   = None
        self.selected_color = None
        self.circle_brush   = QBrush(QColor("#FFFFFF"), Qt.Dense2Pattern)
        self.circle_pen     = QPen(QColor("#c8c8c8"))
        self.hex_pen        = QPen(Qt.NoPen)        
        self.selected_pen   = QPen(QColor("#dd3399"))
        self.selected_brush = QBrush(Qt.NoBrush)
        self.selected_pen.setWidth(3)
        self.resize(350, 350)

    def mousePressEvent(self, event):
        self.clicked_pos =  event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        if self.clicked_pos:
            self.clicked_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self,  event):
        self.clicked_pos = None

    def resizeEvent(self, event):
        self.clicked_pos  = None
        self.selected_hex = None

    def paintEvent(self, event):
        scale   = min(self.width()/320, self.height()/320)
        cx, cy  = self.width()/2, self.height()/2 
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True) 

        painter.setBrush(self.circle_brush)
        painter.setPen(self.circle_pen)
        # painter.drawEllipse(QPointF(cx, cy), 150 * scale, 150 * scale)

        l_hex = self.genVHex(cx, cy, 210 * scale)
        painter.drawPolygon(l_hex)

        painter.setPen(self.hex_pen)
        for i in (self.color_hex_list + self.grayscale_hex_list):
            x, y, color = i
            hex_poly    = self.genHHex(cx + (x * scale), cy + (y * scale), 15 * scale)
            painter.setBrush(QColor(color))
            painter.drawPolygon(hex_poly)  
            if self.clicked_pos and hex_poly.containsPoint(self.clicked_pos, Qt.OddEvenFill):
                self.selected_hex   = hex_poly
                self.selected_color = color

        if self.selected_hex:
            x, y, color = i
            painter.setPen(self.selected_pen)
            painter.setBrush(self.selected_brush)
            painter.drawPolygon(self.selected_hex)
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
    def __init__(self, prim_color = "#FFFFFF", value = 1, orentation = Qt.Vertical, parent=None):
        super(ColorChannelBar, self).__init__(parent)
        self._orentation  = orentation
        self._prim_color  = None
        self._clicked_pos = None
        self._value       = None
        self._padding     = [10, 10, 10, 10]
        self.orentation   = orentation
        self.prim_color   = prim_color
        self.value        = value



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

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if 0 <= value <= 1:
            self._value = value
            self.update()
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, value))

    @property
    def orentation(self):
        return self._orentation

    @orentation.setter
    def orentation(self, orentation):
        if orentation in (Qt.Horizontal, Qt.Vertical):
            self._orentation = orentation
            self.update()
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, orentation))
    @property
    def padding(self):
        return self._padding

    @padding.setter
    def padding(self, l, u, r, d):
        if all([isinstance(p, numbers.Number) and p >=0 for p in [l, u, r, d] ]):
            self._padding = [l, u, r, d]
            self.update()
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, [l, u, r, d]))



    def paintEvent(self, event):
        pl, pu, pr, pd, = self.padding
        w, h            = (self.width() - pl - pr), (self.height() - pu - pd)
        cx, cy          = self.width()/2, self.height()/2         
        painter         = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True) 

        pen      = QPen(QColor("#c8c8c8"))
        gradient = QLinearGradient(0, 0, w, 0) if self.orentation == Qt.Horizontal else QLinearGradient(0, 0, 0, h)
        pen.setWidth(0.5)
        painter.setPen(pen)
        gradient.setColorAt(0, QColor(  0, 0, 0))
        gradient.setColorAt(1, self.prim_color)
        painter.setBrush(gradient) 
        painter.drawRect(pl, pu, w, h)
        if self.orentation == Qt.Horizontal:
            painter.drawPolygon(self.genHTriangle(pl + (w * self.value), pu, 10))
        else:    
            painter.drawPolygon(self.genVTriangle(pl + w, pu + (self.value * h), 10))        
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
        x              = pl if x < pl else (pr + w) if x > (pl + w) else x 
        y              = pd if y < pd else (pu + h) if y > (pu + h) else y
        value          = (x - pl)/(w) if self.orentation == Qt.Horizontal else  (y - pu)/(h)
        return value


def Debugger():
    app  = QApplication(sys.argv)
    form = ColorChannelBar()
    form.show()
    app.exec_()
    
Debugger()