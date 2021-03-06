import time

import os
import csv
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *
from uiplus          import *
import statistics
import pandas 
import numpy


class DataItemModel(QStandardItemModel):
    data_changed = pyqtSignal()
    def __init__(self, parent = None, *args):
        QStandardItemModel.__init__(self, parent, *args)
        self._data_frame   = None
        self._header_frame = None
        self.header        = False

    def setDataFrame(self, data, copy_data = False,  header = False):
        self.header        = True if header == True else False
        data_frame         = data if isinstance(data, pandas.core.frame.DataFrame) else pandas.DataFrame(data)
        self._header_frame = data_frame.iloc[0]     if self.header else None
        data_frame         = data_frame[1:]    if self.header else data_frame
        self._data_frame   = data_frame.copy() if copy_data   else data_frame
        #print(self._header_frame)

        self.clear()
        for row_index in range(len(self._data_frame)):
            self.appendRow([DataItem(data) for data in self._data_frame.iloc[row_index]])

        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return  len(self._data_frame)

    def columnCount(self, parent=None):
        return len(self._data_frame.columns)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        elif (role != Qt.DisplayRole) and (role != Qt.EditRole):
            return None
        else: 
            return self._data_frame.iloc[index.row(), index.column()]

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return None            

        if index.isValid() and index.row() < self.rowCount() and index.column() < self.columnCount():
            self._data_frame.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        return None

    def rowData(self, row, role =Qt.EditRole):
        row_data = []
        if not row < self.rowCount():
            return None
        for col in range(self.columnCount):
            row_data.append(self.data(self.index(row, col)))
        return row_data

    def columnData(self, col, role =Qt.EditRole):
        if not col < self.columnCount():
            return None
        return (self._data_frame.iloc[:,col].copy()).values.tolist()


    def headerData(self, section, orientation, role):
        
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if self.header:
                return (self._header_frame.iloc[section])
            return ('%d' % (section + 1)).zfill(len(str(len(self._data_frame.iloc[0]))))

        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return ('%d' % (section + 1)).zfill(len(str(len(self._data_frame))))
        

class DataItem(QStandardItem):
    def __init__(self, data = None):
        QStandardItem.__init__(self)
        # self.setCheckable(True)
        # self.setCheckState(Qt.Checked)



class TableView(QTableView):
    def __init__(self, model, parent = None, *args):
        QTableView.__init__(self, parent, *args)
        self.filter_proxy_model = SortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(model)
        self.setSortingEnabled(True)
        self.setModel(self.filter_proxy_model)
        header = self.horizontalHeader()
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        header.customContextMenuRequested.connect( self.showHeaderMenu )

        self.setMouseTracking(True)

    def showHeaderMenu(self, point):
        column    = self.horizontalHeader().logicalIndexAt(point.x())
        self.menu = HorizontalHeaderMenu(self, column = column)
        self.menu.pop(QCursor().pos())


        

