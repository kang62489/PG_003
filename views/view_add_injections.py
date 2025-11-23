## Modules
# Standard library imports
import json
from datetime import datetime

# Third-party imports
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialogButtonBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

# Local application imports
from util.constants import MODELS_DIR, MenuOptions, UIAlignments


class ADD_INJECTION_VIEW(QMainWindow):
    def __init__(self, clone_list):
        super().__init__()
        self.setWindowTitle("Add Injection Info...")

        self.clone_list = clone_list
        self.setupUIs()
        self.show()

    def setupUIs(self):
        self.setup_toolbar()
        self.setup_layouts()
        self.setup_labels()
        self.setup_comboboxes()
        self.setup_ui_sets()
        self.setup_dateedit()
        self.setup_buttonBox()

    def setup_toolbar(self):
        # Add action toolbar for showing clone fullnames
        toolbar = QToolBar("Information")
        toolbar.toggleViewAction().setEnabled(False)
        self.addToolBar(toolbar)
        self.btn_cloneInfo = QAction("Clone Info", self)
        toolbar.addAction(self.btn_cloneInfo)

    def setup_layouts(self):
        self.layout_main = QVBoxLayout()
        self.layout_entries = QGridLayout()
        self.layout_main.addLayout(self.layout_entries)

        # Container for QMainWindow
        widget = QWidget()
        widget.setLayout(self.layout_main)
        self.setCentralWidget(widget)

    def setup_labels(self):
        # Define labels: (attribute_name, display_text, column)
        labels_first_row = [
            ("lbl_inj_DOI", "Injection DOI", 0),
            ("lbl_inj_mode", "Injection Mode", 1),
            ("lbl_inj_side", "Side", 2),
            ("lbl_injectate_type", "Injectate Type", 3),
            ("lbl_vector_1", "Vector 1", 4),
            ("lbl_clone_1", "Clone 1", 5),
            ("lbl_vector_2", "Vector 2", 6),
            ("lbl_clone_2", "Clone 2", 7),
        ]

        for attr_name, text, col in labels_first_row:
            label = QLabel(text)
            setattr(self, attr_name, label)
            self.layout_entries.addWidget(label, 0, col, UIAlignments.CENTER)

        labels_thrid_row = [
            ("lbl_incubated", "Incubated", 0),
            ("lbl_volume_total", "Total Volume", 1),
            ("lbl_mixing_ratio", "Mixing Ratio", 2),
            ("lbl_dilution", "Dilution", 3),
            ("lbl_coordinate", "Coordinates (Bregma as origin)", 4),
        ]

        for attr_name, text, col in labels_thrid_row:
            label = QLabel(text)
            setattr(self, attr_name, label)
            self.layout_entries.addWidget(label, 2, col, UIAlignments.CENTER)

        self.lbl_disp_incubated = QLabel("0")
        self.layout_entries.addWidget(self.lbl_disp_incubated, 3, 0, UIAlignments.CENTER)

    def create_combobox(self, combobox_properties):
        for attr_name, items in combobox_properties:
            combobox = QComboBox()
            combobox.setEditable(True)
            combobox.addItems(items)
            combobox.lineEdit().setAlignment(UIAlignments.CENTER)
            combobox.lineEdit().setReadOnly(True)
            setattr(self, attr_name, combobox)

    def setup_comboboxes(self):
        # Define comboboxes: (attribute_name, items, column)
        comboboxes_second_row = [
            ("comboBox_inj_mode", MenuOptions.INJECTION_MODE),
            ("comboBox_inj_side", MenuOptions.SIDE),
            ("comboBox_injectate_type", MenuOptions.INJECTATE_TYPE),
            ("comboBox_vector_1", MenuOptions.VECTOR_LIST),
            ("comboBox_vector_2", MenuOptions.VECTOR_LIST),
        ]

        comboboxes_third_row = [
            ("comboBox_mixing_ratio", MenuOptions.MIXING_RATIO),
            ("comboBox_dilution", MenuOptions.DILUTION),
        ]

        self.create_combobox(comboboxes_second_row)
        attr_names = [attr_name for attr_name, _ in comboboxes_second_row]
        col_order = [1, 2, 3, 4, 6]
        for attr_name, col in zip(attr_names, col_order):
            combobox = getattr(self, attr_name)
            self.layout_entries.addWidget(combobox, 1, col)

        self.create_combobox(comboboxes_third_row)
        attr_names = [attr_name for attr_name, _ in comboboxes_third_row]
        col_order = [2, 3]
        for attr_name, col in zip(attr_names, col_order):
            combobox = getattr(self, attr_name)
            self.layout_entries.addWidget(combobox, 3, col)

    def setup_dateedit(self):
        self.dateEdit_inj_DOI = QDateEdit()
        self.dateEdit_inj_DOI.setDate(datetime.today())
        self.layout_entries.addWidget(self.dateEdit_inj_DOI, 1, 0)

    def setup_ui_sets(self):
        # Container 1 & 2 for clone selection
        self.container_1 = QWidget()
        self.container_2 = QWidget()

        self.layout_entries.addWidget(self.container_1, 1, 5)
        self.layout_entries.addWidget(self.container_2, 1, 7)

        self.layout_container_1 = QHBoxLayout()
        self.layout_container_2 = QHBoxLayout()
        self.container_1.setLayout(self.layout_container_1)
        self.container_2.setLayout(self.layout_container_2)

        # comboboxes
        comboboxes_in_containers = [
            ("comboBox_clone_1", self.clone_list),
            ("comboBox_clone_2", self.clone_list),
        ]
        self.create_combobox(comboboxes_in_containers)

        # buttons
        self.btn_refresh_clone_1 = QPushButton("Refresh")
        self.layout_container_1.addWidget(self.comboBox_clone_1)
        self.layout_container_1.addWidget(self.btn_refresh_clone_1)

        self.btn_refresh_clone_2 = QPushButton("Refresh")
        self.layout_container_2.addWidget(self.comboBox_clone_2)
        self.layout_container_2.addWidget(self.btn_refresh_clone_2)

        self.lineEdit_volume_total = QLineEdit(placeholderText="Total Volume(unit)")
        self.lineEdit_volume_total.setAlignment(UIAlignments.CENTER)
        self.layout_entries.addWidget(self.lineEdit_volume_total, 3, 1)

        # Container 3 for coordinates
        self.container_3 = QWidget()
        self.layout_entries.addWidget(self.container_3, 3, 4)
        self.layout_coordinates = QHBoxLayout()
        self.container_3.setLayout(self.layout_coordinates)

        self.lineEdit_DV = QLineEdit(placeholderText="DV(mm)")
        self.lineEdit_DV.setAlignment(UIAlignments.CENTER)

        self.lineEdit_ML = QLineEdit(placeholderText="ML(mm)")
        self.lineEdit_ML.setAlignment(UIAlignments.CENTER)

        self.lineEdit_AP = QLineEdit(placeholderText="AP(mm)")
        self.lineEdit_AP.setAlignment(UIAlignments.CENTER)

        self.layout_coordinates.addWidget(self.lineEdit_DV)
        self.layout_coordinates.addWidget(self.lineEdit_ML)
        self.layout_coordinates.addWidget(self.lineEdit_AP)

    def setup_buttonBox(self):
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.layout_main.addWidget(self.buttonBox, 0, UIAlignments.CENTER)
