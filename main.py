## Modules
# Standard library imports
import os
from pathlib import Path

# Third-party imports
from PySide6.QtGui import QFont
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

# Local application imports
from controllers import (
    TAB_EXP_Handlers,
    TAB_REC_DB_Handlers,
    TAB_REC_Handlers,
)

# Import resources.py for qss file (using noqa to ignore unused import warning)
from resources import resources  # noqa: F401
from util.constants import APP_NAME, APP_STATUS_MESSAGE, DEFAULTS, STYLE_FILE, UI_FILE
from views import (
    TAB_EXP_View,
    TAB_REC_DB_View,
    TAB_REC_View,
)

loader = QUiLoader()


class MainPanel:  # Inherit from QObject
    def __init__(self) -> None:
        # Load the UI
        self.ui = loader.load(UI_FILE, None)
        self.ui.setWindowTitle(APP_NAME)

        # Load custom font and set it
        self.default_font = QFont("Calibri", 12)
        # font_id = QFontDatabase.addApplicationFont(
        #     "resources/fonts/HACKNERDFONTMONO-REGULAR.TTF",
        # )
        # if font_id == -1:
        #     rich.print("[red]Error loading font: Hack Nerd Font Mono[/red]")
        #     self.ui.setFont(self.default_font)
        # else:
        #     font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        #     self.ui.setFont(QFont(font_family, 12))

        # Apply styles
        with Path.open(STYLE_FILE) as f:
            self.ui.setStyleSheet(f.read())

        # Set status bar message
        self.ui.statusbar.showMessage(APP_STATUS_MESSAGE)

        # Initialize tab managers
        TAB_EXP_View(self.ui)
        TAB_REC_View(self.ui)
        TAB_REC_DB_View(self.ui)

        # Initialize tab handlers
        self.handlers_expInfo = TAB_EXP_Handlers(self.ui)
        self.handlers_recTagger = TAB_REC_Handlers(self.ui)
        self.handlers_recDB = TAB_REC_DB_Handlers(self.ui)
        # Set default tab index
        self.ui.tabs.setCurrentIndex(DEFAULTS["TAB_INDEX"])

        # Show the window
        self.ui.show()


os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"

app = QApplication([])
app.setStyle("fusion")
window = MainPanel()
app.exec()
