## Modules
# Standard library imports
import sys
from pathlib import Path

# Third-party imports
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from rich import print

# Local application imports
from controllers import (
    CtrlAbfNote,
    CtrlExpInfo,
    CtrlRecImport,
    CtrlRecWriter,
    CtrlTiffStacker,
)
from resources import (
    resources,  # noqa: F401 (Import resources.py for qss file,using # noqa to ignore unused import warning)
)
from util.constants import APP_NAME, APP_STATUS_MESSAGE, DEFAULTS, STYLE_FILE, UI_FILE
from views import (
    ViewAbfNote,
    ViewExpInfo,
    ViewRecImport,
    ViewRecWriter,
    ViewTiffStacker,
)

loader = QUiLoader()


class Main:
    def __init__(self) -> None:
        # Load the UI
        self.ui = loader.load(UI_FILE, None)
        self.ui.setWindowTitle(APP_NAME)

        self.ui.setFixedSize(self.ui.size())

        # Load custom fonts
        self.default_font = QFont("Calibri", 12)
        font_dir = Path(__file__).parent / "resources" / "fonts"
        fonts_loaded = False

        for font_file in font_dir.glob("*.ttf"):
            font_id = QFontDatabase.addApplicationFont(str(font_file))
            if font_id != -1:
                fonts_loaded = True

        # Set font once after loading all
        if fonts_loaded:
            self.ui.setFont(QFont("FantasqueSansM Nerd Font Mono", 12))
        else:
            print("[red]All fonts failed to load, using Calibri[/red]")
            self.ui.setFont(self.default_font)

        # Apply styles
        with Path.open(STYLE_FILE) as f:
            self.ui.setStyleSheet(f.read())

        # Set status bar message
        self.ui.statusbar.showMessage(APP_STATUS_MESSAGE)

        # Initialize tab managers
        ViewExpInfo(self.ui)
        ViewRecWriter(self.ui)
        ViewRecImport(self.ui)
        ViewTiffStacker(self.ui)
        ViewAbfNote(self.ui)

        # Initialize tab handlers (need to add handler instances to self to access uis in self.ui)
        self.handlers_expInfo = CtrlExpInfo(self.ui)
        self.handlers_recTagger = CtrlRecWriter(self.ui)
        self.handlers_recDB = CtrlRecImport(self.ui)
        self.handlers_tiffStacker = CtrlTiffStacker(self.ui)
        self.handlers_abfNote = CtrlAbfNote(self.ui)
        # Set default tab index
        self.ui.tabs.setCurrentIndex(DEFAULTS["TAB_INDEX"])

        # Show the window
        self.ui.show()


if sys.platform == "win32":
    sys.argv += ["-platform", "windows:darkmode=0"]

app = QApplication(sys.argv)
app.setStyle("Fusion")
window = Main()
app.exec()
