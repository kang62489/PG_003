## Modules
# Standard library imports
from datetime import datetime

# Third-party imports
from PySide6.QtWidgets import QAbstractItemView, QHeaderView

# Local application imports
from classes import DelegateCenterAlign
from util.constants import MenuOptions, UIAlignments, UISizes


class ViewAbfNote:
    def __init__(self, main_ui):
        self.ui = main_ui
        self.setup_ui()

    def setup_ui(self):
        self.setup_spinbox()
        self.setup_combobox()
        self.setup_dateedit()
        self.setup_tableview()
        self.setup_pushbutton()

    def setup_spinbox(self):
        self.ui.sb_abfSlice.setValue(self.ui.sb_slice.value())
        self.ui.sb_abfSlice.setRange(1, 10)

        self.ui.sb_abfAt.setValue(self.ui.sb_at.value())
        self.ui.sb_abfAt.setRange(1, 10)

    def setup_combobox(self):
        self.ui.cb_abfSide.addItems(MenuOptions.SIDE)
        self.ui.cb_abfAtType.addItems(MenuOptions.LOC_TYPES)
        self.ui.cb_currentAbf.setEnabled(True)

    def setup_dateedit(self):
        self.ui.de_abfDate.setDate(datetime.today())
        self.ui.de_abfDate.setCalendarPopup(True)

    def setup_tableview(self):
        self.ui.tv_abfNote.horizontalHeader().setDefaultAlignment(UIAlignments.CENTER)
        self.ui.tv_abfNote.verticalHeader().setVisible(False)
        self.ui.tv_abfNote.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tv_abfNote.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tv_abfNote.setItemDelegate(DelegateCenterAlign())

    def setup_pushbutton(self):
        self.ui.btn_clearCellParams.setFixedSize(UISizes.BUTTON_GENERAL_WIDTH, UISizes.BUTTON_GENERAL_HEIGHT)
        self.ui.btn_logProtocol.setFixedSize(UISizes.BUTTON_GENERAL_WIDTH, UISizes.BUTTON_GENERAL_HEIGHT)
        self.ui.btn_logCellParams.setFixedSize(UISizes.BUTTON_GENERAL_WIDTH, UISizes.BUTTON_GENERAL_HEIGHT)
        self.ui.btn_deleteSelected.setFixedHeight(UISizes.BUTTON_GENERAL_HEIGHT)
        self.ui.btn_toggleCellParams.setFixedHeight(UISizes.BUTTON_GENERAL_HEIGHT)
        self.ui.btn_toggleCellParams.setCheckable(True)
        self.ui.btn_exportXlsx.setFixedHeight(UISizes.BUTTON_GENERAL_HEIGHT)
