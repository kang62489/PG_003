## Standard library imports

## Third-party imports
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QGridLayout,
    QLabel,
    QPushButton,
)

## Local application imports
from util.constants import UISizes


class AddInjection(QDialog):
    """A class of creating a input panel for adding"""

    def __init__(self, ui, main):
        super().__init__()
        self.ui = ui
        self.main = main
        self.setWindowTitle("Add Injection Info...")

        self.setupUIs()
        # self.connect_signals()
        self.show()

    def setupUIs(self):
        # Main Layout
        self.layout_main = QGridLayout()

        # First Row
        self.lbl_inj_mode = QLabel("Injection Mode")
        self.lbl_inj_side = QLabel("Side")
        self.lbl_inj_DOI = QLabel("Injection DOI")
        self.lbl_vector_types = QLabel("Vector Types")

        self.layout_main.addWidget(self.lbl_inj_mode, 0, 0)
        self.layout_main.addWidget(self.lbl_inj_side, 0, 1)
        self.layout_main.addWidget(self.lbl_inj_DOI, 0, 2)
        self.layout_main.addWidget(self.lbl_vector_types, 0, 3)

        # Second Row
        self.comboBox_inj_mode = QComboBox()

        self.comboBox_inj_side = QComboBox()

        self.dateEdit_inj_DOI = QDateEdit()

        self.comboBox_vector_types = QComboBox()

        self.layout_main.addWidget(self.comboBox_inj_mode, 1, 0)
        self.layout_main.addWidget(self.comboBox_inj_side, 1, 1)
        self.layout_main.addWidget(self.dateEdit_inj_DOI, 1, 2)
        self.layout_main.addWidget(self.comboBox_vector_types, 1, 3)

        self.setLayout(self.layout_main)

    def setup_buttons(self):
        self.btn_load = QPushButton("Load")
        self.btn_delete = QPushButton("Delete")
        self.btn_export = QPushButton("Export")

        buttons = [self.btn_load, self.btn_delete, self.btn_export]
        for btn in buttons:
            btn.setFixedSize(UISizes.BUTTON_SMALL)

    # def setup_layouts(self):
    #     self.layout_btns = QHBoxLayout()

    #     self.layout_btns.addWidget(self.btn_load)
    #     self.layout_btns.addWidget(self.btn_delete)
    #     self.layout_btns.addWidget(self.btn_export)
    #     self.layout_main.addLayout(self.layout_btns)
    #     self.setLayout(self.layout_main)

    # def connect_signals(self):
    #     self.btn_delete.clicked.connect(self.delete)
    #     self.btn_export.clicked.connect(self.export)
