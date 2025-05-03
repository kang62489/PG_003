## Modules
import sys
from rich import print
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader

from views import (
    RecTaggerView,
)

from controllers import (
    RecTaggerHandlers,
    )

from util.constants import (
    APP_NAME,
    APP_STATUS_MESSAGE,
    UI_FILE, 
    STYLE_FILE,
    DEFAULTS
)

class MainPanel:
    def __init__(self):
        super().__init__()
        self.loader = QUiLoader()
        self.ui = self.loader.load(UI_FILE, None)
        self.ui.setWindowTitle(APP_NAME)
        self.ui.show()
        
        with open(STYLE_FILE, "r") as f:
            self.ui.setStyleSheet(f.read())
        
        # Set status bar message
        self.ui.statusbar.showMessage(APP_STATUS_MESSAGE)
        
        # Initialize tab managers
        RecTaggerView(self.ui, self)
        
        # Set default tab index
        self.ui.tabs.setCurrentIndex(DEFAULTS["TAB_INDEX"])
        
        # Connect signals
        self.handlers_expinfo = RecTaggerHandlers(self.ui)

app = QApplication(sys.argv)
window = MainPanel()

app.exec()
