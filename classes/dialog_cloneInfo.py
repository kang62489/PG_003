## Modules
# Standard library imports
import json

# Third-party imports
import pandas as pd
from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QTableView,
    QVBoxLayout,
)

# Local application imports
from classes import customized_delegate, model_table_1
from util.constants import MODELS_DIR, UIAlignments


class CloneInfo(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clone Information")

        _clones_red = self._load_clone_JSON_file("menuList_clones_red.json")
        _clones_green = self._load_clone_JSON_file("menuList_clones_green.json")

        _clones_all = _clones_red | _clones_green
        clones_all_table = pd.DataFrame(list(_clones_all.items()), columns=["Clone Code", "Construct"])

        self.tableView_cloneInfo = QTableView()
        self.tableView_cloneInfo.verticalHeader().setVisible(False)
        self.tableView_cloneInfo.verticalHeader().setDefaultSectionSize(30)
        self.tableView_cloneInfo.horizontalHeader().setDefaultAlignment(UIAlignments.CENTER)
        self.tableView_cloneInfo.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView_cloneInfo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_cloneInfo.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableView_cloneInfo.setItemDelegateForColumn(0, customized_delegate.RCAlignDelegate())
        self.tableView_cloneInfo.setStyleSheet("""
            QTableView {
                font-size: 14px;
                font-family: Calibri;
                gridline-color: #D0D0D0;
            }
            QHeaderView::section {
                background-color: #4A90E2;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border: 1px solid #3A7BC8;
            }
        """)

        self.model_tableView_cloneInfo = model_table_1.TableModel(clones_all_table)
        self.tableView_cloneInfo.setModel(self.model_tableView_cloneInfo)

        self.buttons = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(self.buttons)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableView_cloneInfo)
        self.layout.addWidget(self.buttonBox, 0, UIAlignments.CENTER)
        self.setLayout(self.layout)
        self.resize_to_content()

    def resize_to_content(self):
        """Resize dialog to fit table columns completely"""
        # Calculate total width needed
        total_width = 0
        for col in range(self.model_tableView_cloneInfo.columnCount(QModelIndex())):
            total_width += self.tableView_cloneInfo.columnWidth(col)

        # Add padding for margins and frame
        padding = 30

        # Calculate height (limit to reasonable size)
        header_height = self.tableView_cloneInfo.horizontalHeader().height()
        max_rows = min(20, self.model_tableView_cloneInfo.rowCount(QModelIndex()))
        row_height = max_rows * self.tableView_cloneInfo.verticalHeader().defaultSectionSize()
        button_height = 50
        total_height = header_height + row_height + button_height + 40

        # Set dialog size
        self.resize(total_width + padding, min(total_height, 700))

        # Make width fixed (not resizable horizontally)
        self.setFixedWidth(total_width + padding)

    def _load_clone_JSON_file(self, filename):
        with open(MODELS_DIR / filename, "r") as f:
            loaded = json.load(f)
            sorted_clones = dict(sorted(loaded.items()))
            return sorted_clones

    def accept(self):
        # Close the dialog
        super().accept()
