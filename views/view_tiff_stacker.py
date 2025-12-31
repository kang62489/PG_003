# Third-party imports
# Local application imports
from classes import DelegateCheckableListItem
from util.constants import UISizes


class ViewTiffStacker:
    def __init__(self, ui):
        self.ui = ui
        self.setup_ui()

    def setup_ui(self):
        self.setup_listview()
        self.setup_groupbox()
        self.setup_progressbar()
        self.setup_pushbuttons()

    def setup_listview(self):
        checkbox_delegate = DelegateCheckableListItem()
        self.ui.lv_recFiles.setItemDelegate(checkbox_delegate)

    def setup_groupbox(self):
        self.ui.gb_concat_status.setFixedHeight(2 * UISizes.GROUP_BOX_STATUS_HEIGHT)

    def setup_progressbar(self):
        self.ui.pb_concatenation.setFixedHeight(UISizes.PROGRESSBAR_HEIGHT)

    def setup_pushbuttons(self):
        self.ui.btn_BrowseTiffs.setFixedSize(UISizes.BUTTON_SMALL)
        self.ui.btn_StartConcat.setFixedHeight(UISizes.BUTTON_LONG_HEIGHT)
