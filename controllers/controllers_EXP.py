## Modules
# Standard library imports
import sqlite3

# Third-party imports
import pendulum
from PySide6.QtCore import QObject
from PySide6.QtGui import QStandardItemModel
from rich import print

# Local application imports
from classes import add_injection_trees, dialog_confirm, dialog_database
from util.constants import MODELS_DIR


class TAB_EXP_Handlers(QObject):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

        self.auto_calculation()
        self.connect_signals()

        # Create a model for QTreeView (set model here so that it can be accessed by rm_injections)
        self.model_injections = QStandardItemModel()
        self.model_injections.setHorizontalHeaderLabels(["Injection History", "Description"])

    def connect_signals(self):
        self.ui.btn_add_vir_tree.clicked.connect(self.add_injections)
        self.ui.btn_rm_vir_tree.clicked.connect(self.rm_injections)
        self.ui.btn_openDB.clicked.connect(self.openDB)
        self.ui.btn_saveToDB.clicked.connect(self.save_to_DB)

        self.ui.dateEdit_DOR.dateChanged.connect(self.auto_calculation)
        self.ui.dateEdit_DOB.dateChanged.connect(self.auto_calculation)

    def auto_calculation(self):
        """Calculation of ages of and incubated weeks of the animals"""

        dor = pendulum.instance(self.ui.dateEdit_DOR.date().toPython())
        dob = pendulum.instance(self.ui.dateEdit_DOB.date().toPython())

        duration = dor - dob
        self.ages = f"{duration.in_weeks()}w{duration.remaining_days}d"
        self.ui.lbl_ages.setText(self.ages)

    def add_injections(self):
        self.dlg_addTree = add_injection_trees.ADD_INJECTION_TREES(self.ui, self.model_injections)

    def rm_injections(self):
        """Remove selected injection(s) - finds root parents and removes entire tree"""

        # Get all selected indexes (Return [QModelIndex(row=..., column=...)])
        selected_indexes = self.ui.treeView_injections.selectedIndexes()

        if not selected_indexes:
            print("[bold yellow]No injection selected![/bold yellow]")
            return

        # Find unique root parents
        # set here is a set {}, not set anything.
        root_rows_to_remove = set()  # Use set to avoid duplicates

        # The for loop is used to find the root parent of each selected index
        # (for the situation if I clicked on children terms but want to delete the related root parent)
        for index in selected_indexes:
            # Navigate up to find the root parent
            current_index = index
            while current_index.parent().isValid():
                current_index = current_index.parent()

            # Add root row number to the set
            root_rows_to_remove.add(current_index.row())

        # Convert to sorted list (descending order to remove from bottom up)
        # This prevents row index shifting issues
        root_rows = sorted(root_rows_to_remove, reverse=True)

        # Remove each root parent (and all its children)
        for row in root_rows:
            self.model_injections.removeRow(row)

        print(f"[bold green]Removed {len(root_rows)} injection(s)[/bold green]")

    def openDB(self):
        self.dlg_dbViewer = dialog_database.DatabaseViewer(self.ui, self)

    
    def save_to_DB(self):
        checkSaveToDB = dialog_confirm.Confirm(title="Checking...", msg="Save current expinfo to database?")
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

        conn = sqlite3.connect(MODELS_DIR / "exp_data.db")
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
            sql_command = (
                f"INSERT INTO {table_name} ({columns_to_be_inserted}) VALUES ({placeholders_for_inserting_values})"
            )
            cursor.execute(sql_command, values_to_be_inserted)
            print("[bold green]Data saved to database![/bold green]")

        conn.commit()
        conn.close()
