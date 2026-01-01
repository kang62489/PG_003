## Modules
# Standard Library imports
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

# Third-party imports
from PySide6.QtCore import QSize, Qt

# Application Info
APP_NAME = "Expdata Manager"
APP_VERSION = "4.0"
APP_AUTHOR = "Kang"
APP_LAST_UPDATE = f"{datetime.now():%Y-%b-%d}"
APP_STATUS_MESSAGE = f"{APP_NAME} {APP_VERSION}, Author: {APP_AUTHOR}, Last Update: {APP_LAST_UPDATE}, Made in OIST"

# Directory Paths
BASE_DIR = Path(__file__).parent.parent
UI_DIR = BASE_DIR / "ui"
STYLES_DIR = BASE_DIR / "styles"
MODELS_DIR = BASE_DIR / "data"


# Load menu options from JSON files
def _load_json_menu(filename):
    """Helper to load JSON menu files"""
    with open(MODELS_DIR / filename, "r") as f:
        return json.load(f)


# Load general options set
_general_options = _load_json_menu("menuList_general_options_set.json")

# Greek symbol replacements for customized parameters
GREEK_REPLACEMENTS = _load_json_menu("greek_replacements.json")

# File Paths
UI_FILE = UI_DIR / "Expdata Manager.ui"
STYLE_FILE = STYLES_DIR / "styles.qss"


# UI Sizes
@dataclass
class UISizes:
    # Buttons
    BUTTON_LARGE = QSize(180, 80)  # Main action buttons
    BUTTON_MEDIUM = QSize(100, 80)  # Secondary action buttons
    BUTTON_SMALL = QSize(90, 40)  # Navigation buttons
    BUTTON_TEMPLATE = QSize(80, 30)  # Navigation buttons
    BUTTON_SN = QSize(50, 40)  # Utility buttons (plus, minus, etc.)
    BUTTON_WIDE = QSize(125, 40)  # Wide buttons (copyTag, clearTag)
    BUTTON_TINY_SQUARE = QSize(30, 30)
    BUTTON_LONG_HEIGHT = 50
    BUTTON_GENERAL_HEIGHT = 40
    BUTTON_ROWOP_HEIGHT = 30
    BUTTON_REFRESH = QSize(100, 30)

    # Labels
    LABEL_STANDARD = QSize(180, 40)  # Standard labels
    LABEL_WIDE = QSize(200, 40)  # Wide labels
    LABEL_INCUBATED_DISP = QSize(180, 40)  # Incubated label

    # Combo Boxes
    COMBO_STANDARD = QSize(180, 40)  # Standard combo boxes
    COMBO_WIDE = QSize(200, 40)  # Wide combo boxes
    COMBO_UNIT_WIDTH = 80
    COMBO_GENOTYPE_WIDTH = 100
    COMBO_INJECTATE_WIDTH = 180
    COMBO_RATIO_WIDTH = 180
    COMBO_VECTOR_WIDTH = 150
    COMBO_CLONE_WIDTH = 180
    COMBO_SIDE_WIDTH = 150
    COMBO_INJ_MODE_WIDTH = 250

    COMBO_TAB1_HEIGHT = 30

    # Line Edits
    LINE_EDIT_OS_WIDTH = 80
    LINE_EDIT_ID_WIDTH = 180
    LINE_EDIT_EXPO_WIDTH = 120
    LINE_EDIT_VOLUME_WIDTH = 150
    LINE_EDIT_COORDINATE_WIDTH = 100

    LINE_EDIT_EXPO_HEIGHT = 30
    LINE_EDIT_FPS_HEIGHT = 30
    LINE_EDIT_FSN_HEIGHT = 40

    # Group Boxes (adjusted for 600x800 window)
    GROUP_BOX_ROW1_HEIGHT = 80
    GROUP_BOX_ROW1_WIDTH = 560

    GROUP_BOX_ROW2_HEIGHT = 150
    GROUP_BOX_ROW2_WIDTH = 275

    GROUP_BOX_ROW3_HEIGHT = 150
    GROUP_BOX_ROW3_WIDTH = 560

    GROUP_BOX_WIDTH_LEFT_COLUMN = 275
    GROUP_BOX_WIDTH_RIGHT_COLUMN = 275
    GROUP_BOX_STATUS_HEIGHT = 150

    # Database Viewer
    DATABASE_VIEWER_WIDTH = 1200
    DATABASE_VIEWER_HEIGHT = 800

    # Progress Bar
    PROGRESSBAR_HEIGHT = 40

    # Checkbox
    CHECKBOX_LARGE = QSize(24, 24)

    # DateEdit
    DATE_EDIT_WIDTH = 250
    DATE_EDIT_DOB_WIDTH = 120

    # gb_animals widget widths
    GB_ANIMALS_COL3_WIDTH = 126  # cb_Species, cb_Sex, le_ages (~1/3 of gb_animals)

    # SpinBox
    SPIN_TAB1_HEIGHT = 30

    # TextEdit
    TEXT_EDIT_RECDIR_HEIGHT = 45

    # Stack Widget
    STACK_PARAMETERS_HEIGHT = 180

    # TableView
    TABLEVIEW_CUSTOMIZED_HEIGHT = 126


