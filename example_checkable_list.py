import sys
from PySide6.QtCore import Qt, QAbstractListModel
from PySide6.QtWidgets import QApplication, QMainWindow, QListView, QVBoxLayout, QPushButton, QWidget

class CheckableListModel(QAbstractListModel):
    """Create a list model with checkable items"""
    def __init__(self, list_of_options=None, name=None):
        super().__init__()
        self.list_of_options = list_of_options or []
        self.name = name
        self.checked_states = [False] * len(self.list_of_options)
        
    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.list_of_options[index.row()]
        elif role == Qt.CheckStateRole:
            return Qt.Checked if self.checked_states[index.row()] else Qt.Unchecked
        
    def setData(self, index, value, role):
        if role == Qt.CheckStateRole:
            self.checked_states[index.row()] = (value == Qt.Checked)
            self.dataChanged.emit(index, index, [role])
            return True
        return False
        
    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
        
    def rowCount(self, index):
        return len(self.list_of_options)
    
    def updateList(self, new_list):
        self.beginResetModel()
        self.list_of_options = new_list
        self.checked_states = [False] * len(new_list)
        self.endResetModel()
        
    def getCheckedItems(self):
        """Return a list of checked items"""
        return [item for item, checked in zip(self.list_of_options, self.checked_states) if checked]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checkable List Example")
        self.resize(400, 300)
        
        # Create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Create list view with checkable items
        self.list_view = QListView()
        self.model = CheckableListModel(
            ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"],
            name="example_list"
        )
        self.list_view.setModel(self.model)
        
        # Enable clicking on the checkbox area
        self.list_view.clicked.connect(self.handle_item_clicked)
        
        # Create button to show checked items
        self.button = QPushButton("Show Checked Items")
        self.button.clicked.connect(self.show_checked_items)
        
        # Add widgets to layout
        layout.addWidget(self.list_view)
        layout.addWidget(self.button)
        
        # Set central widget
        self.setCentralWidget(central_widget)
    
    def handle_item_clicked(self, index):
        # Toggle the check state when an item is clicked
        current_state = self.model.data(index, Qt.CheckStateRole)
        new_state = Qt.Unchecked if current_state == Qt.Checked else Qt.Checked
        self.model.setData(index, new_state, Qt.CheckStateRole)
    
    def show_checked_items(self):
        checked_items = self.model.getCheckedItems()
        print("Checked items:", checked_items)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

