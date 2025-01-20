## Author: Kang
## Last Update: 2024-Jan-17
## Usage: To create an input delegate which can be used to modify values in the cells of QTableView

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit

class CellEditDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole)
        editor.setText(value)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.EditRole)
    
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignHCenter | Qt.AlignVCenter
        option.font.setFamily("Arial")