# Modules
from PySide6.QtWidgets import QHeaderView
from classes import customized_delegate
from util.constants import (
    UISizes,
    UIAlignments
)

class RecDBView:
    def __init__(self, ui):
        self.ui = ui
        self.setupUI()
        
    def setupUI(self):
        self.setup_buttons()
        self.setup_tableview()
        self.setup_groupbox()
    
    def setup_tableview(self):
        self.ui.tableView_recDB.horizontalHeader().setDefaultAlignment(UIAlignments.CENTER)
        self.ui.tableView_recDB.verticalHeader().setVisible(False)
        self.ui.tableView_recDB.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableView_recDB.setItemDelegate(customized_delegate.CenterAlignDelegate())
    
    def setup_buttons(self):
        buttons_small = [
            self.ui.btn_loadRecDB,
            self.ui.btn_deleteTable,
            self.ui.btn_exportSummary,
        ]
        
        for btn in buttons_small:
            btn.setFixedSize(UISizes.BUTTON_SMALL)
        
        self.ui.btn_importRecDB.setFixedHeight(UISizes.BUTTON_LONG_HEIGHT)
            
    def setup_groupbox(self):
        self.ui.groupBox_recDB_status.setFixedHeight(UISizes.GROUP_BOX_STATUS_HEIGHT)
        