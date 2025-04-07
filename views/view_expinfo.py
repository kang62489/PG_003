from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QAbstractItemView
from classes.customized_delegate import CellEditDelegate
from util.constants import (
    UISizes, 
    UIAlignments, 
    DEFAULTS
)

class ExpInfoView:
    """Handles UI configuration for Template Manager tab (tab_0)"""
    def __init__(self, ui, main_panel):
        self.ui = ui
        self.main = main_panel
        self.setup_ui()
        
    def setup_ui(self):
        self.setup_layouts()
        self.setup_buttons()
        self.setup_table()
        self.setup_combobox()
        
    def setup_layouts(self):
        # Set spaces
        self.ui.verticalLayout_7.setSpacing(DEFAULTS["LAYOUT_SPACING"])
        self.ui.verticalLayout_11.setSpacing(DEFAULTS["LAYOUT_SPACING"])
        self.ui.verticalLayout_7.insertSpacing(2, DEFAULTS["VERTICAL_SPACING_1"])
        self.ui.verticalLayout_11.insertSpacing(0, DEFAULTS["VERTICAL_SPACING_2"])
        
    def setup_buttons(self):
        buttons = [
            self.ui.btn_loadTemplate,
            self.ui.btn_saveTemplate,
            self.ui.btn_deleteCurrentTemplate,
            self.ui.btn_exportExpInfo,
            self.ui.btn_addNewRows,
            self.ui.btn_removeSelectedRows,
            self.ui.btn_moveUp,
            self.ui.btn_moveDown
        ]
        
        for btn in buttons:
            btn.setFixedSize(UISizes.BUTTON_LARGE)
            
        # Initial button states
        self.ui.btn_deleteCurrentTemplate.setEnabled(False)
        
    def setup_table(self):
        table = self.ui.tv_expInfo
        # Alignment
        table.verticalHeader().setDefaultAlignment(UIAlignments.RIGHT_CENTER)
        
        # Display settings
        table.horizontalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setDefaultSectionSize(50)
        table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        table.setItemDelegate(CellEditDelegate())
        
    def setup_combobox(self):
        self.ui.cb_expInfo.setFixedSize(UISizes.COMBO_STANDARD)
        self.ui.lbl_expInfo.setFixedSize(UISizes.LABEL_STANDARD)
        self.ui.lbl_expInfo.setAlignment(UIAlignments.CENTER)
        
