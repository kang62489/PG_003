## Modules
from util.constants import UISizes

class ConcatenatorView:
    def __init__(self, ui):
        self.ui = ui
        self.setup_ui()
        
    def setup_ui(self):
        self.setup_listview()
        self.setup_groupbox()
        
    
    def setup_listview(self):
        pass
    
    def setup_groupbox(self):
        self.ui.groupBox_concat_status.setFixedHeight(2*UISizes.GROUP_BOX_STATUS_HEIGHT)
        