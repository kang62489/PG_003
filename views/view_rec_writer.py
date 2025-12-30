# Modules
import os
from datetime import datetime

from PySide6.QtWidgets import QAbstractItemView, QButtonGroup, QHeaderView

from classes import DelegateCellEdit
from util.constants import (
    BASE_DIR,
    DEFAULTS,
    DISPLAY_DATE_FORMAT,
    MenuOptions,
    UIAlignments,
    UISizes,
)


class ViewRecWriter:
    """Handles UI configuration for Template Manager tab (tab_0)"""

    def __init__(self, ui):
        self.ui = ui
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
        self.ui.gb_recBasic.setTitle(f"Experiment Date: {datetime.today().strftime(DISPLAY_DATE_FORMAT)}")
        self.ui.gb_recBasic.setFixedWidth(UISizes.GROUP_BOX_WIDTH_LEFT_COLUMN)
        self.ui.gb_recCustomized.setFixedWidth(UISizes.GROUP_BOX_WIDTH_LEFT_COLUMN)

        self.ui.gb_tagOutput.setFixedWidth(UISizes.GROUP_BOX_WIDTH_RIGHT_COLUMN)
        self.ui.gb_status.setFixedHeight(UISizes.GROUP_BOX_STATUS_HEIGHT)

    def setup_radiobuttons(self):
        self.ui.radioBtnGroup_OBJ = QButtonGroup()
        self.ui.radioBtnGroup_OBJ.addButton(self.ui.rb_10X)
        self.ui.radioBtnGroup_OBJ.addButton(self.ui.rb_40X)
        self.ui.radioBtnGroup_OBJ.addButton(self.ui.rb_60X)
        self.ui.rb_60X.setChecked(True)

    def setup_lineedits(self):
        self.ui.le_LEVEL.setText(DEFAULTS["LIGHT_INTENSITY"])
        self.ui.le_EXPO.setText(DEFAULTS["EXPOSURE_TIME"])
        self.ui.le_EXPO.setFixedWidth(UISizes.LINE_EDIT_EXPO_WIDTH)
        self.ui.le_FRAMES.setText(DEFAULTS["FRAMES"])
        self.ui.le_FPS.setText(DEFAULTS["FPS"])

        self.ui.le_recDir.setText(os.path.join(BASE_DIR))

        self.ui.le_filenameSN.setFixedHeight(UISizes.LINE_EDIT_HEIGHT)
        self.ui.le_filenameSN.setAlignment(UIAlignments.CENTER)
        self.ui.le_filenameSN.setPlaceholderText("YYYY_MM_DD-0000")
        self.ui.le_filenameSN.setText(f"{datetime.today().strftime(DISPLAY_DATE_FORMAT)}-{DEFAULTS['SERIAL']:04d}.tif")

    def setup_checkboxes(self):
        self.ui.chk_addCustomized.setChecked(False)

    def setup_pushbuttons(self):
        buttons_for_template = [
            self.ui.btn_TemplateSave,
            self.ui.btn_TemplateDelete,
        ]

        buttons_for_editting = [
            self.ui.btn_RmSelectedRows,
            self.ui.btn_InsertCustomProps,
            self.ui.btn_MvRowsUp,
            self.ui.btn_MvRowsDown,
        ]

        buttons_for_SN = [
            self.ui.btn_SnInc,
            self.ui.btn_SnDec,
            self.ui.btn_SnReset,
            self.ui.btn_SnCopy,
        ]

        for btn in buttons_for_template:
            btn.setFixedSize(UISizes.BUTTON_SMALL)

        for btn in buttons_for_editting:
            btn.setFixedSize(UISizes.BUTTON_SMALL)

        for btn in buttons_for_SN:
            btn.setFixedSize(UISizes.BUTTON_TINY)

        # Initial button states
        self.ui.btn_TemplateDelete.setEnabled(False)

    def setup_tableview(self):
        table = self.ui.tv_customized
        # Alignment
        table.verticalHeader().setDefaultAlignment(UIAlignments.LEFT_CENTER)

        # Display settings
        table.horizontalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setDefaultSectionSize(30)
        table.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
        table.setItemDelegate(DelegateCellEdit())

    def setup_comboboxes(self):
        self.ui.cb_EXC.addItems(MenuOptions.EXCITATION)
        self.ui.cb_EMI.addItems(MenuOptions.EMISSION)
        self.ui.cb_EXPO_UNIT.addItems(MenuOptions.EXPO_UNITS)
        self.ui.cb_CAM_TRIG_MODE.addItems(MenuOptions.CAM_TRIG_MODES)
        self.ui.cb_LOC_TYPE.addItems(MenuOptions.LOC_TYPES)
        self.ui.cb_TemplateLoad.setFixedSize(UISizes.COMBO_STANDARD)

    def setup_spinboxes(self):
        self.ui.sb_SLICE.setValue(1)
        self.ui.sb_SLICE.setRange(1, 10)

        self.ui.sb_AT.setValue(1)
        self.ui.sb_AT.setRange(1, 100)
