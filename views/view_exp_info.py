## Modules
# Standard library imports
from datetime import datetime

# Third-party imports
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QAbstractItemView, QHeaderView

# Local application imports
from util.constants import MenuOptions, UISizes


class ViewExpInfo:
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
        self.ui.gb_fileIO.setFixedSize(UISizes.GROUP_BOX_ROW1_WIDTH, UISizes.GROUP_BOX_ROW1_HEIGHT)
        self.ui.gb_basics.setFixedSize(UISizes.GROUP_BOX_ROW2_WIDTH, UISizes.GROUP_BOX_ROW2_HEIGHT)
        self.ui.gb_solutions.setFixedSize(UISizes.GROUP_BOX_ROW2_WIDTH, UISizes.GROUP_BOX_ROW2_HEIGHT)
        self.ui.gb_animals.setFixedSize(UISizes.GROUP_BOX_ROW3_WIDTH, UISizes.GROUP_BOX_ROW3_HEIGHT)
        self.ui.gb_injections.setFixedWidth(UISizes.GROUP_BOX_ROW3_WIDTH)

    def setup_dateedit(self):
        dateEdits = [
            self.ui.de_DOR,
            self.ui.de_DOB,
        ]
        for dateEdit in dateEdits:
            dateEdit.setDate(datetime.today())
            dateEdit.setCalendarPopup(True)

    def setup_lineedits(self):
        self.ui.le_project.setText("SPIKE_TRIGGERED_ACH_DOMAIN")

        self.ui.le_cuttingOS.setFixedWidth(UISizes.LINE_EDIT_OS_WIDTH)
        self.ui.le_holdingOS.setFixedWidth(UISizes.LINE_EDIT_OS_WIDTH)
        self.ui.le_recordingOS.setFixedWidth(UISizes.LINE_EDIT_OS_WIDTH)

        self.ui.le_animalID.setFixedWidth(UISizes.LINE_EDIT_ID_WIDTH)

    def setup_comboboxes(self):
        self.ui.cb_ACUC.addItems(MenuOptions.ACUC_PNS)
        self.ui.cb_ACUC.setCurrentIndex(1)

        self.ui.cb_SPECIES.addItems(MenuOptions.SPECIES)
        self.ui.cb_GENOTYPE.addItems(MenuOptions.GENOTYPE)
        self.ui.cb_SEX.addItems(MenuOptions.SEX)

        self.ui.cb_GENOTYPE.setFixedWidth(UISizes.COMBO_GENOTYPE_WIDTH)

    def setup_treeview(self):
        # Set column resize mode
        self.ui.tree_injections.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Enable multiple selection (Ctrl+Click or Shift+Click) for deletion
        self.ui.tree_injections.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Enable word wrap and auto-adjust row height
        self.ui.tree_injections.setWordWrap(True)
        self.ui.tree_injections.setUniformRowHeights(False)

        # Set default font size
        tree_font = QFont()
        tree_font.setPointSize(12)
        self.ui.tree_injections.setFont(tree_font)
