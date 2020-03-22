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

class SelectDialog(QWidget):
    def __init__(self,  parent=None):
        super(SelectDialog, self).__init__(parent)    
        b = BrushSelectDrop()
        l = LineSelectDrop()
        f = FontSelectDrop()
        s = SizeSelectDrop()

        b.valueChanged.connect(lambda x : print(x))
        b.buttonClicked.connect(lambda  : print("main clicked"))
        b.dropClicked.connect(lambda    : print("drop clicked"))
        l.valueChanged.connect(lambda x : print(x))
        f.valueChanged.connect(lambda x : print(x))
        s.valueChanged.connect(lambda x : print(x))
        self.setLayout(VBox(
            HBox(QLabel("Brush:"), b),
            HBox(QLabel("Line:"),  l),
            HBox(QLabel("Font:"),  f),
            HBox(QLabel("Size:"),  s)
        ))

class SelectDrop(QPushButton):
    buttonClicked = pyqtSignal()
    dropClicked   = pyqtSignal()
    def __init__(self,  parent=None):
        super(SelectDrop, self).__init__(parent)
        self._pop_selector         = None   
        self._click_blocked        = False 
        self._hovered              = False
        self._main_button_hovered  = False
        self._drop_button_hovered  = False
        self._poped                = False
        self._button_brush         = QBrush(QColor("#E1E1E1"))
        self._button_pen           = QPen(QColor("#ADADAD"))
        self._button_hovered_brush = QBrush(QColor("#E5F1FB"))
        self._button_hovered_pen   = QPen(QColor("#0078D7"))
        self._triangle_brush       = QBrush(QColor("#ADADAD"))
        self._triangle_pen         = QPen(QColor("#565656"))
        self._triangle_spacing     = 22
        self._rect_margin          = 4.5
        self._triangle_pen.setWidthF(1.1)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy(5, 0, QSizePolicy.ComboBox))

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform,   True) 

        w, h, drop_size                    = self.size().width(), self.size().height(), (self._triangle_spacing-self._rect_margin)
        self._poped                        = self._pop_selector.isVisible() if (self._pop_selector) else False
        main_button_brush, main_button_pen = (self._button_hovered_brush, self._button_hovered_pen) if (self._main_button_hovered or self._poped) else (self._button_brush, self._button_pen)
        drop_button_brush, drop_button_pen = (self._button_hovered_brush, self._button_hovered_pen) if (self._drop_button_hovered or self._poped) else (self._button_brush, self._button_pen)
        triangle_brush, triangle_pen       = (QBrush(QColor("#0078D7")),  self._triangle_pen)       if (self._hovered or self._poped) else (QBrush(QColor("#ADADAD")), self._triangle_pen)

        if self._main_button_hovered:
            self._paint_button(w-drop_size, 0,   drop_size, h-1, painter, drop_button_brush, drop_button_pen)
            self._paint_button(          0, 0, w-drop_size, h-1, painter, main_button_brush, main_button_pen)
        else:
            self._paint_button(          0, 0, w-drop_size, h-1, painter, main_button_brush, main_button_pen)
            self._paint_button(w-drop_size, 0,   drop_size, h-1, painter, drop_button_brush, drop_button_pen)

        self._paint_triangle(w-(2*self._rect_margin), h/2+3, 4,  painter, triangle_brush, triangle_pen)
        self._draw_decorator(painter)
        painter.end()        

    def _paint_button(self, x, y, w, h, painter, brush, pen):
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawRect(x, y, w, h)

    def _paint_triangle(self, x, y, size, painter, brush, pen):
        painter.setBrush(brush)
        painter.setPen(pen)
        sl, ml   = (0.8 * size), (size * (3**0.5) / 2.2 )
        hex_poly = QPolygonF()        
        hex_poly.append(QPointF(x - sl, y - ml))
        hex_poly.append(QPointF(x, y))
        hex_poly.append(QPointF(x + sl, y - ml))
        painter.drawPolyline(hex_poly)

    def _draw_decorator(self, painter):
        pass

    def _pop_selector_tab(self):
        if self._pop_selector:
            corner             = self.mapToGlobal(self.rect().bottomLeft())
            self._pop_selector.hide_request.connect( self._hide_selector_tab)
            self._pop_selector.pop(corner)
            self._pop_selector.activateWindow()

    def _hide_selector_tab(self):
        if self._pop_selector:
            self._pop_selector.hide()
            if self._hovered : self._click_blocked = True


    
    def mousePressEvent(self, event):
        if not(self._click_blocked):
            if self._drop_button_hovered:
                self._pop_selector_tab()
                self.dropClicked.emit()
            if self._main_button_hovered:
                self.buttonClicked.emit()
        self._click_blocked = False

    def enterEvent(self, event):
        self._hovered = True
        self.update()     

    def leaveEvent(self, event):
        self._hovered, self._main_button_hovered, self._drop_button_hovered = False, False, False
        self.update()  

    def mouseMoveEvent(self, event):
        w, h, drop_size = self.size().width(), self.size().height(), (self._triangle_spacing-self._rect_margin)
        self._main_button_hovered, self._drop_button_hovered = (True, False) if (event.pos() in QRect(0, 0, w-drop_size, h) and self._hovered) else (False, True)
        self.update()       