# UI Alignments
@dataclass
class UIAlignments:
    CENTER = Qt.AlignCenter
    RIGHT_CENTER = Qt.AlignRight | Qt.AlignVCenter
    LEFT_CENTER = Qt.AlignLeft | Qt.AlignVCenter
    TOP_CENTER = Qt.AlignTop | Qt.AlignHCenter


# Regular Expressions
SERIAL_NAME_REGEX = r"^\d{4}_\d{2}_\d{2}-\d{4}\.tif$"

# File Format Templates
SERIAL_NAME_FORMAT = "{date}-{serial:04d}.tif"
DATE_FORMAT = "%Y%m%d"
DISPLAY_DATE_FORMAT = "%Y_%m_%d"

# Default Values
DEFAULTS = {
    "SERIAL": 0,
    "TAB_INDEX": 0,
    "LIGHT_INTENSITY": "LV6",
    "EXPOSURE_TIME": "50",
    "FRAMES": "1200p",
    "FPS": "20Hz",
}


# Font Settings
@dataclass
class FontSettings:
    FAMILY = "Arial"
    SIZES = {"SMALL": 12, "NORMAL": 14, "LARGE": 16, "EXTRA_LARGE": 24}
    STYLES = {
        "NORMAL": "",
        "BOLD": "bold",
        "ITALIC": "italic",
        "BOLD_ITALIC": "bold italic",
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
    # Loaded from general options JSON
    # For EXP tab
    ACUC_PNS = _general_options["ACUC_PNS"]
    INJECTION_MODE = _general_options["INJECTION_MODE"]
    SIDE = _general_options["SIDE"]
    NUM_OF_SITES = _general_options["NUM_OF_SITES"]
    INJECTATE_TYPE = _general_options["INJECTATE_TYPE"]
    VECTOR_LIST = _general_options["VECTOR_LIST"]
    MIXING_RATIO = _general_options["MIXING_RATIO"]
    # For REC tab
    EXCITATION = _general_options["EXCITATION"]
    EMISSION = _general_options["EMISSION"]
    EXPO_UNITS = _general_options["EXPO_UNITS"]
    CAM_TRIG_MODES = _general_options["CAM_TRIG_MODES"]
    LOC_TYPES = _general_options["LOC_TYPES"]
    VOLUME_UNIT = _general_options["VOLUME_UNIT"]
    GENOTYPE = _general_options["GENOTYPE"]
    SEX = _general_options["SEX"]
    SPECIES = _general_options["SPECIES"]

    # MenuList files mapping (model_name: file_names)
    # MENU_LIST_FILES = {
    #     "model_menuList_ACUC": "menuList_ACUC.json",
    #     "model_menuList_virus_R": "menuList_virus_R.json",
    #     "model_menuList_virus_L": "menuList_virus_L.json",
    # }

    # Loaded from individual JSON files
    # VIRUSES_R = _load_json_menu("menuList_virus_R.json")
    # VIRUSES_L = _load_json_menu("menuList_virus_L.json")
    CUSTOM_TEMPLATES = _load_json_menu("menuList_templates.json")
    IMPORTED_DBS = _load_json_menu("menuList_tables_of_RecDB.json")
