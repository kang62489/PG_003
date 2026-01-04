## Modules
# Standard Library imports
import os
from datetime import datetime

# Third-party imports
from PySide6.QtGui import QTextOption
from PySide6.QtWidgets import QAbstractItemView, QButtonGroup, QHeaderView, QLabel

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
        self.ui.radioBtnGroup_OBJ.addButton(self.ui.rb_10x)
        self.ui.radioBtnGroup_OBJ.addButton(self.ui.rb_40x)
        self.ui.radioBtnGroup_OBJ.addButton(self.ui.rb_60x)
        self.ui.rb_60x.setChecked(True)

    def setup_lineedits(self):
        self.ui.le_expo.setText(DEFAULTS["EXPOSURE_TIME"])
        self.ui.le_expo.setFixedSize(UISizes.LINE_EDIT_EXPO_WIDTH, UISizes.LINE_EDIT_EXPO_HEIGHT)

        self.ui.le_fps.setText(DEFAULTS["FPS"])
        self.ui.le_fps.setFixedHeight(UISizes.LINE_EDIT_FPS_HEIGHT)

        self.ui.le_filenameSn.setFixedHeight(UISizes.LINE_EDIT_FSN_HEIGHT)
        self.ui.le_filenameSn.setAlignment(UIAlignments.CENTER)
        self.ui.le_filenameSn.setPlaceholderText("YYYY_MM_DD-0000")
        self.ui.le_filenameSn.setText(f"{datetime.today().strftime(DISPLAY_DATE_FORMAT)}-{DEFAULTS['SERIAL']:04d}.tif")

    def setup_checkboxes(self):
        self.ui.chk_addCustomized.setChecked(False)

    def setup_pushbuttons(self):
        buttons_for_template = [
            self.ui.btn_templateSave,
            self.ui.btn_templateDelete,
        ]

        buttons_for_row_op = [
            self.ui.btn_rmSelectedRows,
            self.ui.btn_insertCustomProps,
            self.ui.btn_mvRowsUp,
            self.ui.btn_mvRowsDown,
        ]

        buttons_for_SN = [
            self.ui.btn_snInc,
            self.ui.btn_snDec,
            self.ui.btn_snReset,
            self.ui.btn_snCopy,
        ]

        for btn in buttons_for_template:
            btn.setFixedSize(UISizes.BUTTON_TEMPLATE)

        for btn in buttons_for_row_op:
            btn.setFixedSize(UISizes.BUTTON_ROWOP)

        for btn in buttons_for_SN:
            btn.setFixedSize(UISizes.BUTTON_SN)

        self.ui.btn_browseRecDir.setFixedSize(UISizes.BUTTON_BROWSE)

        # Initial button states
        self.ui.btn_templateDelete.setEnabled(False)

        self.ui.btn_generateTags.setFixedHeight(UISizes.BUTTON_GENERAL_HEIGHT)
        self.ui.btn_writeRec.setFixedHeight(UISizes.BUTTON_GENERAL_HEIGHT)

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
        self.ui.cb_exc.addItems(MenuOptions.EXCITATION)
        self.ui.cb_exc.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

        self.ui.cb_emi.addItems(MenuOptions.EMISSION)
        self.ui.cb_emi.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

        self.ui.cb_expoUnit.addItems(MenuOptions.EXPO_UNITS)
        self.ui.cb_expoUnit.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

        self.ui.cb_locType.addItems(MenuOptions.LOC_TYPES)
        self.ui.cb_locType.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

        self.ui.cb_side.addItems(MenuOptions.SIDE)
        self.ui.cb_side.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

        self.ui.cb_templateLoad.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

        self.ui.cb_recFiles.setFixedHeight(UISizes.COMBO_TAB1_HEIGHT)

    def setup_spinboxes(self):
        # LEVEL spinbox (replaces le_LEVEL): 0-9, 10=MAX
        self.ui.sb_level.setValue(10)  # Default to MAX
        self.ui.sb_level.setRange(0, 10)
        self.ui.sb_level.setFixedHeight(UISizes.SPIN_TAB1_HEIGHT)

        # FRAMES spinbox (replaces le_FRAMES)
        self.ui.sb_frames.setValue(1200)
        self.ui.sb_frames.setRange(1, 99999)
        self.ui.sb_frames.setFixedHeight(UISizes.SPIN_TAB1_HEIGHT)

        self.ui.sb_slice.setValue(1)
        self.ui.sb_slice.setRange(1, 10)
        self.ui.sb_slice.setFixedHeight(UISizes.SPIN_TAB1_HEIGHT)

        self.ui.sb_at.setValue(1)
        self.ui.sb_at.setRange(1, 10)
        self.ui.sb_at.setFixedHeight(UISizes.SPIN_TAB1_HEIGHT)

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
        self.ui.te_recDir.setAlignment(UIAlignments.TOP)
        self.ui.te_recDir.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