class BrushSelectDrop(SelectDrop):
    valueChanged = pyqtSignal(Qt.BrushStyle)
    def __init__(self,  parent=None):
        super(BrushSelectDrop, self).__init__(parent)
        self._style                = Qt.SolidPattern
        self._texture_color        = "#333333"
        self._base_color           = "#FFFFFF"
        self._rect_texture_brush   = QBrush(QColor(self._texture_color))
        self._rect_base_brush      = QBrush(QColor(self._base_color))
        self._rect_pen             = QPen(QColor(self._texture_color)) 
        self._pop_selector         = BrushPopSelector()
        self._pop_selector.valueSelected.connect( lambda x : self.setStyle(x))

    def _draw_decorator(self, painter):
        w, h = self.size().width(), self.size().height()
        self._rect_texture_brush.setStyle(self._style)   
        painter.setBrush(self._rect_texture_brush)
        painter.setPen(self._rect_pen)
        painter.drawRect( self._rect_margin,  self._rect_margin, w-(2*self._rect_margin)-1-self._triangle_spacing, h-(2* self._rect_margin)-1)

    def setStyle(self, vals):
        self.style = vals

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, vals):
        if issubclass(type(vals), Qt.BrushStyle):
            self._style = vals
            self.valueChanged.emit(vals)
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, vals))

    @property
    def texture_color(self):
        return [QColor(self._texture_color).red(), QColor(self._texture_color).green(), QColor(self._texture_color).blue()]

    @texture_color.setter
    def texture_color(self, vals):
        if len(vals) == 3 and all([ 0<= val <=255 for val in vals]):
            if not(vals == self._texture_color):
                self._texture_color      = vals
                self._rect_texture_brush = QBrush(QColor(*vals))
                self._rect_pen           = QPen(QColor(*vals))
                self.update()
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, vals))

    @property
    def base_color(self):
        return [QColor(self._base_color).red(), QColor(self._base_color).green(), QColor(self._base_color).blue()]

    @base_color.setter
    def base_color(self, vals):
        if len(vals) == 3 and all([ 0<= val <=255 for val in vals]):
            if not(vals == self._base_color):
                self._base_color      = vals
                self._rect_base_brush = QBrush(QColor(*vals))
                self.update()
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, vals))

class LineSelectDrop(SelectDrop):
    valueChanged = pyqtSignal(Qt.BrushStyle)
    def __init__(self,  parent=None):
        super(LineSelectDrop, self).__init__(parent)
        self._style        = Qt.SolidLine
        self._pop_selector = LinePopSelector()
        self._line_pen     = QPen(QColor(333333))
        self._pop_selector.valueSelected.connect( lambda x : self.setStyle(x))

    def _draw_decorator(self, painter):
        w, h = self.size().width(), self.size().height()
        self._line_pen.setStyle(self._style)
        painter.setPen(self._line_pen)
        painter.drawLine(QPoint(5, h/2), QPoint(w-self._triangle_spacing-5, h/2))

    def setStyle(self, vals):
        self.style = vals

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, vals):
        if issubclass(type(vals), Qt.PenStyle):
            self._style = vals
            self.valueChanged.emit(vals)
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, vals))

class FontSelectDrop(QComboBox):    
    valueChanged = pyqtSignal(str)
    def __init__(self,  parent=None):
        super(FontSelectDrop, self).__init__(parent)
        self._itemModel = QStandardItemModel()

        for index, font_name in enumerate(QFontDatabase().families()):
            i = QStandardItem(font_name)
            f = QFont(font_name)
            f.setPointSize(12)
            i.setFont(f)
            self._itemModel.appendRow(i)
            self._itemModel.setData(self._itemModel.index(index, 0), QSize(20, 20), Qt.SizeHintRole)

        self.setModel(self._itemModel)
        self.setStyleSheet('''QComboBox QAbstractItemView {min-width: 300px;}''')
        self.currentIndexChanged.connect(lambda : self.valueChanged.emit(self.currentText()))

class SizeSelectDrop(QComboBox):    
    valueChanged = pyqtSignal(str)
    def __init__(self,  parent=None):
        super(SizeSelectDrop, self).__init__(parent)

        self._itemModel = QStandardItemModel()

        for index, size in enumerate(range(6, 91)):
            i = QStandardItem(str(size))
            f = QFont("Arial")
            f.setPointSize(8)
            i.setFont(f)
            self._itemModel.appendRow(i)
            self._itemModel.setData(self._itemModel.index(index, 0), QSize(20, 20), Qt.SizeHintRole)

        self.setModel(self._itemModel)
        self.currentIndexChanged.connect(lambda : self.valueChanged.emit(self.currentText()))

