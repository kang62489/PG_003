## Third-party imports
from PySide6.QtCore import QAbstractListModel, Qt


class ListModel(QAbstractListModel):
    """Create a list model for combobox menu which can be updated automatically"""

    def __init__(self, list_of_options=None, name=None):
        super().__init__()
        self.list_of_options = list_of_options or []
        self.name = name

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.list_of_options[index.row()]

    def rowCount(self, index):
        return len(self.list_of_options)

    def updateList(self, new_list):
        self.beginResetModel()
        self.list_of_options = sorted(new_list)
        self.endResetModel()
