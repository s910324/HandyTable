import os
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *

class BrushSelector(QWidget):
    def __init__(self, parent=None):
        super(BrushSelector, self).__init__(parent)
        x, y = 110, -108
        self.hex_list = [
            [-200 + x,  54 + y, '#008104'], [-200 + x,  72 + y, '#0F8100'], [-200 + x,  90 + y, '#278100'], [-200 + x, 108 + y, '#408100'], [-200 + x, 126 + y, '#5A8100'], [-200 + x, 144 + y, '#718100'], 
            [-200 + x, 162 + y, '#817C00'], [-185 + x,  45 + y, '#008118'], [-185 + x,  63 + y, '#00C507'], [-185 + x,  81 + y, '#1EC500'], [-185 + x,  99 + y, '#4BC500'], [-185 + x, 117 + y, '#7AC500'], 
            [-185 + x, 135 + y, '#A7C500'], [-185 + x, 153 + y, '#C5BE00'], [-185 + x, 171 + y, '#816800'], [-170 + x,  36 + y, '#00812E'], [-170 + x,  54 + y, '#00C52C'], [-170 + x,  72 + y, '#0AFF14'], 
            [-170 + x,  90 + y, '#3DFF0A'], [-170 + x, 108 + y, '#84FF0A'], [-170 + x, 126 + y, '#CCFF0A'], [-170 + x, 144 + y, '#FFF50A'], [-170 + x, 162 + y, '#C59900'], [-170 + x, 180 + y, '#815200'], 
            [-155 + x,  27 + y, '#008145'], [-155 + x,  45 + y, '#00C555'], [-155 + x,  63 + y, '#0AFF4D'], [-155 + x,  81 + y, '#4EFF55'], [-155 + x,  99 + y, '#84FF4E'], [-155 + x, 117 + y, '#C9FF4E'], 
            [-155 + x, 135 + y, '#FFF84E'], [-155 + x, 153 + y, '#FFBB0A'], [-155 + x, 171 + y, '#C57000'], [-155 + x, 189 + y, '#813C00'], [-140 + x,  18 + y, '#00815B'], [-140 + x,  36 + y, '#00C57E'], 
            [-140 + x,  54 + y, '#0AFF8D'], [-140 + x,  72 + y, '#4EFF8E'], [-140 + x,  90 + y, '#93FF97'], [-140 + x, 108 + y, '#C9FF93'], [-140 + x, 126 + y, '#FFFA93'], [-140 + x, 144 + y, '#FFBF4E'], 
            [-140 + x, 162 + y, '#FF7C0A'], [-140 + x, 180 + y, '#C54700'], [-140 + x, 198 + y, '#812500'], [-125 + x,   9 + y, '#00816F'], [-125 + x,  27 + y, '#00C5A4'], [-125 + x,  45 + y, '#0AFFCB'], 
            [-125 + x,  63 + y, '#4EFFCB'], [-125 + x,  81 + y, '#93FFCC'], [-125 + x,  99 + y, '#D7FFD8'], [-125 + x, 117 + y, '#FFFDD7'], [-125 + x, 135 + y, '#FFC593'], [-125 + x, 153 + y, '#FF824E'], 
            [-125 + x, 171 + y, '#FF3E0A'], [-125 + x, 189 + y, '#C52000'], [-125 + x, 207 + y, '#811100'], [-110 + x,   0 + y, '#008181'], [-110 + x,  18 + y, '#00C5C5'], [-110 + x,  36 + y, '#0AFFFF'], 
            [-110 + x,  54 + y, '#4EFFFF'], [-110 + x,  72 + y, '#93FFFF'], [-110 + x,  90 + y, '#D7FFFF'], [-110 + x, 108 + y, '#FFFFFF'], [-110 + x, 126 + y, '#FFD7D7'], [-110 + x, 144 + y, '#FF9393'], 
            [-110 + x, 162 + y, '#FF4E4E'], [-110 + x, 180 + y, '#FF0A0A'], [-110 + x, 198 + y, '#C50000'], [-110 + x, 216 + y, '#820011'], [ -95 + x,   9 + y, '#336600'], [ -95 + x,  27 + y, '#009900'], 
            [ -95 + x,  45 + y, '#66FF33'], [ -95 + x,  63 + y, '#99FF66'], [ -95 + x,  81 + y, '#CCFF99'], [ -95 + x,  99 + y, '#FFFFCC'], [ -95 + x, 117 + y, '#FFD7FD'], [ -95 + x, 135 + y, '#FF93C5'], 
            [ -95 + x, 153 + y, '#FF4E82'], [ -95 + x, 171 + y, '#FF0A3E'], [ -95 + x, 189 + y, '#C50020'], [ -95 + x, 207 + y, '#810011'], [ -80 + x,  18 + y, '#333300'], [ -80 + x,  36 + y, '#669900'], 
            [ -80 + x,  54 + y, '#99FF33'], [ -80 + x,  72 + y, '#CCFF66'], [ -80 + x,  90 + y, '#FFFF99'], [ -80 + x, 108 + y, '#FFCC99'], [ -80 + x, 126 + y, '#FF93FA'], [ -80 + x, 144 + y, '#FF4EBF'], 
            [ -80 + x, 162 + y, '#FF0A7C'], [ -80 + x, 180 + y, '#C50047'], [ -80 + x, 198 + y, '#810025'], [ -65 + x,  27 + y, '#666633'], [ -65 + x,  45 + y, '#99CC00'], [ -65 + x,  63 + y, '#CCFF33'], 
            [ -65 + x,  81 + y, '#FFFF66'], [ -65 + x,  99 + y, '#844EFF'], [ -65 + x, 117 + y, '#C94EFF'], [ -65 + x, 135 + y, '#FF4EF8'], [ -65 + x, 153 + y, '#FF0ABB'], [ -65 + x, 171 + y, '#C50070'], 
            [ -65 + x, 189 + y, '#81003C'], [ -50 + x,  36 + y, '#999966'], [ -50 + x,  54 + y, '#CCCC00'], [ -50 + x,  72 + y, '#FFFF00'], [ -50 + x,  90 + y, '#3D0AFF'], [ -50 + x, 108 + y, '#840AFF'], 
            [ -50 + x, 126 + y, '#CC0AFF'], [ -50 + x, 144 + y, '#FF0AF5'], [ -50 + x, 162 + y, '#C50099'], [ -50 + x, 180 + y, '#810052'], [ -35 + x,  45 + y, '#996633'], [ -35 + x,  63 + y, '#CC9900'], 
            [ -35 + x,  81 + y, '#1E00C5'], [ -35 + x,  99 + y, '#4B00C5'], [ -35 + x, 117 + y, '#7A00C5'], [ -35 + x, 135 + y, '#A700C5'], [ -35 + x, 153 + y, '#C500BE'], [ -35 + x, 171 + y, '#810068'], 
            [ -20 + x,  54 + y, '#000481'], [ -20 + x,  72 + y, '#0F0081'], [ -20 + x,  90 + y, '#270081'], [ -20 + x, 108 + y, '#400081'], [ -20 + x, 126 + y, '#5A0081'], [ -20 + x, 144 + y, '#710081'], 
            [ -20 + x, 162 + y, '#81007C']]

        self.resize(1400, 600)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        cx, cy = 300, 200
        painter.setBrush(QColor("#ffffff"))
        painter.setPen(QColor("#c8c8c8"))
        painter.drawEllipse(QPointF(cx, cy), 125, 125)
        painter.drawEllipse(QPointF(cx, cy), 5, 5)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.setPen(QPen(Qt.NoPen))

        for i in self.hex_list:
            x, y, color = i
            painter.setBrush(QColor(color))
            self.drawHex(painter, cx+x, cy+y, 15)   

        
        painter.end()        


    def drawHex(self, painter, x, y, size):
        hex_poly = QPolygonF()
        l = (size/2)*1.38
        hex_poly.append(QPointF(x + l, y))
        hex_poly.append(QPointF(x + 0.5 * l, y + (l * (3**0.5) / 2 )))
        hex_poly.append(QPointF(x - 0.5 * l, y + (l * (3**0.5) / 2 )))
        hex_poly.append(QPointF(x - l, y))
        hex_poly.append(QPointF(x - 0.5 * l, y - (l * (3**0.5) / 2 )))
        hex_poly.append(QPointF(x + 0.5 * l, y - (l * (3**0.5) / 2 )))
        painter.drawPolygon(hex_poly)


def Debugger():
    app  = QApplication(sys.argv)
    form = BrushSelector()
    form.show()
    app.exec_()
    
Debugger()