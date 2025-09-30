# Modules
import os
from datetime import datetime

from PySide6.QtWidgets import QAbstractItemView, QButtonGroup, QHeaderView

from classes.customized_delegate import CellEditDelegate
from util.constants import (
    BASE_DIR,
    DEFAULTS,
    DISPLAY_DATE_FORMAT,
    MenuOptions,
    UIAlignments,
    UISizes,
)


class TAB_REC_View:
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
        self.ui.groupBox_recBasic.setTitle(
            f"Experiment Date: {datetime.today().strftime(DISPLAY_DATE_FORMAT)}"
        )
        self.ui.groupBox_recBasic.setFixedWidth(UISizes.GROUP_BOX_WIDTH_LEFT_COLUMN)
        self.ui.groupBox_recCustomized.setFixedWidth(
            UISizes.GROUP_BOX_WIDTH_LEFT_COLUMN
        )

        self.ui.groupBox_tagOutput.setFixedWidth(UISizes.GROUP_BOX_WIDTH_RIGHT_COLUMN)
        self.ui.groupBox_status.setFixedHeight(UISizes.GROUP_BOX_STATUS_HEIGHT)

    def setup_radiobuttons(self):
        self.ui.radioBtnGroup_OBJ = QButtonGroup()
        self.ui.radioBtnGroup_OBJ.addButton(self.ui.radioBtn_10X)
        self.ui.radioBtnGroup_OBJ.addButton(self.ui.radioBtn_40X)
        self.ui.radioBtnGroup_OBJ.addButton(self.ui.radioBtn_60X)
        self.ui.radioBtn_60X.setChecked(True)

    def setup_lineedits(self):
        self.ui.lineEdit_LEVEL.setText(DEFAULTS["LIGHT_INENSITY"])
        self.ui.lineEdit_EXPO.setText(DEFAULTS["EXPOSURE_TIME"])
        self.ui.lineEdit_EXPO.setFixedWidth(UISizes.LINE_EDIT_EXPO_WIDTH)
        self.ui.lineEdit_FRAMES.setText(DEFAULTS["FRAMES"])
        self.ui.lineEdit_FPS.setText(DEFAULTS["FPS"])

        self.ui.lineEdit_recDir.setText(os.path.join(BASE_DIR))

        self.ui.lineEdit_filenameSN.setFixedHeight(UISizes.LINE_EDIT_HEIGHT)
        self.ui.lineEdit_filenameSN.setAlignment(UIAlignments.CENTER)
        self.ui.lineEdit_filenameSN.setPlaceholderText("YYYY_MM_DD-0000")
        self.ui.lineEdit_filenameSN.setText(
            f"{datetime.today().strftime(DISPLAY_DATE_FORMAT)}-{DEFAULTS['SERIAL']:04d}.tif"
        )

    def setup_checkboxes(self):
        self.ui.checkBox_addCustomized.setChecked(False)

    def setup_pushbuttons(self):
        buttons_for_template = [
            self.ui.btn_saveTemplate,
            self.ui.btn_deleteCurrentTemplate,
        ]

        buttons_for_editting = [
            self.ui.btn_removeSelectedRows,
            self.ui.btn_addNewRows,
            self.ui.btn_moveUp,
            self.ui.btn_moveDown,
        ]

        buttons_for_SN = [
            self.ui.btn_increaseSN,
            self.ui.btn_decreaseSN,
            self.ui.btn_resetSN,
            self.ui.btn_copyFilenameSN,
        ]

        for btn in buttons_for_template:
            btn.setFixedSize(UISizes.BUTTON_SMALL)

        for btn in buttons_for_editting:
            btn.setFixedSize(UISizes.BUTTON_SMALL)

        for btn in buttons_for_SN:
            btn.setFixedSize(UISizes.BUTTON_TINY)

        # Initial button states
        self.ui.btn_deleteCurrentTemplate.setEnabled(False)

    def setup_tableview(self):
        table = self.ui.tableView_customized
        # Alignment
        table.verticalHeader().setDefaultAlignment(UIAlignments.LEFT_CENTER)

        # Display settings
        table.horizontalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setDefaultSectionSize(30)
        table.setEditTriggers(
            QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed
        )
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
