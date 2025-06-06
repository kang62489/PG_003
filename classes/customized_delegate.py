## Author: Kang
## Last Update: 2025-Jan-23
## Usage: To create an input delegate which can be used to modify values in the cells of QTableView

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStyledItemDelegate, QLineEdit

class CenterAlignDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter
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