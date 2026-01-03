# Modules
from PySide6.QtCore import Qt, QAbstractTableModel
from datetime import datetime
import pandas as pd
import warnings

from tabulate import tabulate

# Suppress FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

class ModelMetadataForm(QAbstractTableModel):
    """Create a table model for add customized properties"""
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
        
    def mv_rows(self, rows, step):
        """Move multiple rows up or down by the specified step
        
        Args:
            rows: List of row indices to move
            step: Number of positions to move (-1 for up, 1 for down)
        """
        # Create a copy of selected rows with their original indices
        selected_df = self._data.iloc[rows].copy()
        selected_indices = selected_df.index.tolist()
        
        # Remove selected rows from the dataframe
        self._data = self._data.drop(self._data.index[rows])
        remaining_indices = self._data.index.tolist()
        
        # Calculate target position
        if step == -1:  # Moving up
            target_row = max(0, rows[0] + step)
        elif step == 1:  # Moving down
            target_row = min(rows[0] + step, len(self._data))
        else:
            raise ValueError("Invalid step value. Step must be -1 (up) or 1 (down)")
        
        # Insert rows at target position and reconstruct the index
        if target_row == 0:
            # Insert at the beginning
            self._data = pd.concat([selected_df, self._data])
            new_indices = selected_indices + remaining_indices
        elif target_row >= len(self._data):
            # Insert at the end
            self._data = pd.concat([self._data, selected_df])
            new_indices = remaining_indices + selected_indices
        else:
            # Insert in the middle
            self._data = pd.concat([
                self._data.iloc[:target_row], 
                selected_df, 
                self._data.iloc[target_row:]
            ])
            new_indices = (remaining_indices[:target_row] + 
                           selected_indices + 
                           remaining_indices[target_row:])
        
        # Set the preserved indices
        self._data.index = new_indices
        
        # Notify views of the change
        self.layoutChanged.emit()
        
        # Return the new positions of the moved rows
        return list(range(target_row, target_row + len(selected_df)))
        
    def add_rows(self, SourceParent, start_from_this_row, dataFrameToBeAdded):
        print("Data to be added:")
        print(tabulate(dataFrameToBeAdded, headers="keys", tablefmt="simple"))
        
        count = dataFrameToBeAdded.shape[0]
        # Check if we need to add columns for inserting new rows
        if dataFrameToBeAdded.shape[1] > self._data.shape[1]:
            self.add_cols(SourceParent, self._data.shape[1]-1, (dataFrameToBeAdded.shape[1] - self._data.shape[1]))
        
        self.beginInsertRows(SourceParent, start_from_this_row, start_from_this_row + count - 1)
        rowNames = self._data.index.tolist()
        self._data = pd.concat([self._data.iloc[:start_from_this_row+1], dataFrameToBeAdded, self._data.iloc[start_from_this_row+1:]]).reset_index(drop=True)
        self._data.index = rowNames[:start_from_this_row+1] + dataFrameToBeAdded.index.tolist() + rowNames[start_from_this_row+1:]
        
        print("Data added:")
        print(tabulate(self._data, headers="keys", tablefmt="simple"))
        
        self.endInsertRows()
        self.fill_na()
        self.layoutChanged.emit()
        
    def rm_rows(self, SourceParent, start_from_this_row, count):
        self.beginRemoveRows(SourceParent, start_from_this_row, start_from_this_row + count - 1)
        self._data = self._data.drop(self._data.index[start_from_this_row:start_from_this_row + count])
        self.endRemoveRows()
        
        columns = self._data.columns.to_list()
        if len(columns) > 1:
            for col in columns[1:]:
                if self._data[col].unique().shape[0] == 1 and self._data[col].unique()[0] == "":
                    self._data.drop(columns=col, inplace=True)
        
        self.layoutChanged.emit()
        
    def add_cols(self, SourceParent, colNumber, count):
        columnWidth = len(self._data.columns.tolist())
        rowNames = self._data.index.tolist()
        emptyValueList = [["" for i in range(self._data.shape[0])] for j in range(count)]
        emptyCols = pd.DataFrame(columns=[f"VALUE_{columnWidth+i}" for i in range(count)])
        for idx, col in enumerate(emptyCols.columns):
            emptyCols[col] = emptyValueList[idx]
        
        emptyCols.index = rowNames
        
        self.beginInsertColumns(SourceParent, colNumber, colNumber + count - 1)
        self._data = pd.concat([self._data, emptyCols],axis = 1)
        self.endInsertColumns()
        self._data.columns = [f"VALUE_{i}" for i in range(self._data.shape[1])]
        self._data.index = rowNames
        self.layoutChanged.emit()
        
    def fill_na(self):
       self._data.fillna('', inplace=True)
       

