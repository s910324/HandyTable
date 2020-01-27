import os
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *

class BrushSelector(QWidget):
    def __init__(self, parent=None):
        super(BrushSelector, self).__init__(parent)
        d = 20
        self.d = d
        self.palette_array = [[( -6 * d + ( abs(6) *d /2), 6 * 0.85 * d), ( -5 * d + ( abs(6) *d /2), 6 * 0.85 * d), ( -4 * d + ( abs(6) *d /2), 6 * 0.85 * d), ( -3 * d + ( abs(6) *d /2), 6 * 0.85 * d), ( -2 * d + ( abs(6) *d /2), 6 * 0.85 * d), ( -1 * d + ( abs(6) *d /2), 6 * 0.85 * d), ( 0 * d + ( abs(6) *d /2), 6 * 0.85 * d)], 
            [( -6 * d + ( abs(5) *d /2), 5 * 0.85 * d), ( -5 * d + ( abs(5) *d /2), 5 * 0.85 * d), ( -4 * d + ( abs(5) *d /2), 5 * 0.85 * d), ( -3 * d + ( abs(5) *d /2), 5 * 0.85 * d), ( -2 * d + ( abs(5) *d /2), 5 * 0.85 * d), ( -1 * d + ( abs(5) *d /2), 5 * 0.85 * d), ( 0 * d + ( abs(5) *d /2), 5 * 0.85 * d), ( 1 * d + ( abs(5) *d /2), 5 * 0.85 * d)], 
            [( -6 * d + ( abs(4) *d /2), 4 * 0.85 * d), ( -5 * d + ( abs(4) *d /2), 4 * 0.85 * d), ( -4 * d + ( abs(4) *d /2), 4 * 0.85 * d), ( -3 * d + ( abs(4) *d /2), 4 * 0.85 * d), ( -2 * d + ( abs(4) *d /2), 4 * 0.85 * d), ( -1 * d + ( abs(4) *d /2), 4 * 0.85 * d), ( 0 * d + ( abs(4) *d /2), 4 * 0.85 * d), ( 1 * d + ( abs(4) *d /2), 4 * 0.85 * d), ( 2 * d + ( abs(4) *d /2), 4 * 0.85 * d)], 
            [( -6 * d + ( abs(3) *d /2), 3 * 0.85 * d), ( -5 * d + ( abs(3) *d /2), 3 * 0.85 * d), ( -4 * d + ( abs(3) *d /2), 3 * 0.85 * d), ( -3 * d + ( abs(3) *d /2), 3 * 0.85 * d), ( -2 * d + ( abs(3) *d /2), 3 * 0.85 * d), ( -1 * d + ( abs(3) *d /2), 3 * 0.85 * d), ( 0 * d + ( abs(3) *d /2), 3 * 0.85 * d), ( 1 * d + ( abs(3) *d /2), 3 * 0.85 * d), ( 2 * d + ( abs(3) *d /2), 3 * 0.85 * d), ( 3 * d + ( abs(3) *d /2), 3 * 0.85 * d)], 
            [( -6 * d + ( abs(2) *d /2), 2 * 0.85 * d), ( -5 * d + ( abs(2) *d /2), 2 * 0.85 * d), ( -4 * d + ( abs(2) *d /2), 2 * 0.85 * d), ( -3 * d + ( abs(2) *d /2), 2 * 0.85 * d), ( -2 * d + ( abs(2) *d /2), 2 * 0.85 * d), ( -1 * d + ( abs(2) *d /2), 2 * 0.85 * d), ( 0 * d + ( abs(2) *d /2), 2 * 0.85 * d), ( 1 * d + ( abs(2) *d /2), 2 * 0.85 * d), ( 2 * d + ( abs(2) *d /2), 2 * 0.85 * d), ( 3 * d + ( abs(2) *d /2), 2 * 0.85 * d), ( 4 * d + ( abs(2) *d /2), 2 * 0.85 * d)], 
            [( -6 * d + ( abs(1) *d /2), 1 * 0.85 * d), ( -5 * d + ( abs(1) *d /2), 1 * 0.85 * d), ( -4 * d + ( abs(1) *d /2), 1 * 0.85 * d), ( -3 * d + ( abs(1) *d /2), 1 * 0.85 * d), ( -2 * d + ( abs(1) *d /2), 1 * 0.85 * d), ( -1 * d + ( abs(1) *d /2), 1 * 0.85 * d), ( 0 * d + ( abs(1) *d /2), 1 * 0.85 * d), ( 1 * d + ( abs(1) *d /2), 1 * 0.85 * d), ( 2 * d + ( abs(1) *d /2), 1 * 0.85 * d), ( 3 * d + ( abs(1) *d /2), 1 * 0.85 * d), ( 4 * d + ( abs(1) *d /2), 1 * 0.85 * d), ( 5 * d + ( abs(1) *d /2), 1 * 0.85 * d)], 
            [( -6 * d + ( abs(0) *d /2), 0 * 0.85 * d), ( -5 * d + ( abs(0) *d /2), 0 * 0.85 * d), ( -4 * d + ( abs(0) *d /2), 0 * 0.85 * d), ( -3 * d + ( abs(0) *d /2), 0 * 0.85 * d), ( -2 * d + ( abs(0) *d /2), 0 * 0.85 * d), ( -1 * d + ( abs(0) *d /2), 0 * 0.85 * d), ( 0 * d + ( abs(0) *d /2), 0 * 0.85 * d), ( 1 * d + ( abs(0) *d /2), 0 * 0.85 * d), ( 2 * d + ( abs(0) *d /2), 0 * 0.85 * d), ( 3 * d + ( abs(0) *d /2), 0 * 0.85 * d), ( 4 * d + ( abs(0) *d /2), 0 * 0.85 * d), ( 5 * d + ( abs(0) *d /2), 0 * 0.85 * d), ( 6 * d + ( abs(0) *d /2), 0 * 0.85 * d)], 
            [( -6 * d + ( abs(-1) *d /2), -1 * 0.85 * d), ( -5 * d + ( abs(-1) *d /2), -1 * 0.85 * d), ( -4 * d + ( abs(-1) *d /2), -1 * 0.85 * d), ( -3 * d + ( abs(-1) *d /2), -1 * 0.85 * d), ( -2 * d + ( abs(-1) *d /2), -1 * 0.85 * d), ( -1 * d + ( abs(-1) *d /2), -1 * 0.85 * d), ( 0 * d + ( abs(-1) *d /2), -1 * 0.85 * d), ( 1 * d + ( abs(-1) *d /2), -1 * 0.85 * d), ( 2 * d + ( abs(-1) *d /2), -1 * 0.85 * d), ( 3 * d + ( abs(-1) *d /2), -1 * 0.85 * d), ( 4 * d + ( abs(-1) *d /2), -1 * 0.85 * d), ( 5 * d + ( abs(-1) *d /2), -1 * 0.85 * d)], 
            [( -6 * d + ( abs(-2) *d /2), -2 * 0.85 * d), ( -5 * d + ( abs(-2) *d /2), -2 * 0.85 * d), ( -4 * d + ( abs(-2) *d /2), -2 * 0.85 * d), ( -3 * d + ( abs(-2) *d /2), -2 * 0.85 * d), ( -2 * d + ( abs(-2) *d /2), -2 * 0.85 * d), ( -1 * d + ( abs(-2) *d /2), -2 * 0.85 * d), ( 0 * d + ( abs(-2) *d /2), -2 * 0.85 * d), ( 1 * d + ( abs(-2) *d /2), -2 * 0.85 * d), ( 2 * d + ( abs(-2) *d /2), -2 * 0.85 * d), ( 3 * d + ( abs(-2) *d /2), -2 * 0.85 * d), ( 4 * d + ( abs(-2) *d /2), -2 * 0.85 * d)], 
            [( -6 * d + ( abs(-3) *d /2), -3 * 0.85 * d), ( -5 * d + ( abs(-3) *d /2), -3 * 0.85 * d), ( -4 * d + ( abs(-3) *d /2), -3 * 0.85 * d), ( -3 * d + ( abs(-3) *d /2), -3 * 0.85 * d), ( -2 * d + ( abs(-3) *d /2), -3 * 0.85 * d), ( -1 * d + ( abs(-3) *d /2), -3 * 0.85 * d), ( 0 * d + ( abs(-3) *d /2), -3 * 0.85 * d), ( 1 * d + ( abs(-3) *d /2), -3 * 0.85 * d), ( 2 * d + ( abs(-3) *d /2), -3 * 0.85 * d), ( 3 * d + ( abs(-3) *d /2), -3 * 0.85 * d)], 
            [( -6 * d + ( abs(-4) *d /2), -4 * 0.85 * d), ( -5 * d + ( abs(-4) *d /2), -4 * 0.85 * d), ( -4 * d + ( abs(-4) *d /2), -4 * 0.85 * d), ( -3 * d + ( abs(-4) *d /2), -4 * 0.85 * d), ( -2 * d + ( abs(-4) *d /2), -4 * 0.85 * d), ( -1 * d + ( abs(-4) *d /2), -4 * 0.85 * d), ( 0 * d + ( abs(-4) *d /2), -4 * 0.85 * d), ( 1 * d + ( abs(-4) *d /2), -4 * 0.85 * d), ( 2 * d + ( abs(-4) *d /2), -4 * 0.85 * d)], 
            [( -6 * d + ( abs(-5) *d /2), -5 * 0.85 * d), ( -5 * d + ( abs(-5) *d /2), -5 * 0.85 * d), ( -4 * d + ( abs(-5) *d /2), -5 * 0.85 * d), ( -3 * d + ( abs(-5) *d /2), -5 * 0.85 * d), ( -2 * d + ( abs(-5) *d /2), -5 * 0.85 * d), ( -1 * d + ( abs(-5) *d /2), -5 * 0.85 * d), ( 0 * d + ( abs(-5) *d /2), -5 * 0.85 * d), ( 1 * d + ( abs(-5) *d /2), -5 * 0.85 * d)], 
            [( -6 * d + ( abs(-6) *d /2), -6 * 0.85 * d), ( -5 * d + ( abs(-6) *d /2), -6 * 0.85 * d), ( -4 * d + ( abs(-6) *d /2), -6 * 0.85 * d), ( -3 * d + ( abs(-6) *d /2), -6 * 0.85 * d), ( -2 * d + ( abs(-6) *d /2), -6 * 0.85 * d), ( -1 * d + ( abs(-6) *d /2), -6 * 0.85 * d), ( 0 * d + ( abs(-6) *d /2), -6 * 0.85 * d)]]

        self.resize(690, 620)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        cx, cy = 350, 300
        section = -14
        d = self.d
        r=255
        
        painter.setRenderHint(painter.Antialiasing)
        
        painter.setPen(QColor(88, 88, 88))

        for row in self.palette_array:
            for col in row:
                x, y    = col
                # r, g, b = 255, 255, 255
                r, g, b = 0,0,0
                theta =  (math.atan2(y, x) / math.pi * 180)
                shade = ( math.sqrt((x**2 + y**2)) / (6 * d)) * 255
                if theta >= -90 and theta <= 90:
                    r = shade
                if (theta <= -30 and theta >= -180) or (theta >= 150 and theta <= 180):
                    g = shade
                if (theta >= 30 and theta <= 180) or (theta <= -150 and  theta >= -180):
                    b = shade
                
                    
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(QColor(r,g,b)))
                self.drawHex(painter, cx+x, cy+y, d)  
                # self.drawLoc(painter, cx+x, cy+y, d, theta)  

        painter.end()        

    def drawHex(self, painter, x, y, size):
        hex_poly = QPolygonF()
        l = (size/2)*1.2
        hex_poly.append(QPointF(x, y + l))
        hex_poly.append(QPointF(x - (l*0.85), y + (l/2)))
        hex_poly.append(QPointF(x - (l*0.85), y - (l/2)))
        hex_poly.append(QPointF(x, y - l))
        hex_poly.append(QPointF(x + (l*0.85), y - (l/2)))
        hex_poly.append(QPointF(x + (l*0.85), y + (l/2)))        
        
        painter.drawPolygon(hex_poly)

    def drawLoc(self, painter, x, y, size, theta):
        l = (size/2)
        r = QRectF(x - l, y - (l * 0.85), 2 * l, 0.85 * 2 * l   )
        painter.drawText(r, Qt.AlignCenter, "%.2f" % (theta))




def Debugger():
    app  = QApplication(sys.argv)
    form = BrushSelector()
    form.show()
    app.exec_()
    
Debugger()