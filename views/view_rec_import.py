# Third-party imports
from PySide6.QtWidgets import QAbstractItemView, QHeaderView

# Local application imports
from classes import DelegateCenterAlign
from util.constants import UIAlignments, UISizes


class ViewRecImport:
    def __init__(self, ui):
        self.ui = ui
        self.setup_uis()

    def setup_uis(self):
        self.setup_buttons()
        self.setup_tableview()
        self.setup_groupbox()

    def setup_tableview(self):
        self.ui.tv_recDb.horizontalHeader().setDefaultAlignment(UIAlignments.CENTER)
        self.ui.tv_recDb.verticalHeader().setVisible(False)
        self.ui.tv_recDb.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tv_recDb.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tv_recDb.setItemDelegate(DelegateCenterAlign())

    def setup_buttons(self):
        buttons_small = [
            self.ui.btn_loadRecTable,
            self.ui.btn_deleteTable,
            self.ui.btn_exportSummary,
        ]

        for btn in buttons_small:
            btn.setFixedSize(UISizes.BUTTON_SMALL)

        self.ui.btn_importRecDb.setFixedHeight(UISizes.BUTTON_LONG_HEIGHT)

    def setup_groupbox(self):
        self.ui.gb_recDB_status.setFixedHeight(UISizes.GROUP_BOX_STATUS_HEIGHT)
