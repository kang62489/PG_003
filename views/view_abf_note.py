## Modules

# Local application imports
from util.constants import MenuOptions


class ViewAbfNote:
    def __init__(self, main_ui):
        self.ui = main_ui
        self.setup_ui()

    def setup_ui(self):
        self.setup_spinbox()
        self.setup_combobox()

    def setup_spinbox(self):
        self.ui.sb_abfSlice.setValue(self.ui.sb_SLICE.value())
        self.ui.sb_abfSlice.setRange(1, 10)

        self.ui.sb_abfAt.setValue(self.ui.sb_AT.value())
        self.ui.sb_abfAt.setRange(1, 10)

    def setup_combobox(self):
        self.ui.cb_abfSide.addItems(MenuOptions.SIDE)
        self.ui.cb_abfAtType.addItems(MenuOptions.LOC_TYPES)
