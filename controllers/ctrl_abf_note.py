## Modules
# Third-party imports
from PySide6.QtWidgets import QLineEdit


class CtrlAbfNote:
    def __init__(self, main_ui):
        self.ui = main_ui
        self.connect_signals()

    def connect_signals(self):
        self.ui.btn_clearCellParams.clicked.connect(self.clear_cell_parameters)

    def clear_cell_parameters(self):
        line_edits_to_clear = self.ui.gb_cellParams.findChildren(QLineEdit)
        for line_edit in line_edits_to_clear:
            line_edit.clear()
