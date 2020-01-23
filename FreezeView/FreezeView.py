import os
import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from CursorTracker   import CursorTracker

class FreezeView(QTableView):
	horizontal_header_resized = pyqtSignal(int, int, int)
	vertical_header_resized   = pyqtSignal(int, int, int)
	mouse_move_signal         = pyqtSignal(QMouseEvent)
	mouse_press_signal        = pyqtSignal(QMouseEvent)
	mouse_release_signal      = pyqtSignal(QMouseEvent)
	top, left, corner         = 0, 1, 2
	def __init__(self, orentation, start_column_index, end_column_index, start_row_index, end_row_index, parent):
		QTableView.__init__(self, parent)
		assert isinstance(parent, QTableView)
		assert orentation in [FreezeView.left, FreezeView.top, FreezeView.corner]
		self.resizable            = False
		self.start_column_index   = start_column_index
		self.start_row_index      = start_row_index
		self.end_column_index     = end_column_index
		self.end_row_index        = end_row_index
		self.parent               = parent
		self.orentation           = orentation
		self.freeze_hiddin_row    = []
		self.freeze_hiddin_column = []
		self.border_width         = 1
		self.border_color		  = "#ccffcc"
		self.parent_scroll_mode   = {"vertical":None, "horizontal":None}
		self.mouse_anchor         = object()
		self.initiallize_mouse_anchor()
		self.initiallize_header()

		self.set_border_style()
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)	
		self.show()
	

	def showEvent(self, event):
		QTableView.showEvent(self, event)
		#must initiallize geroetry before resizable is set true, otherwise will receive "set 0 width error"
		#must be called after show event, or the visibility of header will always return false
		self.initiallize_geometry()

	def set_border_style(self):
		if self.orentation == FreezeView.left:
			self.setStyleSheet('''
				FreezeView{
					border: none;
					border-top: 0px;
					border-left: 0px;
					border-right: %dpx solid %s;
					border-bottom: 0px;
			}''' % (self.border_width, self.border_color))

		if self.orentation == FreezeView.top:
			self.setStyleSheet('''
				FreezeView{
					border: none;

					border-top: 0px;
					border-left: 0px;
					border-right: 0px;
					border-bottom: %dpx solid %s;
			}''' % (self.border_width, self.border_color))

		if self.orentation == FreezeView.corner:
			self.setStyleSheet('''
				FreezeView{
					border: none;
					border-top: 0px;
					border-left: 0px;
					border-right: %dpx solid  %s;
					border-bottom: %dpx solid  %s;
			}''' %(self.border_width, self.border_color, self.border_width, self.border_color))

	def initiallize_header(self):
		if self.orentation == FreezeView.left:
			self.horizontalHeader().setHidden(self.parent.horizontalHeader().isHidden())
			self.verticalHeader().hide()

		if self.orentation == FreezeView.top:
			self.verticalHeader().setHidden(self.parent.verticalHeader().isHidden())
			self.horizontalHeader().hide()
			
		if self.orentation == FreezeView.corner:
			self.horizontalHeader().hide()
			self.verticalHeader().hide()

	def connect_to_views(self):
		self.resizable = True
		parent         = self.parent
		self.horizontalHeader().sectionResized.connect(lambda column, old_size, new_size : self.increament_width(  new_size - old_size))
		self.verticalHeader().sectionResized.connect  (lambda    row, old_size, new_size : self.increament_height( new_size - old_size))
		if self.orentation == FreezeView.left:
			if parent.corner_frozen_view : self.horizontalHeader().sectionResized.connect(  lambda column, old_size, new_size : parent.corner_frozen_view.setColumnWidth(column, new_size))
			if parent.top_frozen_view    : self.horizontalHeader().sectionResized.connect(  lambda column, old_size, new_size : parent.top_frozen_view.setColumnWidth(column, new_size))
			if parent                    : self.horizontalHeader().sectionResized.connect(  lambda column, old_size, new_size : parent.setColumnWidth(column, new_size))
			if parent                    : parent.verticalHeader().sectionResized.connect(self.initiallize_geometry)
			if parent                    : parent.horizontalHeader().sectionResized.connect( self.initiallize_geometry)
			if parent                    : parent.verticalScrollBar().valueChanged.connect( self.verticalScrollBar().setValue)
			self.verticalScrollBar().valueChanged.connect(parent.verticalScrollBar().setValue)

		if self.orentation == FreezeView.top:
			if parent                    : parent.horizontalScrollBar().valueChanged.connect(self.horizontalScrollBar().setValue)			
			if parent.corner_frozen_view : self.verticalHeader().sectionResized.connect(    lambda    row, old_size, new_size : parent.corner_frozen_view.setRowHeight(row, new_size))
			if parent.left_frozen_view   : self.verticalHeader().sectionResized.connect(    lambda    row, old_size, new_size : parent.left_frozen_view.setRowHeight(row, new_size))
			if parent                    : self.verticalHeader().sectionResized.connect(    lambda    row, old_size, new_size : parent.setRowHeight(row, new_size))
			if parent                    : parent.horizontalHeader().sectionResized.connect( self.initiallize_geometry)
			if parent                    : parent.verticalHeader().sectionResized.connect(self.initiallize_geometry)
			if parent                    : parent.horizontalScrollBar().valueChanged.connect(self.horizontalScrollBar().setValue)	
			self.horizontalScrollBar().valueChanged.connect(parent.horizontalScrollBar().setValue)
		parent.horizontalHeader().geometriesChanged.connect(self.initiallize_geometry)
		parent.verticalHeader().geometriesChanged.connect(self.initiallize_geometry)
		parent.data_updated.connect(self.initiallize_geometry)
		parent.columns_removed.connect(self.remove_columns)
		parent.rows_removed.connect(self.remove_rows)
		# parent.column_inserted.connect(self.insert_column_at)
		# parent.row_inserted.connect(self.insert_row_at)

		parent.vscroll_mode_changed.connect(self.setVerticalScrollMode)
		parent.hscroll_mode_changed.connect(self.setHorizontalScrollMode)

		self.mouse_press_signal.connect(parent.cursor_tracker.set_anchor)
		self.mouse_move_signal.connect(parent.cursor_tracker.set_pivot)
		self.mouse_release_signal.connect(parent.cursor_tracker.clear_points)
		self.setSelectionModel(parent.selectionModel())



	def disconnect_to_views(self):
		self.resizable = False
		parent         = self.parent
		if self.orentation == FreezeView.left:
			self.verticalScrollBar().valueChanged.disconnect()
			self.horizontalHeader().sectionResized.disconnect()
			parent.verticalScrollBar().valueChanged.disconnect( self.verticalScrollBar().setValue)
			parent.verticalHeader().sectionResized.disconnect(self.initiallize_geometry)
			parent.horizontalHeader().sectionResized.disconnect(self.initiallize_geometry)
		if self.orentation == FreezeView.top:
			self.horizontalScrollBar().valueChanged.disconnect()
			self.verticalHeader().sectionResized.disconnect()
			parent.horizontalScrollBar().valueChanged.disconnect(self.horizontalScrollBar().setValue)	
			parent.verticalHeader().sectionResized.disconnect(self.initiallize_geometry)
			parent.horizontalHeader().sectionResized.disconnect(self.initiallize_geometry)

		parent.data_updated.disconnect(self.initiallize_geometry)
		parent.columns_removed.disconnect(self.remove_columns)
		parent.rows_removed.disconnect(self.remove_rows)
		# parent.column_inserted.disconnect(self.insert_column_at)
		# parent.row_inserted.disconnect(self.insert_row_at)

		parent.vscroll_mode_changed.disconnect(self.setVerticalScrollMode)
		parent.hscroll_mode_changed.disconnect(self.setHorizontalScrollMode)

		self.mouse_press_signal.disconnect(parent.cursor_tracker.set_anchor)
		self.mouse_move_signal.disconnect(parent.cursor_tracker.set_pivot)
		self.mouse_release_signal.disconnect(parent.cursor_tracker.clear_points)
		self.show_freezed_area()
		self.deleteLater()

	def update_data_model(self, data_model):
		self.setModel(data_model)

	def columnResized(self, column, oldWidth, newWidth):
		QTableView.columnWidth(column, oldWidth, newWidth)

	def resizeEvent(self, event):
		QTableView.resizeEvent(self, event)
		# self.updateFrozenTableGeometry()/////////////////////////////////////required

	def moveCursor(self, cursorAction, modifiers):
		print("AAAAAAAA")
		parent = self.parent 
		current = QTableView.moveCursor(parent, cursorAction, modifiers)
		if cursorAction == parent.MoveLeft and current.column() > 1 and parent.visualRect(current).topLeft().x() < (self.columnWidth(0) + self.columnWidth(1)):
			newValue = parent.horizontalScrollBar().value() + parent.visualRect(current).topLeft().x() - (self.columnWidth(0) + self.columnWidth(1))
			parent.horizontalScrollBar().setValue(newValue) # todo not best pratice
		return current
		
	def initiallize_geometry(self):
		self.initiallize_header() #init_header if parent header visibility changed
		self.setModel(self.parent.model())
		self.set_scroll_mode_constrain()

		parent               = self.parent
		x_header_offset      = parent.verticalHeader().width()    *  (self.verticalHeader().isHidden()   - parent.verticalHeader().isHidden())
		y_header_offset      = parent.horizontalHeader().height() *  (self.horizontalHeader().isHidden() - parent.horizontalHeader().isHidden())
		x                    = parent.frameWidth() + x_header_offset 
		y                    = parent.frameWidth() + y_header_offset 
		w                    = parent.verticalHeader().width()    *  self.verticalHeader().isVisible()
		h                    = parent.horizontalHeader().height() *  self.horizontalHeader().isVisible()

		print (self.orentation, w, h, self.verticalHeader().isVisible(), self.horizontalHeader().isVisible())
		if self.orentation == FreezeView.top:
			w =  w + parent.viewport().width()   
			h =  h + sum([parent.rowHeight(row_index)      for row_index    in range(   self.start_row_index,      self.end_row_index)]) + self.border_width                   
		if self.orentation == FreezeView.left:
			w =  w + sum([parent.columnWidth(column_index) for column_index in range(self.start_column_index,   self.end_column_index)]) + self.border_width
			h =  h + parent.viewport().height()
		if self.orentation == FreezeView.corner:
			w =  w + sum([parent.columnWidth(column_index) for column_index in range(self.start_column_index,   self.end_column_index)]) + self.border_width
			h =  h + sum([parent.rowHeight(row_index)      for row_index    in range(   self.start_row_index,      self.end_row_index)]) + self.border_width
		self.hide_freezed_area()
		self.set_size( x, y, w, h)
		self.relesae_scroll_mode_constrain()
	

	def set_scroll_mode_constrain(self):
		parent = self.parent
		self.parent_scroll_mode = {"vertical":parent.verticalScrollMode(), "horizontal":parent.horizontalScrollMode()}
		parent.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
		parent.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
		self.setVerticalScrollMode(QAbstractItemView.ScrollPerItem)
		self.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)

	
	def relesae_scroll_mode_constrain(self):
		parent = self.parent
		parent.setVerticalScrollMode(self.parent_scroll_mode["vertical"])
		parent.setHorizontalScrollMode(self.parent_scroll_mode["horizontal"])
		self.setVerticalScrollMode(self.parent_scroll_mode["vertical"])
		self.setHorizontalScrollMode(self.parent_scroll_mode["horizontal"])
		# need to set self scroll mode because the scroll mode binding happens after init_geometry

	def hide_freezed_area(self):
		parent = self.parent
		for column_index in range(parent.model().columnCount()):
			if column_index not in range(self.start_column_index, self.end_column_index):
				self.setColumnHidden(column_index, True)
				if self.orentation == FreezeView.top:
					if not parent.isColumnHidden(column_index):
						parent.setColumnHidden(column_index, True)
						self.freeze_hiddin_column.append(column_index)
			else:
				self.setColumnWidth(column_index, parent.columnWidth(column_index))

		for row_index in range(parent.model().rowCount()):
			if row_index not in range(self.start_row_index, self.end_row_index):
				self.setRowHidden(row_index, True)	
				if self.orentation == FreezeView.left:
					if not parent.isRowHidden(row_index):
						parent.setRowHidden(row_index, True)
						self.freeze_hiddin_row.append(row_index)
			else:
				self.setRowHeight(row_index, parent.rowHeight(row_index))

	def show_freezed_area(self):
		parent = self.parent
		for row_index in self.freeze_hiddin_row:
			parent.setRowHidden(row_index, False)
		for column_index in self.freeze_hiddin_column:
			parent.setColumnHidden(column_index, False)		

	def set_size(self, x, y, w, h):
		self.move(x, y)
		self.setFixedWidth(w)
		self.setFixedHeight(h)
		self.updateGeometry()

	def increament_width(self, delta_width):
		if self.resizable:
			self.setFixedWidth(self.width() + delta_width)
			self.updateGeometry()
		
	def increament_height(self, delta_height):
		if self.resizable:
			self.setFixedHeight(self.height() + delta_height)
			self.updateGeometry()
		
	def remove_rows(self, row_index):
		# if row_index in range(self.start_row_index, self.end_row_index):
		# 	self.end_row_index -= 1
			self.initiallize_geometry()

	def remove_columns(self, column_index):
		# if column_index in range(self.start_column_index, self.end_column_index):
		# 	self.end_column_index -= 1
			self.initiallize_geometry()


	def insert_row_at(self, row_index, row_counts = 1):
		# if row_index in range(self.start_row_index, self.end_row_index):
		# 	self.end_row_index += row_counts
		# 	for row_index in range(self.end_row_index-1, self.end_row_index+row_counts-1):
		# 		self.setRowHidden(row_index, False)
			self.initiallize_geometry()

	def insert_column_at(self, column_index, column_counts = 1):
		# if column_index in range(self.start_column_index, self.end_column_index):
		# 	self.end_column_index += column_counts
		# 	for column_index in range(self.end_column_index-1, self.end_column_index+column_counts-1):
		# 		self.setColumnHidden(column_index, False)
			self.initiallize_geometry()

	def initiallize_mouse_anchor(self):
		pass
		# self.mouse_anchor.__dict__["anchor_x"] = None
		# self.mouse_anchor.__setattr__("anchor_x", None)
		# self.mouse_anchor.__setattr__("anchor_y", None)
		# self.mouse_anchor.__setattr__(       "x", None)
		# self.mouse_anchor.__setattr__(       "y", None)
		# self.mouse_anchor.__setattr__( "pivot_y", None)
		# self.mouse_anchor.__setattr__( "pivot_y", None)
		# self.mouse_anchor.__setattr__(  "rect_w", None)
		# self.mouse_anchor.__setattr__(  "rect_h", None)

	def mouseMoveEvent (self, event):
		QTableView.mouseMoveEvent (self, event)
		self.mouse_move_signal.emit(event)


	def mousePressEvent(self, event):
		QTableView.mousePressEvent (self, event)
		self.mouse_press_signal.emit(event)

	def mouseReleaseEvent (self, event):
		QTableView.mouseReleaseEvent (self, event)
		self.mouse_release_signal.emit(event)

