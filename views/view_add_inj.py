## Modules
# Standard library imports
from datetime import datetime

# Third-party imports
from PySide6.QtCore import Qt
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
    QWidget,
)

# Local application imports
from util.constants import MenuOptions, UIAlignments, UISizes


class ViewAddInj(QMainWindow):
    def __init__(self, clone_list, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Injection Info...")

        self.clone_list = clone_list
        self.setup_uis()
        self.show()

        # Center the window on parent after show() so geometry is calculated
        if parent:
            self.center_on_parent(parent)

    def center_on_parent(self, parent):
        """Center this window on the parent window"""
        # Ensure window size is calculated
        self.adjustSize()

        # Get geometries
        parent_geometry = parent.geometry()
        child_geometry = self.frameGeometry()

        # Calculate center position
        parent_center = parent_geometry.center()
        child_geometry.moveCenter(parent_center)

        # Move window to centered position
        self.move(child_geometry.topLeft())

    def setup_uis(self):
        self.setup_toolbar()
        self.setup_ui_containers()
        self.setup_layouts()
        self.setup_labels()
        self.setup_comboboxes()
        self.setup_lineedits()
        self.setup_dateedit()
        self.setup_buttons()
        self.setup_buttonbox()

    def setup_toolbar(self):
        # Add action toolbar for showing clone fullnames
        toolbar = QToolBar("Information")
        toolbar.toggleViewAction().setEnabled(False)
        self.addToolBar(toolbar)
        self.btn_cloneInfo = QAction("Clone Info", self)
        toolbar.addAction(self.btn_cloneInfo)

    def setup_layouts(self):
        self.layout_main = QHBoxLayout()
        self.layout_grid = QGridLayout()

        self.layout_main.addLayout(self.layout_grid)

        # Containers for putting clone list refrefresh button sets
        self.layout_grid.addWidget(self.container_1, 1, 5)
        self.layout_grid.addWidget(self.container_2, 3, 5)

        self.layout_container_1 = QHBoxLayout()
        self.layout_container_2 = QHBoxLayout()

        self.container_1.setLayout(self.layout_container_1)
        self.container_2.setLayout(self.layout_container_2)

        # Container for putting coordinates
        self.layout_grid.addWidget(self.container_3, 3, 1, UIAlignments.CENTER)
        self.layout_coordinates = QHBoxLayout()
        self.container_3.setLayout(self.layout_coordinates)

        # Container for QMainWindow
        widget = QWidget()
        widget.setLayout(self.layout_main)
        self.setCentralWidget(widget)

    def setup_labels(self):
        # Define labels: (attribute_name, display_text, column)
        labels = [
            ("lbl_inj_DOI", "Injection DOI", 0, 0),
            ("lbl_inj_mode", "Injection Mode", 0, 1),
            ("lbl_inj_side", "Side", 0, 2),
            ("lbl_injectate_type", "Injectate Type", 0, 3),
            ("lbl_vector_1", "Vector 1", 0, 4),
            ("lbl_clone_1", "Clone 1", 0, 5),
            ("lbl_incubated", "Incubated", 2, 0),
            ("lbl_coordinate", "Coordinates (Bregma as origin)", 2, 1),
            ("lbl_volume_per_shot", "Volume Per Shot", 2, 2),
            ("lbl_mixing_ratio", "Mixing Ratio", 2, 3),
            ("lbl_vector_2", "Vector 2", 2, 4),
            ("lbl_clone_2", "Clone 2", 2, 5),
            ("lbl_incubated_disp", "", 3, 0),
        ]

        for attr_name, text, row, col in labels:
            label = QLabel(text)
            setattr(self, attr_name, label)
            self.layout_grid.addWidget(label, row, col, UIAlignments.CENTER)

    def create_combobox(self, combobox_properties):
        for attr_name, items, _, _ in combobox_properties:
            combobox = QComboBox()
            combobox.setEditable(True)
            combobox.addItems(items)
            combobox.lineEdit().setAlignment(UIAlignments.CENTER)
            combobox.lineEdit().setReadOnly(True)
            setattr(self, attr_name, combobox)

    def setup_comboboxes(self):
        # Define comboboxes: (attribute_name, items, column)
        comboboxes = [
            ("cb_InjectionModeCtrl", MenuOptions.INJECTION_MODE, 1, 1),
            ("cb_inj_side", MenuOptions.SIDE, 1, 2),
            ("cb_InjectateTypeCtrl", MenuOptions.INJECTATE_TYPE, 1, 3),
            ("cb_vector_1", MenuOptions.VECTOR_LIST, 1, 4),
            ("cb_mixing_ratio", MenuOptions.MIXING_RATIO, 3, 3),
            ("cb_vector_2", MenuOptions.VECTOR_LIST, 3, 4),
        ]
        self.create_combobox(comboboxes)
        for attr_name, _, row, col in comboboxes:
            combobox = getattr(self, attr_name)
            self.layout_grid.addWidget(combobox, row, col, UIAlignments.CENTER)

        comboboxes_in_containers = [
            ("cb_clone_1", self.clone_list, 0, 0),
            ("cb_clone_2", self.clone_list, 0, 0),
            ("cb_num_of_sites", MenuOptions.NUM_OF_SITES, 0, 0),
        ]
        self.create_combobox(comboboxes_in_containers)
        self.layout_container_1.addWidget(self.cb_clone_1)
        self.layout_container_2.addWidget(self.cb_clone_2)
        self.layout_coordinates.addWidget(self.cb_num_of_sites)

        self.cb_InjectionModeCtrl.setFixedWidth(UISizes.COMBO_INJ_MODE_WIDTH)
        self.cb_inj_side.setFixedWidth(UISizes.COMBO_SIDE_WIDTH)
        self.cb_InjectateTypeCtrl.setFixedWidth(UISizes.COMBO_INJECTATE_WIDTH)
        self.cb_vector_1.setFixedWidth(UISizes.COMBO_VECTOR_WIDTH)
        self.cb_vector_2.setFixedWidth(UISizes.COMBO_VECTOR_WIDTH)

        self.cb_mixing_ratio.setFixedWidth(UISizes.COMBO_RATIO_WIDTH)
        self.cb_clone_1.setFixedWidth(UISizes.COMBO_CLONE_WIDTH)
        self.cb_clone_2.setFixedWidth(UISizes.COMBO_CLONE_WIDTH)

    def setup_dateedit(self):
        self.de_inj_DOI = QDateEdit()
        self.de_inj_DOI.setDate(datetime.today())
        self.de_inj_DOI.setCalendarPopup(True)

        self.layout_grid.addWidget(self.de_inj_DOI, 1, 0)
        self.de_inj_DOI.setFixedWidth(UISizes.DATE_EDIT_WIDTH)
        self.de_inj_DOI.setAlignment(UIAlignments.CENTER)

    def setup_ui_containers(self):
        # Container 1 & 2 for clone selection
        self.container_1 = QWidget()
        self.container_2 = QWidget()
        self.container_3 = QWidget()

    def setup_lineedits(self):
        self.le_DV = QLineEdit(placeholderText="DV(mm)")
        self.le_ML = QLineEdit(placeholderText="ML(mm)")
        self.le_AP = QLineEdit(placeholderText="AP(mm)")

        self.layout_coordinates.addWidget(self.le_DV)
        self.layout_coordinates.addWidget(self.le_ML)
        self.layout_coordinates.addWidget(self.le_AP)

        self.le_DV.setAlignment(UIAlignments.CENTER)
        self.le_ML.setAlignment(UIAlignments.CENTER)
        self.le_AP.setAlignment(UIAlignments.CENTER)

        self.le_DV.setFixedWidth(UISizes.LINE_EDIT_COORDINATE_WIDTH)
        self.le_ML.setFixedWidth(UISizes.LINE_EDIT_COORDINATE_WIDTH)
        self.le_AP.setFixedWidth(UISizes.LINE_EDIT_COORDINATE_WIDTH)

        self.le_volume_total = QLineEdit(placeholderText="Volume(unit)")
        self.layout_grid.addWidget(self.le_volume_total, 3, 2)

        self.le_volume_total.setAlignment(UIAlignments.CENTER)
        self.le_volume_total.setFixedWidth(UISizes.LINE_EDIT_VOLUME_WIDTH)

    def setup_buttons(self):
        self.btn_refresh_clone_1 = QPushButton("Refresh")
        self.btn_refresh_clone_2 = QPushButton("Refresh")

        self.layout_container_1.addWidget(self.btn_refresh_clone_1)
        self.layout_container_2.addWidget(self.btn_refresh_clone_2)

        self.btn_refresh_clone_1.setFixedSize(UISizes.BUTTON_REFRESH)
        self.btn_refresh_clone_2.setFixedSize(UISizes.BUTTON_REFRESH)

    def setup_buttonbox(self):
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.setOrientation(Qt.Vertical)  # Set vertical layout
        self.layout_main.addWidget(self.buttonBox, 0, UIAlignments.CENTER)
