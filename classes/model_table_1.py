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
            self.autoCalc()
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
        if addData.shape[1] > self._data.shape[1]:
            self.addCols(SourceParent, self._data.shape[1]-1, (addData.shape[1] - self._data.shape[1]))
        
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
       
    def autoCalc(self):
        properties = self._data.index.tolist()
        iloc_0 = self._data.index.get_loc("Date of Recording")
        iloc_1 = self._data.index.get_loc("Date of Birth")
        iloc_2 = self._data.index.get_loc("Date of Injection")
        iloc_3 = self._data.index.get_loc("Ages(weeks)")
        iloc_4 = self._data.index.get_loc("Incubated(weeks)")
        iloc_5 = self._data.index.get_loc("Animal ID")
        iloc_6 = self._data.index.get_loc("Numbers of Animals")
        
        if "Date of Recording" in properties:
            if self._data.iloc[iloc_0, 0] != "":
                self.DOR = datetime.strptime(self._data.iloc[iloc_0][0], '%Y-%m-%d')
            else:
                self.DOR = datetime.today()
                self._data.iloc[iloc_0, 0] = self.DOR.strftime('%Y-%m-%d')
                
        if "Numbers of Animals" in properties:
            ani_id_list = [val for val in self._data.iloc[iloc_5] if val != ""]
            self._data.iloc[iloc_6, 0] = len(ani_id_list)
        
        if "Date of Birth" in properties:
            self.DOB = [val for val in self._data.iloc[iloc_1].values if val != ""]
            
        if "Date of Injection" in properties:
            self.DOI = [val for val in self._data.iloc[iloc_2].values if val != ""]
            
        if (hasattr(self, 'DOB') and self.DOB) and (hasattr(self, 'DOI') and self.DOI):
            self.AGE = []
            self.INCU = []
            

            # Calculation of ages of and incubated weeks of the animals
            for dob, doi in zip(self.DOB, self.DOI):
                dor = pendulum.instance(self.DOR.date())
                self.AGE.append((dor - pendulum.instance(datetime.strptime(dob, '%Y-%m-%d').date())).in_weeks())
                self.INCU.append((dor - pendulum.instance(datetime.strptime(doi, '%Y-%m-%d').date())).in_weeks())
            
            for idx, val in enumerate(self.AGE):
                self._data.iloc[iloc_3, idx] = val
            
            for idx, val in enumerate(self.INCU):
                self._data.iloc[iloc_4, idx] = val
            
            print("Data Updated!!")
            self.layoutChanged.emit()

