# Modules
import os
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from util.constants import (
    UISizes,
    MenuOptions
)

class ExpInfoView:
    def __init__(self, ui, main_panel):
        self.ui = ui
        self.main = main_panel
        self.setup_ui()
        
    def setup_ui(self):
        self.setup_labels()
        self.setup_groupboxes()
        self.setup_dateedit()
        self.setup_lineedits()
        self.setup_checkboxes()
        self.setup_pushbuttons()
        self.setup_comboboxes()
    
    def setup_labels(self):
        self.ui.lbl_DOR.setText(datetime.today().strftime("%Y-%b-%d (%a)"))
        
    def setup_groupboxes(self):
        groupboxes_first_row = [
            self.ui.groupBox_display,
            self.ui.groupBox_fileIO,
        ]
        
        for box in groupboxes_first_row:
            box.setFixedSize(UISizes.GROUP_BOX_ROW1_WIDTH, UISizes.GROUP_BOX_ROW1_HEIGHT)
        
        self.ui.groupBox_basics.setFixedSize(UISizes.GROUP_BOX_ROW2_WIDTH, UISizes.GROUP_BOX_ROW2_HEIGHT_1)
        self.ui.groupBox_solutions.setFixedSize(UISizes.GROUP_BOX_ROW2_WIDTH, UISizes.GROUP_BOX_ROW2_HEIGHT_1)
        self.ui.groupBox_animals.setFixedSize(UISizes.GROUP_BOX_ROW2_WIDTH, UISizes.GROUP_BOX_ROW2_HEIGHT_2)
        self.ui.groupBox_injections.setFixedWidth(UISizes.GROUP_BOX_ROW3_WIDTH)
    
    def setup_dateedit(self):
        dateEdits = [
            self.ui.dateEdit_DOR,
            self.ui.dateEdit_DOB,
            self.ui.dateEdit_DOI,
        ]
        for dateEdit in dateEdits:
            dateEdit.setDate(datetime.today())
            dateEdit.setCalendarPopup(True)
            
    def setup_lineedits(self):
        self.ui.lineEdit_experimenters.setText('Kang')
        self.ui.lineEdit_targetArea.setText('Dorsal Medial Striatum')
        
    def setup_pushbuttons(self):
        tiny_buttons = [
            self.ui.btn_add_ACUC_PN,
            self.ui.btn_rm_ACUC_PN,
            self.ui.btn_add_virus_R,
            self.ui.btn_rm_virus_R,
            self.ui.btn_add_virus_L,
            self.ui.btn_rm_virus_L
        ]
        
        for btn in tiny_buttons:
            btn.setFixedSize(UISizes.BUTTON_TINY_SQUARE)
    
    def setup_checkboxes(self):
        self.ui.checkBox_enable_R.setCheckState(Qt.Checked)
        self.ui.checkBox_enable_L.setCheckState(Qt.Unchecked)
        
    def setup_comboboxes(self):
        self.ui.comboBox_volumeUnit_R.addItems(MenuOptions.VOLUME_UNIT)
        self.ui.comboBox_volumeUnit_L.addItems(MenuOptions.VOLUME_UNIT)
        self.ui.comboBox_injectionMode_R.addItems(MenuOptions.INJECTION_MODE)
        self.ui.comboBox_injectionMode_L.addItems(MenuOptions.INJECTION_MODE)
        self.ui.comboBox_species.addItems(MenuOptions.SPECIES)
        self.ui.comboBox_genotype.addItems(MenuOptions.GENOTYPE)
        self.ui.comboBox_sex.addItems(MenuOptions.SEX)
