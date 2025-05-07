## Modules
import sys
from resources import resources
from rich import print
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader

from views import (
    ExpInfoView,
    RecTaggerView
)

from controllers import (
    ExpInfoHandlers,
    RecTaggerHandlers
    )

from util.constants import (
    APP_NAME,
    APP_STATUS_MESSAGE,
    UI_FILE, 
    STYLE_FILE,
    DEFAULTS
)
loader = QUiLoader()
class MainPanel:  # Inherit from QObject
    def __init__(self):
        # Load the UI
        self.ui = loader.load(UI_FILE, None)
        self.ui.setWindowTitle(APP_NAME)

        # Apply styles
        with open(STYLE_FILE, "r") as f:
            self.ui.setStyleSheet(f.read())

        # Set status bar message
        self.ui.statusbar.showMessage(APP_STATUS_MESSAGE)

        # Initialize tab managers
        ExpInfoView(self.ui, self)
        RecTaggerView(self.ui, self)

        # Initialize tab handlers
        self.handlers_expInfo = ExpInfoHandlers(self.ui)
        self.handlers_recTagger = RecTaggerHandlers(self.ui)

        # Set default tab index
        self.ui.tabs.setCurrentIndex(DEFAULTS["TAB_INDEX"])

        # Show the window
        self.ui.show()


app = QApplication([])
window = MainPanel()

app.exec()
