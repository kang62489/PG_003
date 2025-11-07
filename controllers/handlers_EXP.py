## Modules
# Standard library imports
import sqlite3

# Third-party imports
import pendulum
from PySide6.QtCore import QObject
from rich import print

# Local application imports
from classes import dialog_addTree, dialog_confirm, dialog_database, model_list_1
from util.constants import MODELS_DIR, MenuOptions


class TAB_EXP_Handlers(QObject):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.model_menuList_ACUC = model_list_1.ListModel(name="model_menuList_ACUC")
        self.ui.comboBox_ACUC.setModel(self.model_menuList_ACUC)

        self.loadMenuLists()
        self.ui.comboBox_ACUC.setCurrentIndex(0)

        # install event filter for using ESC key to cancel editing
        self.ui.installEventFilter(self)

        self.auto_calculation()

        self.connect_signals()

    def connect_signals(self):
        self.ui.btn_add_vir_tree.clicked.connect(self.add_injections)
        self.ui.btn_openDB.clicked.connect(self.openDB)
        self.ui.btn_saveToDB.clicked.connect(self.save_to_DB)

        # self.ui.btn_add_ACUC_PN.clicked.connect(
        #     lambda: self.add_new_item_to_menu(
        #         self.ui.comboBox_ACUC, self.model_menuList_ACUC
        #     )
        # )
        # self.ui.btn_rm_ACUC_PN.clicked.connect(
        #     lambda: self.remove_item_from_menu(
        #         self.ui.comboBox_ACUC, self.model_menuList_ACUC
        #     )
        # )

        self.ui.dateEdit_DOR.dateChanged.connect(self.auto_calculation)
        self.ui.dateEdit_DOB.dateChanged.connect(self.auto_calculation)

    # def eventFilter(self, obj, event):
    #     """Event filter to handle ESC key to cancel editing in combobox, installed in __init__"""
    #     if event.type() == QEvent.KeyPress:
    #         focus_widget = QApplication.focusWidget()
    #         if event.key() == Qt.Key_Escape and isinstance(focus_widget, QComboBox):
    #             focus_widget.setEditable(False)
    #             return True  # Event handled
    #     return super().eventFilter(obj, event)

    # def add_new_item_to_menu(self, ui_combobox, model_combobox):
    #     ui_combobox.setEditable(True)
    #     ui_combobox.clearEditText()
    #     ui_combobox.setFocus()
    #     ui_combobox.lineEdit().returnPressed.disconnect()
    #     ui_combobox.lineEdit().returnPressed.connect(
    #         lambda: self.on_edit_done(ui_combobox, model_combobox)
    #     )

    # def update_menuList_JSON_files(self, model_combobox):
    #     for model_name, file_name in MenuOptions.MENU_LIST_FILES.items():
    #         if model_name == model_combobox.name:
    #             file_path = MODELS_DIR / file_name
    #             break
    #     with open(file_path, "w") as f:
    #         json.dump(model_combobox.list_of_options, f, indent=4)
    #     model_combobox.updateList(model_combobox.list_of_options)
    #     model_combobox.layoutChanged.emit()

    # def on_edit_done(self, ui_combobox, model_combobox):
    #     model_combobox.list_of_options.append(ui_combobox.currentText())
    #     self.update_menuList_JSON_files(model_combobox)
    #     ui_combobox.setEditable(False)
    #     ui_combobox.setCurrentIndex(ui_combobox.count() - 1)

    # def editing_finished(self, ui_combobox):
    #     ui_combobox.setEditable(False)

    # def remove_item_from_menu(self, ui_combobox, model_combobox):
    #     item_to_be_removed = ui_combobox.currentText()
    #     model_combobox.list_of_options.remove(item_to_be_removed)
    #     self.update_menuList_JSON_files(model_combobox)

    def loadMenuLists(self):
        self.model_menuList_ACUC.updateList(MenuOptions.ACUC_PNS)
        self.model_menuList_ACUC.layoutChanged.emit()

    def auto_calculation(self):
        """Calculation of ages of and incubated weeks of the animals"""

        dor = pendulum.instance(self.ui.dateEdit_DOR.date().toPython())
        dob = pendulum.instance(self.ui.dateEdit_DOB.date().toPython())

        duration = dor - dob
        self.ages = f"{duration.in_weeks()}w{duration.remaining_days}d"
        self.ui.lbl_ages.setText(self.ages)

    def add_injections(self):
        self.dlg_addTree = dialog_addTree.AddInjection(self.ui, self)

    def openDB(self):
        self.dlg_dbViewer = dialog_database.DatabaseViewer(self.ui, self)

    def save_to_DB(self):
        checkSaveToDB = dialog_confirm.Confirm(
            title="Checking...", msg="Save current expinfo to database?"
        )
        if not checkSaveToDB.exec():
            print("[bold yellow]Save Cancelled![/bold yellow]")
            return

        # get data from UIs
        data_main = {
            "DOR": self.ui.dateEdit_DOR.date().toPython().strftime("%Y_%m_%d"),
            "Experimenters": self.ui.lineEdit_experimenters.text(),
            "ACUC_Protocol": self.ui.comboBox_ACUC.currentText(),
            "Animal_ID": self.ui.lineEdit_animalID.text(),
            "Species": self.ui.comboBox_species.currentText(),
            "Genotype": self.ui.comboBox_genotype.currentText(),
            "Sex": self.ui.comboBox_sex.currentText(),
            "DOB": self.ui.dateEdit_DOB.date().toPython().strftime("%Y_%m_%d"),
            "Ages": self.ui.lbl_ages.text(),
            "CuttingOS": self.ui.lineEdit_CuttingOS.text(),
            "HoldingOS": self.ui.lineEdit_HoldingOS.text(),
            "RecordingOS": self.ui.lineEdit_RecordingOS.text(),
        }

        conn = sqlite3.connect(MODELS_DIR / "expInfo.db")
        cursor = conn.cursor()
        table_name = self.ui.comboBox_tableOfExpInfoDB.currentText()

        # Check if record exists using DOR and Animal_ID as unique identifier
        check_query = f"SELECT id FROM {table_name} WHERE DOR = ? AND Animal_ID = ?"
        cursor.execute(check_query, (data_main["DOR"], data_main["Animal_ID"]))
        existing_record = cursor.fetchone()

        if existing_record:
            # Record exists - UPDATE
            record_id = existing_record[0]
            set_clause = ", ".join([f"{key} = ?" for key in data_main.keys()])
            values_to_update = tuple(data_main.values()) + (record_id,)
            sql_command = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
            cursor.execute(sql_command, values_to_update)
            print("[bold green]Data updated in database![/bold green]")
        else:
            # Record doesn't exist - INSERT
            columns_to_be_inserted = ", ".join(data_main.keys())
            placeholders_for_inserting_values = ", ".join(["?"] * len(data_main))
            values_to_be_inserted = tuple(data_main.values())
            sql_command = f"INSERT INTO {table_name} ({columns_to_be_inserted}) VALUES ({placeholders_for_inserting_values})"
            cursor.execute(sql_command, values_to_be_inserted)
            print("[bold green]Data saved to database![/bold green]")

        conn.commit()
        conn.close()
