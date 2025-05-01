"""
Constants for the Metadata Generator application.
Author: Kang
"""

from pathlib import Path
from PySide6.QtCore import Qt, QSize
from dataclasses import dataclass

# Application Info
APP_NAME = "ACh Dynamic Analyzer"
APP_VERSION = "1.1.3"
APP_AUTHOR = "Kang"
APP_LAST_UPDATE = "2025-Jan-26"
APP_STATUS_MESSAGE = f"{APP_NAME} {APP_VERSION}, Author: {APP_AUTHOR}, Last Update: {APP_LAST_UPDATE}, Made in OIST"

# Directory Paths
BASE_DIR = Path(__file__).parent.parent
UI_DIR = BASE_DIR / "ui"
STYLES_DIR = BASE_DIR / "styles"
MODELS_DIR = BASE_DIR / "data"

# File Paths
UI_FILE = UI_DIR / "metadata_generator.ui"
STYLE_FILE = STYLES_DIR / "styles.qss"

# UI Sizes
@dataclass
class UISizes:
    # Buttons
    BUTTON_LARGE = QSize(180, 80)    # Main action buttons
    BUTTON_MEDIUM = QSize(100, 80)   # Secondary action buttons
    BUTTON_SMALL = QSize(80, 40)     # Navigation buttons
    BUTTON_TINY = QSize(60, 30)      # Utility buttons (plus, minus, etc.)
    BUTTON_WIDE = QSize(125, 40)     # Wide buttons (copyTag, clearTag)

    # Labels
    LABEL_STANDARD = QSize(180, 40)  # Standard labels
    LABEL_WIDE = QSize(200, 40)      # Wide labels

    # Combo Boxes
    COMBO_STANDARD = QSize(180, 40)  # Standard combo boxes
    COMBO_WIDE = QSize(200, 40)      # Wide combo boxes
    
    # Line Edits
    LINE_EDIT_HEIGHT = 60

    # Group Boxes
    GROUP_BOX_WIDTH = 150

# UI Alignments
@dataclass
class UIAlignments:
    CENTER = Qt.AlignCenter
    RIGHT_CENTER = Qt.AlignRight | Qt.AlignVCenter
    LEFT_CENTER = Qt.AlignLeft | Qt.AlignVCenter

# Regular Expressions
SERIAL_NAME_REGEX = r"^\d{8}-\d{4}\.tif$"

# File Format Templates
SERIAL_NAME_FORMAT = "{date}-{serial:04d}.tif"
DATE_FORMAT = "%Y%m%d"
DISPLAY_DATE_FORMAT = "%Y-%m-%d"

# Default Values
DEFAULTS = {
    "SERIAL": 0,
    "TAB_INDEX": 1,
    "LIGHT_INENSITY": "LV6",
    "EXPOSURE_TIME": "40",
    "FRAMES": "1200p",
    "FPS": "20Hz",
}

# Font Settings
@dataclass
class FontSettings:
    FAMILY = "Arial"
    SIZES = {
        "SMALL": 12,
        "NORMAL": 14,
        "LARGE": 16,
        "EXTRA_LARGE": 24
    }
    STYLES = {
        "NORMAL": "",
        "BOLD": "bold",
        "ITALIC": "italic",
        "BOLD_ITALIC": "bold italic"
    }

# Colors
@dataclass
class Colors:
    PURPLE = "#800080"
    RED = "#FF0000"
    GREEN = "#008000"
    GRAY = "#808080"
    BLUE = "#0000FF"
    
# Menu Options
@dataclass
class MenuOptions:
    # Excitation options
    EXCITATION = ["HLG", "LED_GREEN", "LED_BLUE"]
    
    # Emission filter options
    EMISSION = ["IR", "RED", "GREEN"]

    # Exposure time units
    EXPO_UNITS = ["ms", "us"]
    
    # Recording modes
    CAM_TRIG_MODES = ["EXT_EXP_START", "EXT_EXP_CTRL"]
    
    # Recording location types
    LOC_TYPES = ["SITE_", "CELL_"]