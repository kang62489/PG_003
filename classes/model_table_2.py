## Author: Kang
## Last Update: 2025-Jan-22
## Usage: A class for build a customized model for QTableView

import pendulum
from PySide6.QtCore import Qt, QAbstractTableModel
from datetime import datetime
import pandas as pd
import warnings

# Suppress FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

class TableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data if data is not None else pd.DataFrame()

        
    def data(self, index, role):
        columns = list(self._data.columns)
        if role == Qt.DisplayRole:
            # Get the raw value
            value = self._data.iloc[index.row(), index.column()]
            # Perform per-type checks and render accordingly.
            if isinstance(value, datetime):
                # Render time to YYY-MM-DD.
                return value.strftime("%Y-%m-%d")
            if isinstance(value, float):
                # Render float to 2 dp
                return "%.2f" % value
            if isinstance(value, str):
            # Render strings with quotes
                return '%s' % value
            return "%s" % value

    def rowCount(self, index):
        return self._data.shape[0]
    
    def columnCount(self, index):
        return self._data.shape[1]
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
    
    # To make cells editable by define "flags" and "setData"
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return super().flags(index) | Qt.ItemIsEditable

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
            return True
        return False        
    
    # To make the model can be update
    def update(self, new_table):
        self.beginResetModel()
        self._data = new_table
        self.endResetModel()
        
    def moveRows(self, sourceRow, destinationRow, count=1):
        if destinationRow > sourceRow:
            destinationRow -= 1
                
        rows = self._data.iloc[sourceRow:sourceRow + count].copy()
        rowNames = self._data.index.tolist()
        
        self._data = pd.concat([self._data.iloc[:sourceRow], self._data.iloc[sourceRow + count:]]).reset_index(drop=True)
        self._data = pd.concat([self._data.iloc[:destinationRow], rows, self._data.iloc[destinationRow:]]).reset_index(drop=True)
        
        current = rowNames[sourceRow]
        destination = rowNames[destinationRow]
        rowNames[sourceRow], rowNames[destinationRow] = destination, current
        
        self._data.index = rowNames
        
        self.layoutChanged.emit()
        
    def addRows(self, SourceParent, rowNumber, addData):
        count = addData.shape[0]
        
        self.beginInsertRows(SourceParent, rowNumber, rowNumber + count - 1)
        rowNames = self._data.index.tolist()
        self._data = pd.concat([self._data.iloc[:rowNumber+1], addData, self._data.iloc[rowNumber+1:]]).reset_index(drop=True)
        self._data.index = rowNames[:rowNumber+1] + addData.index.tolist() + rowNames[rowNumber+1:]
        self.endInsertRows()
        self.selfClean()
        self.layoutChanged.emit()
        
    def rmRows(self, SourceParent, rowNumber, count):
        self.beginRemoveRows(SourceParent, rowNumber, rowNumber + count - 1)
        self._data = self._data.drop(self._data.index[rowNumber:rowNumber + count])
        self.endRemoveRows()
        
        for col in self._data.columns:
            if self._data[col].unique().shape[0] == 1 and self._data[col].unique()[0] == "":
                self._data.drop(columns=col, inplace=True)
        
        self.layoutChanged.emit()
    
    def addCols(self, SourceParent, colNumber, count):
        columnWidth = len(self._data.columns.tolist())
        rowNames = self._data.index.tolist()
        emptyValueList = [["" for i in range(self._data.shape[0])] for j in range(count)]
        emptyCols = pd.DataFrame(columns=[f"Value_{columnWidth+i}" for i in range(count)])
        for idx, col in enumerate(emptyCols.columns):
            emptyCols[col] = emptyValueList[idx]
        
        emptyCols.index = rowNames
        
        self.beginInsertColumns(SourceParent, colNumber, colNumber + count - 1)
        self._data = pd.concat([self._data, emptyCols],axis = 1)
        self.endInsertColumns()
        self._data.columns = [f"Value_{i}" for i in range(self._data.shape[1])]
        self._data.index = rowNames
        self.layoutChanged.emit()
        
    def selfClean(self):
       self._data.fillna('', inplace=True)