class PopSelector(QWidget):
    valueSelected = pyqtSignal(object)
    hide_request  = pyqtSignal()
    def __init__(self,  parent=None):
        super(PopSelector, self).__init__(parent)
        self._width              = 150
        self._height             = 150
        self._animation_duration = 150
        self._selected_value     = None
        self._clicked_pos        = None
        self._hover_pos          = None

        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""QWidget{border: 1px solid rgba(182, 188, 188, 182);}""")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.SubWindow | Qt.WindowStaysOnTopHint)
        

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform,   True) 
        self._draw_decorator(painter)
        painter.end()

    def _draw_decorator(self, painter):
        pass        
        
    def update(self):
        if self._selected_value:
            self.valueSelected.emit(self._selected_value)
            self.hide_request.emit()   
            self._selected_value = None     
            self._clicked_pos    = None            
        QWidget.update(self)

    def changeEvent(self, event):
        if event.type() == QEvent.ActivationChange and (not self.isActiveWindow()):
            self.hide_request.emit()

    def mousePressEvent(self, event):
        self._clicked_pos =  event.pos()
        self.update()       

    def mouseMoveEvent(self, event):
        self._hover_pos = event.pos()
        self.update()     

    def mouseReleaseEvent(self,  event):
        self.update()     

    def pop(self, point):
        x, y           = point.x(), point.y()
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(self._animation_duration)
        self.animation.setStartValue(QRect(x, y, self._width, 0))
        self.animation.setEndValue(QRect(x, y, self._width, self._height))
        QWidget.show(self)
        self.animation.start()
        
class BrushPopSelector(PopSelector):    
    valueSelected = pyqtSignal(object)
    def __init__(self,  parent=None):
        super(BrushPopSelector, self).__init__(parent)
        self._width        = 220
        self._height       = 480
        x, y, w, h, dx, dy = 0, 0, 60, 20, 70, 25
        self._pattern_list = [ 
            [x + ( dx * 0 ), y + ( dy * 0 ), w, h,     Qt.SolidPattern,  True],
            [x + ( dx * 1 ), y + ( dy * 0 ), w, h,    Qt.Dense1Pattern, False],
            [x + ( dx * 2 ), y + ( dy * 0 ), w, h,    Qt.Dense2Pattern, False],
            [x + ( dx * 0 ), y + ( dy * 1 ), w, h,    Qt.Dense3Pattern, False],
            [x + ( dx * 1 ), y + ( dy * 1 ), w, h,     Qt.FDiagPattern, False],
            [x + ( dx * 2 ), y + ( dy * 1 ), w, h,    Qt.Dense4Pattern, False],
            [x + ( dx * 0 ), y + ( dy * 2 ), w, h,    Qt.Dense5Pattern, False],
            [x + ( dx * 1 ), y + ( dy * 2 ), w, h,    Qt.Dense6Pattern, False],
            [x + ( dx * 2 ), y + ( dy * 2 ), w, h,    Qt.Dense7Pattern, False],
            [x + ( dx * 0 ), y + ( dy * 3 ), w, h, Qt.DiagCrossPattern, False],
            [x + ( dx * 1 ), y + ( dy * 3 ), w, h,       Qt.HorPattern, False],
            [x + ( dx * 2 ), y + ( dy * 3 ), w, h,       Qt.VerPattern, False],
            [x + ( dx * 0 ), y + ( dy * 4 ), w, h,     Qt.CrossPattern, False],
            [x + ( dx * 1 ), y + ( dy * 4 ), w, h,     Qt.BDiagPattern, False]
        ]

        x, y, w, h, dx, dy = 0, 0, 15, 15, 20, 15
        self._texture_list = [
            [x + (dx * 0), y + (dy * 0) - 5, w, h, "#FFFFFF", False],[x + (dx * 0), y + (dy * 1), w, h, "#F2F2F2", False],[x + (dx * 0), y + (dy * 2), w, h, "#D8D8D8", False],[x + (dx * 0), y + (dy * 3), w, h, "#BFBFBF", False],[x + (dx * 0), y + (dy * 4), w, h, "#A5A5A5", False],[x + (dx * 0), y + (dy * 5), w, h, "#7F7F7F", False],[x + (dx * 0), y + (dy * 6) + 5, w, h, "#C00000", False], #column  1
            [x + (dx * 1), y + (dy * 0) - 5, w, h, "#000000",  True],[x + (dx * 1), y + (dy * 1), w, h, "#595959", False],[x + (dx * 1), y + (dy * 2), w, h, "#3F3F3F", False],[x + (dx * 1), y + (dy * 3), w, h, "#262626", False],[x + (dx * 1), y + (dy * 4), w, h, "#0C0C0C", False],[x + (dx * 1), y + (dy * 5), w, h, "#060606", False],[x + (dx * 1), y + (dy * 6) + 5, w, h, "#FF0000", False], #column  2
            [x + (dx * 2), y + (dy * 0) - 5, w, h, "#FF0066", False],[x + (dx * 2), y + (dy * 1), w, h, "#FFCCE0", False],[x + (dx * 2), y + (dy * 2), w, h, "#FE99C1", False],[x + (dx * 2), y + (dy * 3), w, h, "#FF65A3", False],[x + (dx * 2), y + (dy * 4), w, h, "#BF004C", False],[x + (dx * 2), y + (dy * 5), w, h, "#7F0032", False],[x + (dx * 2), y + (dy * 6) + 5, w, h, "#FFC000", False], #column  3
            [x + (dx * 3), y + (dy * 0) - 5, w, h, "#FF6600", False],[x + (dx * 3), y + (dy * 1), w, h, "#FFE0CC", False],[x + (dx * 3), y + (dy * 2), w, h, "#FEC199", False],[x + (dx * 3), y + (dy * 3), w, h, "#FFA365", False],[x + (dx * 3), y + (dy * 4), w, h, "#BF4C00", False],[x + (dx * 3), y + (dy * 5), w, h, "#7F3200", False],[x + (dx * 3), y + (dy * 6) + 5, w, h, "#FCFC16", False], #column  4
            [x + (dx * 4), y + (dy * 0) - 5, w, h, "#FFcc00", False],[x + (dx * 4), y + (dy * 1), w, h, "#FFF2CC", False],[x + (dx * 4), y + (dy * 2), w, h, "#FEE599", False],[x + (dx * 4), y + (dy * 3), w, h, "#FFD965", False],[x + (dx * 4), y + (dy * 4), w, h, "#BF9000", False],[x + (dx * 4), y + (dy * 5), w, h, "#7F6000", False],[x + (dx * 4), y + (dy * 6) + 5, w, h, "#92D050", False], #column  5
            [x + (dx * 5), y + (dy * 0) - 5, w, h, "#FFFF00", False],[x + (dx * 5), y + (dy * 1), w, h, "#FFFFCC", False],[x + (dx * 5), y + (dy * 2), w, h, "#FFFE99", False],[x + (dx * 5), y + (dy * 3), w, h, "#FFFF65", False],[x + (dx * 5), y + (dy * 4), w, h, "#BFBF00", False],[x + (dx * 5), y + (dy * 5), w, h, "#7F7F00", False],[x + (dx * 5), y + (dy * 6) + 5, w, h, "#00B050", False], #column  6
            [x + (dx * 6), y + (dy * 0) - 5, w, h, "#92D050", False],[x + (dx * 6), y + (dy * 1), w, h, "#E9F5DC", False],[x + (dx * 6), y + (dy * 2), w, h, "#D3ECB9", False],[x + (dx * 6), y + (dy * 3), w, h, "#BDE295", False],[x + (dx * 6), y + (dy * 4), w, h, "#6DAA2D", False],[x + (dx * 6), y + (dy * 5), w, h, "#49711E", False],[x + (dx * 6), y + (dy * 6) + 5, w, h, "#00B0F0", False], #column  7
            [x + (dx * 7), y + (dy * 0) - 5, w, h, "#00B050", False],[x + (dx * 7), y + (dy * 1), w, h, "#BCFFDA", False],[x + (dx * 7), y + (dy * 2), w, h, "#79FFB6", False],[x + (dx * 7), y + (dy * 3), w, h, "#36FE91", False],[x + (dx * 7), y + (dy * 4), w, h, "#00843B", False],[x + (dx * 7), y + (dy * 5), w, h, "#005827", False],[x + (dx * 7), y + (dy * 6) + 5, w, h, "#0070C0", False], #column  8
            [x + (dx * 8), y + (dy * 0) - 5, w, h, "#00B0F0", False],[x + (dx * 8), y + (dy * 1), w, h, "#C9F0FE", False],[x + (dx * 8), y + (dy * 2), w, h, "#93E2FF", False],[x + (dx * 8), y + (dy * 3), w, h, "#5CD3FF", False],[x + (dx * 8), y + (dy * 4), w, h, "#0084B4", False],[x + (dx * 8), y + (dy * 5), w, h, "#005878", False],[x + (dx * 8), y + (dy * 6) + 5, w, h, "#002060", False], #column  9
            [x + (dx * 9), y + (dy * 0) - 5, w, h, "#0070C0", False],[x + (dx * 9), y + (dy * 1), w, h, "#BFE4FF", False],[x + (dx * 9), y + (dy * 2), w, h, "#7FCAFF", False],[x + (dx * 9), y + (dy * 3), w, h, "#40AFFF", False],[x + (dx * 9), y + (dy * 4), w, h, "#005390", False],[x + (dx * 9), y + (dy * 5), w, h, "#003760", False],[x + (dx * 9), y + (dy * 6) + 5, w, h, "#A380C0", False]  #column 10
        ]
        

        self._color_list   = [
            [x + (dx * 0), y + (dy * 0) - 5, w, h, "#FFFFFF",  True],[x + (dx * 0), y + (dy * 1), w, h, "#F2F2F2", False],[x + (dx * 0), y + (dy * 2), w, h, "#D8D8D8", False],[x + (dx * 0), y + (dy * 3), w, h, "#BFBFBF", False],[x + (dx * 0), y + (dy * 4), w, h, "#A5A5A5", False],[x + (dx * 0), y + (dy * 5), w, h, "#7F7F7F", False],[x + (dx * 0), y + (dy * 6) + 5, w, h, "#C00000", False], #column  1
            [x + (dx * 1), y + (dy * 0) - 5, w, h, "#000000", False],[x + (dx * 1), y + (dy * 1), w, h, "#595959", False],[x + (dx * 1), y + (dy * 2), w, h, "#3F3F3F", False],[x + (dx * 1), y + (dy * 3), w, h, "#262626", False],[x + (dx * 1), y + (dy * 4), w, h, "#0C0C0C", False],[x + (dx * 1), y + (dy * 5), w, h, "#060606", False],[x + (dx * 1), y + (dy * 6) + 5, w, h, "#FF0000", False], #column  2
            [x + (dx * 2), y + (dy * 0) - 5, w, h, "#FF0066", False],[x + (dx * 2), y + (dy * 1), w, h, "#FFCCE0", False],[x + (dx * 2), y + (dy * 2), w, h, "#FE99C1", False],[x + (dx * 2), y + (dy * 3), w, h, "#FF65A3", False],[x + (dx * 2), y + (dy * 4), w, h, "#BF004C", False],[x + (dx * 2), y + (dy * 5), w, h, "#7F0032", False],[x + (dx * 2), y + (dy * 6) + 5, w, h, "#FFC000", False], #column  3
            [x + (dx * 3), y + (dy * 0) - 5, w, h, "#FF6600", False],[x + (dx * 3), y + (dy * 1), w, h, "#FFE0CC", False],[x + (dx * 3), y + (dy * 2), w, h, "#FEC199", False],[x + (dx * 3), y + (dy * 3), w, h, "#FFA365", False],[x + (dx * 3), y + (dy * 4), w, h, "#BF4C00", False],[x + (dx * 3), y + (dy * 5), w, h, "#7F3200", False],[x + (dx * 3), y + (dy * 6) + 5, w, h, "#FCFC16", False], #column  4
            [x + (dx * 4), y + (dy * 0) - 5, w, h, "#FFcc00", False],[x + (dx * 4), y + (dy * 1), w, h, "#FFF2CC", False],[x + (dx * 4), y + (dy * 2), w, h, "#FEE599", False],[x + (dx * 4), y + (dy * 3), w, h, "#FFD965", False],[x + (dx * 4), y + (dy * 4), w, h, "#BF9000", False],[x + (dx * 4), y + (dy * 5), w, h, "#7F6000", False],[x + (dx * 4), y + (dy * 6) + 5, w, h, "#92D050", False], #column  5
            [x + (dx * 5), y + (dy * 0) - 5, w, h, "#FFFF00", False],[x + (dx * 5), y + (dy * 1), w, h, "#FFFFCC", False],[x + (dx * 5), y + (dy * 2), w, h, "#FFFE99", False],[x + (dx * 5), y + (dy * 3), w, h, "#FFFF65", False],[x + (dx * 5), y + (dy * 4), w, h, "#BFBF00", False],[x + (dx * 5), y + (dy * 5), w, h, "#7F7F00", False],[x + (dx * 5), y + (dy * 6) + 5, w, h, "#00B050", False], #column  6
            [x + (dx * 6), y + (dy * 0) - 5, w, h, "#92D050", False],[x + (dx * 6), y + (dy * 1), w, h, "#E9F5DC", False],[x + (dx * 6), y + (dy * 2), w, h, "#D3ECB9", False],[x + (dx * 6), y + (dy * 3), w, h, "#BDE295", False],[x + (dx * 6), y + (dy * 4), w, h, "#6DAA2D", False],[x + (dx * 6), y + (dy * 5), w, h, "#49711E", False],[x + (dx * 6), y + (dy * 6) + 5, w, h, "#00B0F0", False], #column  7
            [x + (dx * 7), y + (dy * 0) - 5, w, h, "#00B050", False],[x + (dx * 7), y + (dy * 1), w, h, "#BCFFDA", False],[x + (dx * 7), y + (dy * 2), w, h, "#79FFB6", False],[x + (dx * 7), y + (dy * 3), w, h, "#36FE91", False],[x + (dx * 7), y + (dy * 4), w, h, "#00843B", False],[x + (dx * 7), y + (dy * 5), w, h, "#005827", False],[x + (dx * 7), y + (dy * 6) + 5, w, h, "#0070C0", False], #column  8
            [x + (dx * 8), y + (dy * 0) - 5, w, h, "#00B0F0", False],[x + (dx * 8), y + (dy * 1), w, h, "#C9F0FE", False],[x + (dx * 8), y + (dy * 2), w, h, "#93E2FF", False],[x + (dx * 8), y + (dy * 3), w, h, "#5CD3FF", False],[x + (dx * 8), y + (dy * 4), w, h, "#0084B4", False],[x + (dx * 8), y + (dy * 5), w, h, "#005878", False],[x + (dx * 8), y + (dy * 6) + 5, w, h, "#002060", False], #column  9
            [x + (dx * 9), y + (dy * 0) - 5, w, h, "#0070C0", False],[x + (dx * 9), y + (dy * 1), w, h, "#BFE4FF", False],[x + (dx * 9), y + (dy * 2), w, h, "#7FCAFF", False],[x + (dx * 9), y + (dy * 3), w, h, "#40AFFF", False],[x + (dx * 9), y + (dy * 4), w, h, "#005390", False],[x + (dx * 9), y + (dy * 5), w, h, "#003760", False],[x + (dx * 9), y + (dy * 6) + 5, w, h, "#A380C0", False]  #column 10
        ]

        self._rect_brush      = QBrush(QColor("#333333"))
        self._rect_pen        = QPen(QColor("#333333"))     
        self._hovered_pen     = QPen(QColor("#0078D7"))
        self._hovered_brush   = QBrush(QColor("#E5F1FB"))
        self._text_pen        = QPen(QColor("#000000"))
        self._text_rect_brush = QBrush(QColor("#DDDDDD"))
        self._text_rect_pen   = QPen(QColor("#BBBBBB"))
        self._rect_pen.setWidth(1)

    def  _draw_decorator(self, painter):
        self._draw_pattern(     painter, 10,   5, self._pattern_list, "Pattern style")
        self._draw_color_bundle(painter, 10, 160, self._texture_list, "Texture color")
        self._draw_color_bundle(painter, 10, 350, self._color_list,   "Base color")

    def _draw_pattern(self, painter, x, y, pattern_list, text, spacing = 25):
        self._draw_text_label(painter, x-2, y, text)

        for rect_set in pattern_list:
            rx, ry, rw, rh, style, selected = rect_set
            rx, ry                          = rx + x, ry + y + spacing
            self._selected_value            = style if (self._clicked_pos and (self._clicked_pos in QRect(rx, ry, rw, rh))) else self._selected_value
            pen, brush, style               = (self._hovered_pen, self._hovered_brush, style) if (self._hover_pos and self._hover_pos in QRect(rx, ry, rw, rh)) else (Qt.NoPen, Qt.NoBrush, style)
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRect(rx-3, ry-3, rw+4, rh+4)

            self._rect_brush.setStyle(style)
            painter.setPen(self._rect_pen)
            painter.setBrush(self._rect_brush)
            painter.drawRect(rx, ry, rw-3, rh-3)    

    def _draw_color_bundle(self, painter, x, y, item_list, text, spacing = 30):
        selected_rect  = None
        selected_color = None
        hovered_rect   = None
        hovered_color  = None
        self._draw_text_label(painter, x-2, y, text)     

        valid_selection = False
        for rect_set in item_list:
            rx, ry, rw, rh = rect_set[0:4]
            if (self._clicked_pos and QRect((rx + x), (ry + y + spacing), rw, rh).contains(self._clicked_pos)):
                valid_selection = True  
                break

        for index, rect_set in enumerate(item_list):
            rx, ry, rw, rh, color, selected = rect_set
            rx, ry = (rx + x), (ry + y + spacing)
            
            if valid_selection:
                item_list[index][5] = True if (self._clicked_pos and QRect(rx, ry, rw, rh).contains(self._clicked_pos)) else False

            if item_list[index][5] == True:
                selected_color, selected_rect = color, (rx, ry, rw, rh)

            if (self._hover_pos and QRect(rx, ry, rw, rh).contains(self._hover_pos)):
                hovered_color, hovered_rect = color, (rx, ry, rw, rh)

            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(color))
            painter.drawRect(rx,ry,rw,rh) 
            painter.drawRect(x, y + 150, 195, 20)

        if selected_rect:
            x, y, w, h = selected_rect
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QColor("#FFFFFF"))
            painter.drawRect(QRect(x + 1, y + 1, w - 2, h - 2))
            painter.setPen(self._hovered_pen)
            painter.drawRect(QRect(x, y, w, h)) 

        if hovered_rect :
            x, y, w, h = hovered_rect
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QColor("#FFFFFF"))
            painter.drawRect(QRect(x + 1, y + 1, w - 2, h - 2))
            painter.setPen(self._hovered_pen)
            painter.drawRect(QRect(x, y, w, h))

    def _draw_text_label(self, painter, x, y, text):
        painter.setBrush(self._text_rect_brush)
        painter.setPen(self._text_rect_pen)
        painter.drawRect(x, y, (self._width - 20), 20)
        painter.setPen(self._text_pen)
        painter.drawText(x + 5, y, (self._width - 20), 20, Qt.AlignLeft|Qt.AlignVCenter, text)

    @property
    def value(self):
        return self._selected_value

class ColorPopWidget(QWidget):
    valueSelected = pyqtSignal(object)
    def __init__(self,  parent=None):
        super(ColorPopWidget, self).__init__(parent)
        k = QPushButton(">")
        k.setFixedSize(QSize(20, 20))
        self.setLayout(VBox(
            ColorPalletLite(), 
            HBox(
                ColorPalletCustom(), 
                ColorTextEdit("FFAADA"),
                5,
                k,
                10
            ).setContentsMargins(0, 0, 0, 0).setSpacing(0),
            -1
        ).setContentsMargins(0, 0, 0, 0))
        self.resize(200, 200)
        
class ColorTextEdit(QLineEdit):
    def __init__(self,  parent=None):
        super(ColorTextEdit, self).__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setInputMask(r"\#>HHHHHH")
        self.setTextMargins(0,0,0,0)
        self.setFixedHeight(17)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setFont(QFont("consolas", weight = 55))
        # self.textChanged.connect(lambda : self.update_palette())


class ColorPalletLite(PopSelector):
    valueSelected = pyqtSignal(object)
    def __init__(self,  parent=None):
        super(ColorPalletLite, self).__init__(parent)   
        x, y, w, h, dx, dy = 10, 15, 15, 15, 20, 15
        self._color_list = [
            [x + (dx * 0), y + (dy * 0) - 5, w, h, "#FFFFFF", False],[x + (dx * 0), y + (dy * 1), w, h, "#F2F2F2", False],[x + (dx * 0), y + (dy * 2), w, h, "#D8D8D8", False],[x + (dx * 0), y + (dy * 3), w, h, "#BFBFBF", False],[x + (dx * 0), y + (dy * 4), w, h, "#A5A5A5", False],[x + (dx * 0), y + (dy * 5), w, h, "#7F7F7F", False],[x + (dx * 0), y + (dy * 6) + 5, w, h, "#C00000", False], #column  1
            [x + (dx * 1), y + (dy * 0) - 5, w, h, "#000000",  True],[x + (dx * 1), y + (dy * 1), w, h, "#595959", False],[x + (dx * 1), y + (dy * 2), w, h, "#3F3F3F", False],[x + (dx * 1), y + (dy * 3), w, h, "#262626", False],[x + (dx * 1), y + (dy * 4), w, h, "#0C0C0C", False],[x + (dx * 1), y + (dy * 5), w, h, "#060606", False],[x + (dx * 1), y + (dy * 6) + 5, w, h, "#FF0000", False], #column  2
            [x + (dx * 2), y + (dy * 0) - 5, w, h, "#FF0066", False],[x + (dx * 2), y + (dy * 1), w, h, "#FFCCE0", False],[x + (dx * 2), y + (dy * 2), w, h, "#FE99C1", False],[x + (dx * 2), y + (dy * 3), w, h, "#FF65A3", False],[x + (dx * 2), y + (dy * 4), w, h, "#BF004C", False],[x + (dx * 2), y + (dy * 5), w, h, "#7F0032", False],[x + (dx * 2), y + (dy * 6) + 5, w, h, "#FFC000", False], #column  3
            [x + (dx * 3), y + (dy * 0) - 5, w, h, "#FF6600", False],[x + (dx * 3), y + (dy * 1), w, h, "#FFE0CC", False],[x + (dx * 3), y + (dy * 2), w, h, "#FEC199", False],[x + (dx * 3), y + (dy * 3), w, h, "#FFA365", False],[x + (dx * 3), y + (dy * 4), w, h, "#BF4C00", False],[x + (dx * 3), y + (dy * 5), w, h, "#7F3200", False],[x + (dx * 3), y + (dy * 6) + 5, w, h, "#FCFC16", False], #column  4
            [x + (dx * 4), y + (dy * 0) - 5, w, h, "#FFcc00", False],[x + (dx * 4), y + (dy * 1), w, h, "#FFF2CC", False],[x + (dx * 4), y + (dy * 2), w, h, "#FEE599", False],[x + (dx * 4), y + (dy * 3), w, h, "#FFD965", False],[x + (dx * 4), y + (dy * 4), w, h, "#BF9000", False],[x + (dx * 4), y + (dy * 5), w, h, "#7F6000", False],[x + (dx * 4), y + (dy * 6) + 5, w, h, "#92D050", False], #column  5
            [x + (dx * 5), y + (dy * 0) - 5, w, h, "#FFFF00", False],[x + (dx * 5), y + (dy * 1), w, h, "#FFFFCC", False],[x + (dx * 5), y + (dy * 2), w, h, "#FFFE99", False],[x + (dx * 5), y + (dy * 3), w, h, "#FFFF65", False],[x + (dx * 5), y + (dy * 4), w, h, "#BFBF00", False],[x + (dx * 5), y + (dy * 5), w, h, "#7F7F00", False],[x + (dx * 5), y + (dy * 6) + 5, w, h, "#00B050", False], #column  6
            [x + (dx * 6), y + (dy * 0) - 5, w, h, "#92D050", False],[x + (dx * 6), y + (dy * 1), w, h, "#E9F5DC", False],[x + (dx * 6), y + (dy * 2), w, h, "#D3ECB9", False],[x + (dx * 6), y + (dy * 3), w, h, "#BDE295", False],[x + (dx * 6), y + (dy * 4), w, h, "#6DAA2D", False],[x + (dx * 6), y + (dy * 5), w, h, "#49711E", False],[x + (dx * 6), y + (dy * 6) + 5, w, h, "#00B0F0", False], #column  7
            [x + (dx * 7), y + (dy * 0) - 5, w, h, "#00B050", False],[x + (dx * 7), y + (dy * 1), w, h, "#BCFFDA", False],[x + (dx * 7), y + (dy * 2), w, h, "#79FFB6", False],[x + (dx * 7), y + (dy * 3), w, h, "#36FE91", False],[x + (dx * 7), y + (dy * 4), w, h, "#00843B", False],[x + (dx * 7), y + (dy * 5), w, h, "#005827", False],[x + (dx * 7), y + (dy * 6) + 5, w, h, "#0070C0", False], #column  8
            [x + (dx * 8), y + (dy * 0) - 5, w, h, "#00B0F0", False],[x + (dx * 8), y + (dy * 1), w, h, "#C9F0FE", False],[x + (dx * 8), y + (dy * 2), w, h, "#93E2FF", False],[x + (dx * 8), y + (dy * 3), w, h, "#5CD3FF", False],[x + (dx * 8), y + (dy * 4), w, h, "#0084B4", False],[x + (dx * 8), y + (dy * 5), w, h, "#005878", False],[x + (dx * 8), y + (dy * 6) + 5, w, h, "#002060", False], #column  9
            [x + (dx * 9), y + (dy * 0) - 5, w, h, "#0070C0", False],[x + (dx * 9), y + (dy * 1), w, h, "#BFE4FF", False],[x + (dx * 9), y + (dy * 2), w, h, "#7FCAFF", False],[x + (dx * 9), y + (dy * 3), w, h, "#40AFFF", False],[x + (dx * 9), y + (dy * 4), w, h, "#005390", False],[x + (dx * 9), y + (dy * 5), w, h, "#003760", False],[x + (dx * 9), y + (dy * 6) + 5, w, h, "#A380C0", False]  #column 10
        ]

        self._rect_brush      = QBrush(QColor("#333333"))
        self._hovered_brush   = QBrush(QColor("#E5F1FB"))
        self._text_rect_brush = QBrush(QColor("#DDDDDD"))
        self._rect_pen        = QPen(QColor("#333333"))     
        self._hovered_pen     = QPen(QColor("#0078D7"))
        self._text_pen        = QPen(QColor("#000000"))
        self._text_rect_pen   = QPen(QColor("#BBBBBB"))
        self._rect_pen.setWidth(1)
        self.setStyleSheet("""QWidget{border: 0px solid rgba(182, 188, 188, 182);}""")
        self.setFixedSize(QSize(215, 110))

    def  _draw_decorator(self, painter):
        item_list      = self._color_list
        selected_rect  = None
        selected_color = None
        hovered_rect   = None
        hovered_color  = None

        valid_selection = False
        for rect_set in item_list:
            if (self._clicked_pos and QRect(*rect_set[0:4]).contains(self._clicked_pos)):
                valid_selection = True  
                break

        for index, rect_set in enumerate(item_list):
            x, y, w, h, color, selected = rect_set
            
            if valid_selection:
                item_list[index][5] = True if (self._clicked_pos and QRect(x, y, w, h).contains(self._clicked_pos)) else False

            if item_list[index][5] == True:
                selected_color, selected_rect = color, (x, y, w, h)

            if (self._hover_pos and QRect(x, y, w, h).contains(self._hover_pos)):
                hovered_color, hovered_rect = color, (x, y, w, h)

            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(color))
            painter.drawRect(x, y, w, h) 

        if selected_rect:
            x, y, w, h = selected_rect
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QColor("#FFFFFF"))
            painter.drawRect(QRect(x + 1, y + 1, w - 2, h - 2))
            painter.setPen(self._hovered_pen)
            painter.drawRect(QRect(x, y, w, h)) 

        if hovered_rect :
            x, y, w, h = hovered_rect
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QColor("#FFFFFF"))
            painter.drawRect(QRect(x + 1, y + 1, w - 2, h - 2))
            painter.setPen(self._hovered_pen)
            painter.drawRect(QRect(x, y, w, h))


class ColorPalletCustom(PopSelector):
    valueSelected = pyqtSignal(object)
    valueChanged  = pyqtSignal(object)
    def __init__(self,  parent=None):
        super(ColorPalletCustom, self).__init__(parent)   
        x, y, w, h, dx, dy = 10, 10, 15, 15, 20, 15 
        self._custom_rect = [x + (dx * 0), y + (dy * 0) - 5, w, h, "#23ff32", False]

        self._rect_brush      = QBrush(QColor("#333333"))
        self._hovered_brush   = QBrush(QColor("#E5F1FB"))
        self._text_rect_brush = QBrush(QColor("#DDDDDD"))
        self._rect_pen        = QPen(QColor("#333333"))     
        self._hovered_pen     = QPen(QColor("#0078D7"))
        self._text_pen        = QPen(QColor("#000000"))
        self._text_rect_pen   = QPen(QColor("#BBBBBB"))
        self._rect_pen.setWidth(1)
        self.setFixedSize(QSize(30, 25))
        self.setStyleSheet("""QWidget{border: 0px solid rgba(182, 188, 188, 182);}""")
        a = QColor("#Fa32DD")
        print(a.name())

    def  _draw_decorator(self, painter):
        selected_rect  = None
        selected_color = None
        hovered_rect   = None
        hovered_color  = None

        x, y, w, h, color, selected   = self._custom_rect
        self._custom_rect[5]          = True if (self._clicked_pos and QRect(x, y, w, h).contains(self._clicked_pos)) else False
        selected_color, selected_rect = (color, (x, y, w, h)) if self._custom_rect[5] == True else (selected_color, selected_rect)
        hovered_color, hovered_rect   = (color, (x, y, w, h)) if (self._hover_pos and QRect(x, y, w, h).contains(self._hover_pos)) else (hovered_color, hovered_rect)
             
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(color))
        painter.drawRect(x, y, w, h) 

        if selected_rect:
            x, y, w, h = selected_rect
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QColor("#FFFFFF"))
            painter.drawRect(QRect(x + 1, y + 1, w - 2, h - 2))
            painter.setPen(self._hovered_pen)
            painter.drawRect(QRect(x, y, w, h)) 

        if hovered_rect :
            x, y, w, h = hovered_rect
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QColor("#FFFFFF"))
            painter.drawRect(QRect(x + 1, y + 1, w - 2, h - 2))
            painter.setPen(self._hovered_pen)
            painter.drawRect(QRect(x, y, w, h))

    def setSelected(self, val):
        self.selected = val

    @property
    def selected(self):
        return self._custom_rect[5]

    @selected.setter
    def selected(self, val):
        if val in (True, False):
            self._custom_rect[5] = val
            if val : self.valueSelected.emit(self._custom_rect[4])
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, val))
        self.update()


    def setColor(self, val):
        self.color = val

    @property
    def color(self):
        return self._custom_rect[4]

    @color.setter
    def color(self, val):
        if type(val) == QColor:
            self._prim_color = prim_color.name()
        elif type(val) == str:
            self._prim_color = QColor(prim_color).name()
        else:
            raise TypeError("%s TypeError: %s" % (inspect.stack()[1].function, val))


class LinePopSelector(PopSelector):    
    valueSelected = pyqtSignal(object)
    def __init__(self,  parent=None):
        super(LinePopSelector, self).__init__(parent)
        self._width       = 140
        self._height      = 140
        self._line_margin = 5
        x, y, w, h, dy = 10, 10, 120, 25, 25

        self._pattern_list = [ 
            [x, y + ( dy * 0 ), w, h,      Qt.SolidLine],
            [x, y + ( dy * 1 ), w, h,       Qt.DashLine],
            [x, y + ( dy * 2 ), w, h,        Qt.DotLine],
            [x, y + ( dy * 3 ), w, h,    Qt.DashDotLine],
            [x, y + ( dy * 4 ), w, h, Qt.DashDotDotLine]
        ]

        self._hovered_brush = QBrush(QColor("#E5F1FB"))
        self._hovered_pen   = QPen(QColor("#0078D7"))        
        self._line_pen      = QPen(QColor("#333333"))

    def  _draw_decorator(self, painter):
        for line_set in self._pattern_list:
            x, y, w, h, style    = line_set
            self._selected_value = style if (self._clicked_pos and (self._clicked_pos in QRect(x, y, w, h))) else self._selected_value
            pen, brush, style    = (self._hovered_pen, self._hovered_brush, style) if (self._hover_pos and self._hover_pos in QRect(x, y, w, h)) else (Qt.NoPen, Qt.NoBrush, style)
            painter.setPen(pen)
            painter.setBrush(brush)
            painter.drawRect(x, y, w-3, h-3)
            self._line_pen.setStyle(style)
            painter.setPen(self._line_pen)
            painter.drawLine(QPoint((x + self._line_margin), (y + h/2)), QPoint((x + w - (2 * self._line_margin)), (y + h/2)))


    @property
    def value(self):
        return self._selected_value

if __name__ == "__main__":
    def Debugger():

        app  = QApplication(sys.argv)
        form = ColorPopWidget()
        # form = m()
        form.show()
        app.exec_()

    Debugger()