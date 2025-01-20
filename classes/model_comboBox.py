## Author: Kang
## Last Update: 2024-Jan-15
## Usage: A class for build a customized model for QComboBox

from PySide6.QtCore import Qt, QAbstractListModel

class SelectorModel(QAbstractListModel):
    def __init__(self, selections=None):
        super().__init__()
        self.selections = selections or []
        
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.selections[index.row()]
        
    def rowCount(self, index):
        return len(self.selections)
    
    def updateList(self, new_list):
        self.beginResetModel()
        self.selections = new_list
        self.endResetModel()