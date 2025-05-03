# Modules
import pendulum
from PySide6.QtCore import Qt, QAbstractTableModel
from datetime import datetime
import pandas as pd
import warnings

from tabulate import tabulate

# Suppress FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

class TableModel(QAbstractTableModel):
    """Create a table model for add customized properties"""
    
    def __init__(self, data=None, auto_calc=True):
        super().__init__()
        self._data = data if data is not None else pd.DataFrame()
        self._auto_calc = auto_calc
        
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
            if self._auto_calc:
                self.autoCalc()
            self.dataChanged.emit(index, index, [Qt.DisplayRole, Qt.EditRole])
            return True
        return False        
    
    # To make the model can be update
    def update(self, new_table):
        self.beginResetModel()
        self._data = new_table
        self.endResetModel()
        
    def moveRows(self, rows, step):
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
        
    def addRows(self, SourceParent, start_from_this_row, dataFrameToBeAdded):
        print("Data to be added:")
        print(tabulate(dataFrameToBeAdded, headers="keys", tablefmt="simple"))
        
        count = dataFrameToBeAdded.shape[0]
        # Check if we need to add columns for inserting new rows
        if dataFrameToBeAdded.shape[1] > self._data.shape[1]:
            self.addCols(SourceParent, self._data.shape[1]-1, (dataFrameToBeAdded.shape[1] - self._data.shape[1]))
        
        self.beginInsertRows(SourceParent, start_from_this_row, start_from_this_row + count - 1)
        rowNames = self._data.index.tolist()
        self._data = pd.concat([self._data.iloc[:start_from_this_row+1], dataFrameToBeAdded, self._data.iloc[start_from_this_row+1:]]).reset_index(drop=True)
        self._data.index = rowNames[:start_from_this_row+1] + dataFrameToBeAdded.index.tolist() + rowNames[start_from_this_row+1:]
        
        print("Data added:")
        print(tabulate(self._data, headers="keys", tablefmt="simple"))
        
        self.endInsertRows()
        self.selfClean()
        self.layoutChanged.emit()
        
    def rmRows(self, SourceParent, start_from_this_row, count):
        self.beginRemoveRows(SourceParent, start_from_this_row, start_from_this_row + count - 1)
        self._data = self._data.drop(self._data.index[start_from_this_row:start_from_this_row + count])
        self.endRemoveRows()
        
        columns = self._data.columns.to_list()
        if len(columns) > 1:
            for col in columns[1:]:
                if self._data[col].unique().shape[0] == 1 and self._data[col].unique()[0] == "":
                    self._data.drop(columns=col, inplace=True)
        
        self.layoutChanged.emit()
        
    def addCols(self, SourceParent, colNumber, count):
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
        
    def selfClean(self):
       self._data.fillna('', inplace=True)
       
    def set_auto_calc(self, enabled):
        """Enable or disable automatic calculations"""
        self._auto_calc = enabled
    
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

