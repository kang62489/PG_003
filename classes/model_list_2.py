## Modules
from PySide6.QtCore import Qt, QAbstractListModel, Signal

class ListModel(QAbstractListModel):
    """Create a checkable list model for QListView file browser"""
    
    # Add a custom signal to check if all items are selected in setData
    allSelectedCheck = Signal(bool)
    
    def __init__(self, list_of_files=None, name=None):
        super().__init__()
        self.list_of_files = list_of_files or []
        self.name = name
        self.checked_states = [True] * len(self.list_of_files)
        
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.list_of_files[index.row()]
        elif role == Qt.CheckStateRole:
            return Qt.Checked if self.checked_states[index.row()] else Qt.Unchecked
        
    def rowCount(self, index):
        return len(self.list_of_files)
    
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
    
    def setData(self, index, value, role):
        """Set the checked state of a checkbox"""
        value_to_qt = {0: False, 2: True}
        if role == Qt.CheckStateRole:
            self.checked_states[index.row()] = value_to_qt[value]
            self.dataChanged.emit(index, index, [role])
        
            self.allSelectedCheck.emit(all(self.checked_states))
            return True
        return False
    
    def loadFileList(self, file_list, all_is_checked=True):
        self.beginResetModel()
        self.list_of_files = file_list
        if all_is_checked:
            self.checked_states = [True] * len(file_list)
        else:
            self.checked_states = [False] * len(file_list)
        self.endResetModel()
        
    def getCheckedItems(self):
        """Return a list of checked items"""
        return [item for item, checked in zip(self.list_of_files, self.checked_states) if checked]
    
    def setAllChecked(self, checked):
        self.beginResetModel()
        self.checked_states = [checked] * len(self.list_of_files)
        self.endResetModel()