## Modules
import sys
from resources import resources
from rich import print
from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QFontDatabase, QFont


from views import (
    ExpInfoView,
    RecTaggerView,
    RecDBView,
    ConcatenatorView
)

from controllers import (
    ExpInfoHandlers,
    RecTaggerHandlers,
    RecDBHandlers,
    ConcatenatorHandlers
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
        
        # Load custom font and set it
        self.default_font = QFont("Calibri", 12)
        font_id = QFontDatabase.addApplicationFont("resources/fonts/HACKNERDFONTMONO-REGULAR.TTF")
        if font_id == -1:
            print("[red]Error loading font: Hack Nerd Font Mono[/red]")
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        self.ui.setFont(self.default_font)
        
        # Apply styles
        with open(STYLE_FILE, "r") as f:
            self.ui.setStyleSheet(f.read())

        # Set status bar message
        self.ui.statusbar.showMessage(APP_STATUS_MESSAGE)

        # Initialize tab managers
        ExpInfoView(self.ui)
        RecTaggerView(self.ui)
        RecDBView(self.ui)
        ConcatenatorView(self.ui)

        # Initialize tab handlers
        self.handlers_expInfo = ExpInfoHandlers(self.ui)
        self.handlers_recTagger = RecTaggerHandlers(self.ui)
        self.handlers_recDB = RecDBHandlers(self.ui)
        self.handlers_concatenator = ConcatenatorHandlers(self.ui)

        # Set default tab index
        self.ui.tabs.setCurrentIndex(DEFAULTS["TAB_INDEX"])

        # Show the window
        self.ui.show()


app = QApplication([])
window = MainPanel()
app.exec()
