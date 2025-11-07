## Modules
# Standard library imports
from datetime import datetime

# Local application imports
from util.constants import MenuOptions, UISizes


class TAB_EXP_View:
    def __init__(self, ui):
        self.ui = ui
        self.setup_ui()

    def setup_ui(self):
        self.setup_groupboxes()
        self.setup_dateedit()
        self.setup_lineedits()
        # self.setup_pushbuttons()
        self.setup_comboboxes()

    def setup_groupboxes(self):
        self.ui.groupBox_fileIO.setFixedSize(
            UISizes.GROUP_BOX_ROW1_WIDTH, UISizes.GROUP_BOX_ROW1_HEIGHT
        )
        self.ui.groupBox_basics.setFixedSize(
            UISizes.GROUP_BOX_ROW2_WIDTH, UISizes.GROUP_BOX_ROW2_HEIGHT
        )
        self.ui.groupBox_solutions.setFixedSize(
            UISizes.GROUP_BOX_ROW2_WIDTH, UISizes.GROUP_BOX_ROW2_HEIGHT
        )
        self.ui.groupBox_animals.setFixedSize(
            UISizes.GROUP_BOX_ROW3_WIDTH, UISizes.GROUP_BOX_ROW3_HEIGHT
        )
        self.ui.groupBox_injections.setFixedWidth(UISizes.GROUP_BOX_ROW3_WIDTH)

    def setup_dateedit(self):
        dateEdits = [
            self.ui.dateEdit_DOR,
            self.ui.dateEdit_DOB,
        ]
        for dateEdit in dateEdits:
            dateEdit.setDate(datetime.today())
            dateEdit.setCalendarPopup(True)

    def setup_lineedits(self):
        self.ui.lineEdit_experimenters.setText("Kang")

        self.ui.lineEdit_cuttingOS.setFixedWidth(UISizes.LINE_EDIT_OS_WIDTH)
        self.ui.lineEdit_holdingOS.setFixedWidth(UISizes.LINE_EDIT_OS_WIDTH)
        self.ui.lineEdit_recordingOS.setFixedWidth(UISizes.LINE_EDIT_OS_WIDTH)

        self.ui.lineEdit_animalID.setFixedWidth(UISizes.LINE_EDIT_ID_WIDTH)

    # def setup_pushbuttons(self):
    #     tiny_buttons = [
    #         self.ui.btn_add_ACUC_PN,
    #         self.ui.btn_rm_ACUC_PN,
    #     ]

    #     for btn in tiny_buttons:
    #         btn.setFixedSize(UISizes.BUTTON_TINY_SQUARE)

    def setup_comboboxes(self):
        self.ui.comboBox_ACUC.addItems(MenuOptions.ACUC_PNS)
        self.ui.comboBox_species.addItems(MenuOptions.SPECIES)
        self.ui.comboBox_genotype.addItems(MenuOptions.GENOTYPE)
        self.ui.comboBox_sex.addItems(MenuOptions.SEX)
        self.ui.comboBox_tableOfExpInfoDB.addItems(MenuOptions.EXPINFO_DB_TABLES)

        self.ui.comboBox_genotype.setFixedWidth(UISizes.COMBO_GENOTYPE_WITDH)
