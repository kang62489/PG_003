# Modules
from PySide6.QtWidgets import QHeaderView, QAbstractItemView, QButtonGroup
from classes.customized_delegate import CellEditDelegate
from datetime import datetime
from util.constants import (
    UISizes, 
    UIAlignments,
    MenuOptions,
    DISPLAY_DATE_FORMAT,
    DEFAULTS
)

class RecTaggerView:
    """Handles UI configuration for Template Manager tab (tab_0)"""
    def __init__(self, ui, main_panel):
        self.ui = ui
        self.main = main_panel
        self.setup_ui()
        
    def setup_ui(self):
        self.setup_labels()
        self.setup_pushbuttons()
        self.setup_groupboxes()
        self.setup_radiobuttons()
        self.setup_lineedits()
        self.setup_tableview()
        self.setup_comboboxes()
        self.setup_spinboxes()
        
    def setup_labels(self):
        self.ui.lbl_OBJ.setText("Objective Magnification: ")
        self.ui.lbl_EXC.setText("Excitation Light: ")
        self.ui.lbl_LEVEL.setText("Excitation Level: ")
        self.ui.lbl_EXPO.setText("Exposure Time: ")
        self.ui.lbl_EMI.setText("Emission Light: ")
        self.ui.lbl_FRAMES.setText("Number of Frames: ")
        self.ui.lbl_CAM_TRIG_MODE.setText("Camera Trigger Mode: ")
        self.ui.lbl_SLICE.setText("Slice Number: ")
    
    def setup_groupboxes(self):
        self.ui.groupBox_recBasic.setTitle(f"Experiment Date: {datetime.today().strftime(DISPLAY_DATE_FORMAT)}")
    
    def setup_radiobuttons(self):
        self.ui.radioBtnGroup_obj = QButtonGroup()
        self.ui.radioBtnGroup_obj.addButton(self.ui.radioBtn_10X)
        self.ui.radioBtnGroup_obj.addButton(self.ui.radioBtn_40X)
        self.ui.radioBtnGroup_obj.addButton(self.ui.radioBtn_60X)
        self.ui.radioBtn_60X.setChecked(True)

    def setup_lineedits(self):
        self.ui.lineEdit_LEVEL.setText(DEFAULTS["LIGHT_INENSITY"])
        self.ui.lineEdit_EXPO.setText(DEFAULTS["EXPOSURE_TIME"])
        self.ui.lineEdit_FRAMES.setText(DEFAULTS["FRAMES"])
        self.ui.lineEdit_FPS.setText(DEFAULTS["FPS"])
    
    def setup_pushbuttons(self):
        buttons = [
            self.ui.btn_loadTemplate,
            self.ui.btn_saveTemplate,
            self.ui.btn_newTemplate,
            self.ui.btn_deleteCurrentTemplate,
            self.ui.btn_removeSelectedRows,
            self.ui.btn_addNewRows,
            self.ui.btn_moveUp,
            self.ui.btn_moveDown
        ]
        
        for btn in buttons[0:4]:
            btn.setFixedSize(UISizes.BUTTON_SMALL)
            
        # Initial button states
        self.ui.btn_deleteCurrentTemplate.setEnabled(False)
    
        
    def setup_tableview(self):
        table = self.ui.tableView_customized
        # Alignment
        table.verticalHeader().setDefaultAlignment(UIAlignments.RIGHT_CENTER)
        
        # Display settings
        table.horizontalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setDefaultSectionSize(50)
        table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        table.setItemDelegate(CellEditDelegate())
        
    def setup_comboboxes(self):
        self.ui.comboBox_EXC.addItems(MenuOptions.EXCITATION)
        self.ui.comboBox_EMI.addItems(MenuOptions.EMISSION)
        self.ui.comboBox_EXPO_UNITS.addItems(MenuOptions.EXPO_UNITS)
        self.ui.comboBox_CAM_TRIG_MODES.addItems(MenuOptions.CAM_TRIG_MODES)
        self.ui.comboBox_LOC_TYPES.addItems(MenuOptions.LOC_TYPES)
        self.ui.comboBox_tagTemplates.setFixedSize(UISizes.COMBO_STANDARD)
    
    def setup_spinboxes(self):
        self.ui.spinBox_SLICE.setValue(1)
        self.ui.spinBox_SLICE.setRange(1, 10)
        
        self.ui.spinBox_AT.setValue(1)
        self.ui.spinBox_AT.setRange(1, 100)
