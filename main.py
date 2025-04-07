## Modules
import os
import sys
from pathlib import Path
from rich import print
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader

from views import (
    view_expinfo,
    view_parameters
)

from controllers import (
    HandlersExpInfo,
    HandlersParameters
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
        view_expinfo.ExpInfoView(self.ui, self)
        view_parameters.ParametersView(self.ui, self)
        
        # Set default tab index
        self.ui.tab_main.setCurrentIndex(DEFAULTS["TAB_INDEX"])
        
        # Connect signals
        self.handlers_expinfo = HandlersExpInfo(self.ui)
        self.handlers_parameters = HandlersParameters(self.ui)

app = QApplication(sys.argv)
window = MainPanel()

app.exec()