class HorizontalHeaderMenu(QWidget):
    def __init__(self, parent, column):
        super().__init__()
        self.parent = parent
        self.column = column
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.SubWindow )
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.initUI()

    def initUI(self):

        self.sort_des_order  = QPushButton("Sort Z to A")
        self.sort_asc_order  = QPushButton("Sort A to Z")
        self.sort_cust_order = QPushButton("Custom Sort")
        self.filter_edit     = QLineEdit()
        self.clear_filter    = QPushButton("Clear filter")
        self.filter_tree     = TableFilterTree(self.parent.model(), self.column)
        self.setLayout(VBox(self.sort_asc_order, self.sort_des_order, self.sort_cust_order, self.filter_edit,  self.clear_filter, self.filter_tree))
        
    def pop(self, point):
        x, y           = point.x(), point.y()
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(50)
        self.animation.setStartValue(self.geometry() if self.isVisible() else QRect(x, y, 0, 0))
        self.animation.setEndValue(QRect(x, y, 250, 400))


        # t_item = QTreeWidgetItem()
        # t_item.setText(0, 'Select All')
        # t_item.setCheckState (0, Qt.CheckState.Checked)
        # self.filter_tree.addTopLevelItem(t_item)
        # for item in ( sorted(set(self.parent.model().sourceModel().columnData(column)))):
        #     c_item = QTreeWidgetItem()
        #     c_item.setText(0, item)
        #     c_item.setCheckState (0,Qt.CheckState.Checked)
        #     t_item.addChild(c_item)

        # t_item.setExpanded(True)
        QWidget.show(self)
        self.animation.start()

        if self.column in self.parent.filter_proxy_model.filters:
            filter_regex = self.parent.filter_proxy_model.filters[self.column]['regex']
            if filter_regex:
                filter_pattern = filter_regex.pattern()
                self.filter_edit.setText(filter_pattern)
            

        self.filter_edit.textChanged.connect(lambda text = self.filter_edit.text(), col = self.column: 
            self.parent.filter_proxy_model.setRegexFilterByColumn(QRegExp(text, Qt.CaseSensitive, QRegExp.FixedString),col))

        self.filter_edit.textChanged.connect(self.filter_tree.udpateModel)
        self.sort_des_order.clicked.connect(lambda : self.parent.sortByColumn(self.column, Qt.DescendingOrder))
        self.sort_asc_order.clicked.connect(lambda : self.parent.sortByColumn(self.column, Qt.AscendingOrder))
        self.filter_tree.checkStateChanged.connect(lambda item : self.parent.model().setExclusionFilterByColumn(item.data(0), self.column))

    def eventFilter(self, object, event):
        if event.type() == QEvent.WindowDeactivate:
            self.hide()
            self.close()

        return False


class TableFilterTree(QTreeView):
    checkStateChanged = pyqtSignal(QStandardItem)
    def __init__(self, model, column, parent = None):
        super().__init__()
        self.setHeaderHidden(True)
        self.hideColumn(0)
        self.column       = column
        self.source_model = model
        self.udpateModel()
        self.header().resizeSection(0, 300)

        
    #multiple exclusion is still not function properly -------------------------------------------V
    def udpateModel(self):
        active_data   = self.source_model.columnData(self.column)
        excluded_data = self.source_model.columnExcludedData(self.column)
        full_data     = sorted(set([*active_data, *excluded_data]))
        model         = TreeModel(full_data)
        toplevel_item = model.index(0,0, QModelIndex())
        
        self.clicked.connect(lambda index : self.k(index))
        for data in excluded_data:
            i = full_data.index(data)
            model.flipCheckState(model.index(i, 0, toplevel_item))


        model.checkStateChanged.connect(lambda item : self.checkStateChanged.emit(item))
        self.setModel(model)
        self.expand(toplevel_item)

    def k(self, index):
        self.model().flipCheckState(index)
        self.update(index)
        self.update(index.parent())
        for row in range(self.model().rowCount(index)):
            self.update(index.child(row, 0)) 
            
        
        # unable to update childs and parent
