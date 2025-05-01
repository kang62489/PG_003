from PySide6.QtCore import Qt, QAbstractListModel

class ListModel(QAbstractListModel):
    """Create a list model for combobox menu which can be updated automatically"""
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