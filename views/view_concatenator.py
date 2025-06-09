## Modules
from util.constants import UISizes
from classes import customized_delegate

class ConcatenatorView:
    def __init__(self, ui):
        self.ui = ui
        self.setup_ui()
        
    def setup_ui(self):
        self.setup_listview()
        self.setup_groupbox()
        self.setup_progressbar()
        self.setup_pushbuttons()
    
    
    def setup_listview(self):
        checkbox_delegate = customized_delegate.QListViewItemDelegate()
        self.ui.listView_recFiles.setItemDelegate(checkbox_delegate)
        # pass
    
    def setup_groupbox(self):
        self.ui.groupBox_concat_status.setFixedHeight(2*UISizes.GROUP_BOX_STATUS_HEIGHT)
    
    def setup_progressbar(self):
        self.ui.progressBar_concatenation.setFixedHeight(UISizes.PROGRESSBAR_HEIGHT)

    def setup_pushbuttons(self):
        self.ui.btn_browse_tiffs.setFixedSize(UISizes.BUTTON_SMALL)
        self.ui.btn_start_concatenation.setFixedHeight(UISizes.BUTTON_LONG_HEIGHT)
    