## Modules
# Standard library imports
from datetime import datetime

# Third-party imports
from PySide6.QtWidgets import QAbstractItemView, QHeaderView

# Local application imports
from classes import DelegateWordWrap
from util.constants import MenuOptions, UIAlignments, UISizes


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
        self.setup_pushbuttons()

    def setup_groupboxes(self):
        # Let layouts handle sizing naturally for 600x800 window
        pass

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

        # Ages display (read-only, gb_animals column 3)
        self.ui.le_ages.setReadOnly(True)
        self.ui.le_ages.setFixedWidth(UISizes.GB_ANIMALS_COL3_WIDTH)

    def setup_comboboxes(self):
        self.ui.cb_ACUC.addItems(MenuOptions.ACUC_PNS)
        self.ui.cb_ACUC.setCurrentIndex(1)

        self.ui.cb_Species.addItems(MenuOptions.SPECIES)
        self.ui.cb_Genotype.addItems(MenuOptions.GENOTYPE)
        self.ui.cb_Sex.addItems(MenuOptions.SEX)

        # gb_animals column 3
        self.ui.cb_Species.setFixedWidth(UISizes.GB_ANIMALS_COL3_WIDTH)
        self.ui.cb_Sex.setFixedWidth(UISizes.GB_ANIMALS_COL3_WIDTH)

    def setup_treeview(self):
        # Set column resize mode
        self.ui.tree_injections.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tree_injections.header().setDefaultAlignment(UIAlignments.CENTER)

        # Enable multiple selection (Ctrl+Click or Shift+Click) for deletion
        self.ui.tree_injections.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # Enable word wrap and auto-adjust row height
        self.ui.tree_injections.setWordWrap(True)
        self.ui.tree_injections.setUniformRowHeights(False)

        # Set delegate for auto-adjusting row height and font sizes
        self.word_wrap_delegate = DelegateWordWrap(self.ui.tree_injections, parent_font_size=12, child_font_size=11)
        self.ui.tree_injections.setItemDelegate(self.word_wrap_delegate)

    def setup_pushbuttons(self):
        self.ui.btn_AddInjections.setFixedHeight(UISizes.BUTTON_GENERAL_HEIGHT)
        self.ui.btn_RmInjections.setFixedHeight(UISizes.BUTTON_GENERAL_HEIGHT)
        self.ui.btn_OpenExpDb.setFixedHeight(UISizes.BUTTON_GENERAL_HEIGHT)
        self.ui.btn_SaveToDb.setFixedHeight(UISizes.BUTTON_GENERAL_HEIGHT)
