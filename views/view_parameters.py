# Modules
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from classes.customized_delegate import CellEditDelegate, CenterAlignDelegate
from datetime import datetime
from util.constants import (
    UISizes, 
    UIAlignments, 
    DISPLAY_DATE_FORMAT,
    SERIAL_NAME_REGEX,
    DEFAULTS
)

class ParametersView:
    """Handles UI configuration for Tag Manager tab (tab_1)"""
    def __init__(self, ui, main_panel):
        self.ui = ui
        self.main = main_panel
        self.setup_ui()
        
    def setup_ui(self):
        self.setup_buttons()
        self.setup_labels()
        self.setup_combobox()
        self.setup_groupbox()
        self.setup_lineedit()
        
    def setup_buttons(self):
        # Main action buttons
        large_buttons = [
            self.ui.btn_up,
            self.ui.btn_down,
            self.ui.btn_insert,
            self.ui.btn_rm,
            self.ui.btn_convert
        ]
        for btn in large_buttons:
            btn.setFixedSize(UISizes.BUTTON_MEDIUM)
            
        # Tag set management buttons
        medium_buttons = [
            self.ui.btn_loadTagSet,
            self.ui.btn_newTagSet,
            self.ui.btn_discard,
            self.ui.btn_saveTagSet,
            self.ui.btn_deleteTagSet
        ]
        for btn in medium_buttons:
            btn.setFixedSize(UISizes.BUTTON_SMALL)
            
        # Serial number buttons
        small_buttons = [
            self.ui.btn_plus,
            self.ui.btn_minus,
            self.ui.btn_resetSerial,
            self.ui.btn_copySerial
        ]
        for btn in small_buttons:
            btn.setFixedSize(UISizes.BUTTON_TINY)
            
        # Tag buttons
        self.ui.btn_copyTag.setFixedSize(UISizes.BUTTON_WIDE)
        self.ui.btn_clearTag.setFixedSize(UISizes.BUTTON_WIDE)
        
        # Initial button states
        self.ui.btn_deleteTagSet.setEnabled(False)
        self.ui.btn_discard.setVisible(False)
        
    def setup_labels(self):
        self.ui.lbl_DOR.setFixedSize(UISizes.LABEL_WIDE)
        self.ui.lbl_date.setFixedSize(UISizes.LABEL_WIDE)
        self.ui.lbl_date.setAlignment(UIAlignments.CENTER)
        self.ui.lbl_date.setText(datetime.today().strftime(DISPLAY_DATE_FORMAT))
        
    def setup_combobox(self):
        self.ui.cb_recTagSet.setFixedSize(UISizes.COMBO_WIDE)
        self.ui.cb_recTagSet.setItemDelegate(CenterAlignDelegate())
        
    def setup_groupbox(self):
        self.ui.gb_tagSwitch.setTitle("Button Switches")
        self.ui.gb_tagSwitch.setFixedWidth(UISizes.GROUP_BOX_WIDTH)
        
    def setup_lineedit(self):
        self.ui.le_serialName.setFixedHeight(UISizes.LINE_EDIT_HEIGHT)
        self.ui.le_serialName.setAlignment(UIAlignments.CENTER)
        
        regex = QRegularExpression(SERIAL_NAME_REGEX)
        self.validator = QRegularExpressionValidator(regex)
        self.ui.le_serialName.setValidator(self.validator)
        self.ui.le_serialName.setPlaceholderText("YYYYMMDD-0000")
        self.ui.le_serialName.textChanged.connect(self.validate_serial)
        self.ui.le_serialName.setValidator(None)
        
        self.ui.le_serialName.setText(f"{self.ui.lbl_date.text().replace('-',"")}-{DEFAULTS['SERIAL']:04d}.tif")
    
    
    def validate_serial(self):
        self.ui.le_serialName.setValidator(self.validator)
        if self.ui.le_serialName.hasAcceptableInput():
            self.ui.le_serialName.setStyleSheet("QLineEdit { color: green; }")
            self.ui.btn_copySerial.setEnabled(True)
            self.ui.le_serialName.setValidator(None)
        else:
            self.ui.le_serialName.setStyleSheet("QLineEdit { color: red; }")
            self.ui.btn_copySerial.setEnabled(False)
            self.ui.le_serialName.setValidator(None)