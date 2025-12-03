## Modules
# Standard library imports
from datetime import datetime

# Third-party imports
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QAbstractItemView, QHeaderView

# Local application imports
from util.constants import MenuOptions, UISizes


class TAB_EXP_View:
    def __init__(self, ui):
        self.ui = ui
        self.setup_ui()

    def setup_ui(self):
        self.setup_groupboxes()
        self.setup_dateedit()
        self.setup_lineedits()
        self.setup_comboboxes()
        self.setup_treeview()

    def setup_groupboxes(self):
        self.ui.groupBox_fileIO.setFixedSize(UISizes.GROUP_BOX_ROW1_WIDTH, UISizes.GROUP_BOX_ROW1_HEIGHT)
        self.ui.groupBox_basics.setFixedSize(UISizes.GROUP_BOX_ROW2_WIDTH, UISizes.GROUP_BOX_ROW2_HEIGHT)
        self.ui.groupBox_solutions.setFixedSize(UISizes.GROUP_BOX_ROW2_WIDTH, UISizes.GROUP_BOX_ROW2_HEIGHT)
        self.ui.groupBox_animals.setFixedSize(UISizes.GROUP_BOX_ROW3_WIDTH, UISizes.GROUP_BOX_ROW3_HEIGHT)
        self.ui.groupBox_injections.setFixedWidth(UISizes.GROUP_BOX_ROW3_WIDTH)

    def setup_dateedit(self):
        dateEdits = [
            self.ui.dateEdit_DOR,
            self.ui.dateEdit_DOB,
        ]
        for dateEdit in dateEdits:
            dateEdit.setDate(datetime.today())
            dateEdit.setCalendarPopup(True)

    def setup_lineedits(self):
        self.ui.lineEdit_project.setText("SPIKE_TRIGGERED_ACH_DOMAIN")

        self.ui.lineEdit_cuttingOS.setFixedWidth(UISizes.LINE_EDIT_OS_WIDTH)
        self.ui.lineEdit_holdingOS.setFixedWidth(UISizes.LINE_EDIT_OS_WIDTH)
        self.ui.lineEdit_recordingOS.setFixedWidth(UISizes.LINE_EDIT_OS_WIDTH)

        self.ui.lineEdit_animalID.setFixedWidth(UISizes.LINE_EDIT_ID_WIDTH)

    def setup_comboboxes(self):
        self.ui.comboBox_ACUC.addItems(MenuOptions.ACUC_PNS)
        self.ui.comboBox_ACUC.setCurrentIndex(1)

        self.ui.comboBox_species.addItems(MenuOptions.SPECIES)
        self.ui.comboBox_genotype.addItems(MenuOptions.GENOTYPE)
        self.ui.comboBox_sex.addItems(MenuOptions.SEX)

        self.ui.comboBox_genotype.setFixedWidth(UISizes.COMBO_GENOTYPE_WITDH)

    def setup_treeview(self):
        # Set column resize mode
        self.ui.treeView_injections.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Enable multiple selection (Ctrl+Click or Shift+Click) for deletion
        self.ui.treeView_injections.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Enable word wrap and auto-adjust row height
        self.ui.treeView_injections.setWordWrap(True)
        self.ui.treeView_injections.setUniformRowHeights(False)

        # Set default font size
        tree_font = QFont()
        tree_font.setPointSize(12)
        self.ui.treeView_injections.setFont(tree_font)
