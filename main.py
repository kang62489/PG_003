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
    ConcatenatorHandlers,
    ExpInfoHandlers,
    RecDBHandlers,
    RecTaggerHandlers,
)

# Import resources.py for qss file (using noqa to ignore unused import warning)
from resources import resources  # noqa: F401
from util.constants import APP_NAME, APP_STATUS_MESSAGE, DEFAULTS, STYLE_FILE, UI_FILE
from views import ConcatenatorView, ExpInfoView, RecDBView, RecTaggerView

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


os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"

app = QApplication([])
app.setStyle("fusion")
window = MainPanel()
app.exec()
