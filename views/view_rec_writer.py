## Modules
# Standard Library imports
import os
from datetime import datetime

# Third-party imports
from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import QAbstractItemView, QButtonGroup, QHeaderView

# Local application imports
from classes import DelegateCellEdit
from util.constants import BASE_DIR, DEFAULTS, DISPLAY_DATE_FORMAT, MenuOptions, UIAlignments, UISizes


class ViewRecWriter:
    """Handles UI configuration for Template Manager tab (tab_0)"""

    def __init__(self, ui):
        self.ui = ui
        self.setup_ui()

    def setup_ui(self):
        self.setup_pushbuttons()
        self.setup_groupboxes()
        self.setup_radiobuttons()
        self.setup_lineedits()
        self.setup_tableview()
        self.setup_comboboxes()
        self.setup_spinboxes()
        self.setup_toggle_buttons()
        self.setup_stacked_widget()
        self.setup_textedits()

    def setup_groupboxes(self):
        self.ui.lbl_expDate.setText(f"Experiment Date: {datetime.today().strftime(DISPLAY_DATE_FORMAT)}")

    def setup_radiobuttons(self):
        self.ui.radioBtnGroup_OBJ = QButtonGroup()
        self.ui.radioBtnGroup_OBJ.addButton(self.ui.rb_10X)
        self.ui.radioBtnGroup_OBJ.addButton(self.ui.rb_40X)
        self.ui.radioBtnGroup_OBJ.addButton(self.ui.rb_60X)
        self.ui.rb_60X.setChecked(True)

    def setup_lineedits(self):
        self.ui.le_EXPO.setText(DEFAULTS["EXPOSURE_TIME"])
        self.ui.le_EXPO.setFixedSize(UISizes.LINE_EDIT_EXPO_WIDTH, UISizes.LINE_EDIT_EXPO_HEIGHT)

        self.ui.le_FPS.setText(DEFAULTS["FPS"])
        self.ui.le_FPS.setFixedHeight(UISizes.LINE_EDIT_FPS_HEIGHT)

        self.ui.le_filenameSN.setFixedHeight(UISizes.LINE_EDIT_FSN_HEIGHT)
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

        buttons_for_row_op = [
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
            btn.setFixedSize(UISizes.BUTTON_TEMPLATE)

        for btn in buttons_for_row_op:
            btn.setFixedHeight(UISizes.BUTTON_ROWOP_HEIGHT)

        for btn in buttons_for_SN:
            btn.setFixedSize(UISizes.BUTTON_SN)

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

        # Set fixed height
        table.setFixedHeight(UISizes.TABLEVIEW_CUSTOMIZED_HEIGHT)

    def setup_comboboxes(self):
        self.ui.cb_EXC.addItems(MenuOptions.EXCITATION)
        self.ui.cb_EXC.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

        self.ui.cb_EMI.addItems(MenuOptions.EMISSION)
        self.ui.cb_EMI.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

        self.ui.cb_EXPO_UNIT.addItems(MenuOptions.EXPO_UNITS)
        self.ui.cb_EXPO_UNIT.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

        self.ui.cb_LOC_TYPE.addItems(MenuOptions.LOC_TYPES)
        self.ui.cb_LOC_TYPE.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

        self.ui.cb_SIDE.addItems(MenuOptions.SIDE)
        self.ui.cb_SIDE.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

        self.ui.cb_TemplateLoad.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

        self.ui.cb_recFiles.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

    def setup_spinboxes(self):
        # LEVEL spinbox (replaces le_LEVEL): 0-9, 10=MAX
        self.ui.sb_LEVEL.setValue(10)  # Default to MAX
        self.ui.sb_LEVEL.setRange(0, 10)
        self.ui.sb_LEVEL.setFixedHeight(UISizes.SPIN_TAB1_HEIGHT)

        # FRAMES spinbox (replaces le_FRAMES)
        self.ui.sb_FRAMES.setValue(1200)
        self.ui.sb_FRAMES.setRange(1, 99999)
        self.ui.sb_FRAMES.setFixedHeight(UISizes.SPIN_TAB1_HEIGHT)

        self.ui.sb_SLICE.setValue(1)
        self.ui.sb_SLICE.setRange(1, 10)
        self.ui.sb_SLICE.setFixedHeight(UISizes.SPIN_TAB1_HEIGHT)

        self.ui.sb_AT.setValue(1)
        self.ui.sb_AT.setRange(1, 100)
        self.ui.sb_AT.setFixedHeight(UISizes.SPIN_TAB1_HEIGHT)

    def setup_toggle_buttons(self):
        """Setup toggle buttons for switching between Basic and Customized parameters"""
        # Create button group for exclusive selection
        self.ui.toggleBtnGroup = QButtonGroup()
        self.ui.toggleBtnGroup.addButton(self.ui.btn_toggleBasic, 0)
        self.ui.toggleBtnGroup.addButton(self.ui.btn_toggleCustomized, 1)
        self.ui.toggleBtnGroup.setExclusive(True)

        # Set initial state
        self.ui.btn_toggleBasic.setChecked(True)

    def setup_stacked_widget(self):
        """Setup stacked widget for parameter pages"""
        self.ui.stack_parameters.setCurrentIndex(0)  # Show Basic page by default
        self.ui.stack_parameters.setFixedHeight(UISizes.STACK_PARAMETERS_HEIGHT)

    def setup_textedits(self):
        self.ui.te_recDir.setPlainText(os.path.join(BASE_DIR))
        self.ui.te_recDir.setFixedHeight(UISizes.TEXT_EDIT_RECDIR_HEIGHT)
        self.ui.te_recDir.setAlignment(UIAlignments.TOP_CENTER)
        self.ui.te_recDir.setWordWrapMode(QTextOption.WrapAnywhere)