class TreeModel(QAbstractItemModel):
    checkStateChanged = pyqtSignal(QStandardItem)
    def __init__(self, data, parent=None):
        super(TreeModel, self).__init__(parent)

        self.rootItem = TreeItem(['Root'])
        self.topItem  = TreeItem(["All"], self.rootItem)
        self.rootItem.appendChild(self.topItem)   
        self.setupModelData(self.topItem, data)


    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        
        item = index.internalPointer()
        if role != Qt.DisplayRole:    

            if (role == Qt.CheckStateRole) and (index.column() == 0):
                return item.checkState()
            return None

        return item.data(index.column())

    def flipCheckState(self, index):

        # print (index.row(), index.column(), index.parent(), index.internalPointer(), index.internalId())
        if not index.isValid():
            return None

        item = index.internalPointer()
        self.setCheckState(index, Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked)
        self.checkStateChanged.emit(item)

    def setCheckState(self, index, state):
        if not index.isValid():
            return None

        # checked : 2, partiallychecked : 1, unchecked : 0
        # define check state propagation between parent and child 
        # emit update signal to view

        item        = index.internalPointer()
        item_parent = item.parent()
        item_childs = [ item.child(row) for row in range(item.childCount()) ]

        item.setCheckState(state)

        if item_childs and state in [Qt.Checked, Qt.Unchecked]:
            _ = [ child.setCheckState(state) for child in item_childs]

        if item_parent:
            states = statistics.mean( [ item_parent.child(row).checkState() for row in range(item_parent.childCount()) ] )
            item_parent.setCheckState( states if states in [Qt.Checked, Qt.Unchecked] else Qt.PartiallyChecked)
    
    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags 
        return index.internalPointer().flags()

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)
        return None

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)


    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()

    def setupModelData(self, parent, data): 
        for item in data:
            dataitem = TreeItem([item], parent)
            parent.appendChild(dataitem)



class TreeItem(QStandardItem):
    def __init__(self, data, parent=None):
        super(TreeItem, self).__init__(parent)
        self.parentItem = parent
        self.itemData   = data
        self.childItems = []
        self.setCheckable(True)
        self.state      = Qt.Checked
 
    def checkState(self):
        return self.state

    def setCheckState(self, state):
        self.state = state
 
    def flags(self):
        return ( Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable ) & ~Qt.ItemIsEditable

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0


class SortFilterProxyModel(QSortFilterProxyModel):
    column_filtered = pyqtSignal(int)
    def __init__(self, *args, **kwargs):
        QSortFilterProxyModel.__init__(self, *args, **kwargs)
        self.filters = {}

    def setSourceModel(self, model):
        self.filter_result = [False for i in range(model.rowCount())]
        QSortFilterProxyModel.setSourceModel(self, model)


    def initFilterColumn(self, column):
        self.filters[column] = { 'regex' : None, 'excluded' : [], 'data' : []}

    def setRegexFilterByColumn(self, regex, column):
        if not (column in self.filters):
            self.initFilterColumn(column)
        self.filters[column]['regex'] = regex
        self.invalidateFilter()

    def setExclusionFilterByColumn(self, data, column):
        if not (column in self.filters):
            self.initFilterColumn(column)

        if data in self.filters[column]['excluded']:
            self.filters[column]['excluded'].remove(data)
        else:
            self.filters[column]['excluded'].append(data)
        
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):

        for key, filter_item in self.filters.items():
            regex    = filter_item['regex']
            excluded = filter_item['excluded']
            ix       = self.sourceModel().index(source_row, key, source_parent)

            if ix.isValid():
                text = self.sourceModel().data(ix)
                if regex:
                    if not regex.indexIn(text) != -1:
                        return False
                if excluded:
                    if text in excluded:
                        return False

                filter_item['data'].append(text)

            self.column_filtered.emit(key)

     
        return True

    def columnData(self, col, role =Qt.EditRole):
        if not col < self.columnCount():
            return None
        return [ self.data(self.index(row,col)) for row in range(self.rowCount())]

    def columnExcludedData(self, col, role =Qt.EditRole):
        if not col < self.columnCount():
            return None
        try:
            return self.filters[col]['excluded']
        except KeyError:
            return []

if __name__ == '__main__':
    app = QApplication([])
    window = QWidget()
    k = []
    with open('./mockup.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            k.append(row)
        
    model = DataItemModel()
    model.setDataFrame(k, header= True)


    layout = QVBoxLayout(window)
    line_edit = QLineEdit()
    # line_edit.textChanged.connect(filter_proxy_model.setFilterRegExp)
    layout.addWidget(line_edit)

    table = TableView(model)
    layout.addWidget(table)
    window.resize(1000, 800)
    window.show()
    app.exec_()


