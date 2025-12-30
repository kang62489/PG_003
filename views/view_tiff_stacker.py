# Third-party imports
# Local application imports
from classes import DelegateCheckableListItem
from util.constants import UISizes


class ViewTiffStacker:
    def __init__(self, ui):
        self.ui = ui
        self.setup_ui()

    def setup_ui(self):
        # NOTE: The following widgets do not exist in the current UI file (Expdata Manager.ui)
        # A tab with TIFF stacker functionality needs to be added to the UI file
        # Required widgets: lv_recFiles, gb_concat_status, pb_concatenation,
        # btn_BrowseTiffs, btn_StartConcat
        pass
        # self.setup_listview()
        # self.setup_groupbox()
        # self.setup_progressbar()
        # self.setup_pushbuttons()

    def setup_listview(self):
        # WARNING: Widget 'lv_recFiles' does not exist in current UI
        checkbox_delegate = DelegateCheckableListItem()
        self.ui.lv_recFiles.setItemDelegate(checkbox_delegate)

    def setup_groupbox(self):
        # WARNING: Widget 'gb_concat_status' does not exist in current UI
        self.ui.gb_concat_status.setFixedHeight(2 * UISizes.GROUP_BOX_STATUS_HEIGHT)

    def setup_progressbar(self):
        # WARNING: Widget 'pb_concatenation' does not exist in current UI
        self.ui.pb_concatenation.setFixedHeight(UISizes.PROGRESSBAR_HEIGHT)

    def setup_pushbuttons(self):
        # WARNING: Widgets 'btn_BrowseTiffs' and 'btn_StartConcat' do not exist in current UI
        self.ui.btn_BrowseTiffs.setFixedSize(UISizes.BUTTON_SMALL)
        self.ui.btn_StartConcat.setFixedHeight(UISizes.BUTTON_LONG_HEIGHT)
