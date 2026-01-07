## Modules
# Standard library imports
import sqlite3

# Third-party imports
import pendulum
from PySide6.QtCore import QObject
from PySide6.QtGui import QStandardItemModel
from rich import print

# Local application imports
from classes import DialogConfirm, DialogExpDb
from classes.dialog_inj_manager import DialogInjManager
from util.constants import MODELS_DIR


class CtrlExpInfo(QObject):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui

        self.auto_calculation()
        self.connect_signals()

        # Create a model for QTreeView (set model here so that it can be accessed by rm_injections)
        self.model_injections = QStandardItemModel()
        self.model_injections.setHorizontalHeaderLabels(["Injection History", "Description"])

    def connect_signals(self):
        self.ui.btn_addInjections.clicked.connect(self.add_injections)
        self.ui.btn_rmInjections.clicked.connect(self.rm_injections)
        self.ui.btn_openExpDb.clicked.connect(self.open_exp_db)
        self.ui.btn_saveToExpDb.clicked.connect(self.save_to_db)

        self.ui.de_dor.dateChanged.connect(self.auto_calculation)
        self.ui.de_dob.dateChanged.connect(self.auto_calculation)

    def auto_calculation(self):
        """Calculation of ages of and incubated weeks of the animals"""

        dor = pendulum.instance(self.ui.de_dor.date().toPython())
        dob = pendulum.instance(self.ui.de_dob.date().toPython())

        total_days = (dor - dob).days
        weeks = total_days // 7
        days = total_days % 7
        self.ages = f"{weeks}w{days}d"
        self.ui.le_ages.setText(self.ages)

        # Also send the input date to de_abfDate
        self.ui.de_abfDate.setDate(self.ui.de_dor.date())

    def add_injections(self):
        self.dlg_addTree = DialogInjManager(self.ui, self.model_injections)

    def rm_injections(self):
        """Remove selected injection(s) - finds root parents and removes entire tree"""

        # Get all selected indexes (Return [QModelIndex(row=..., column=...)])
        selected_indexes = self.ui.tree_injections.selectedIndexes()

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

    def open_exp_db(self):
        self.dlg_dbViewer = DialogExpDb(self.ui, self)

    def save_to_db(self):
        checkSaveToDB = DialogConfirm(title="Checking...", msg="Save current expinfo to database?")
        if not checkSaveToDB.exec():
            print("[bold yellow]Save Cancelled![/bold yellow]")
            return

        # get data from UIs (matching fields from load_to_tab0 and UI widgets)
        data_main = {
            "DOR": self.ui.de_dor.date().toPython().strftime("%Y_%m_%d"),
            "Project_Code": self.ui.le_project.text(),
            "ACUC_Protocol": self.ui.cb_acuc.currentText(),
            "CuttingOS": self.ui.le_cuttingOS.text(),
            "HoldingOS": self.ui.le_holdingOS.text(),
            "RecordingOS": self.ui.le_recordingOS.text(),
            "Animal_ID": self.ui.le_animalId.text(),
            "Genotype": self.ui.cb_genotype.currentText(),
            "Species": self.ui.cb_species.currentText(),
            "DOB": self.ui.de_dob.date().toPython().strftime("%Y_%m_%d"),
            "Ages": self.ui.le_ages.text(),
            "Sex": self.ui.cb_sex.currentText(),
        }

        conn = sqlite3.connect(MODELS_DIR / "exp_data.db")
        cursor = conn.cursor()
        table_name = "BASIC_INFO"  # Fixed table name since cb_EXP_DB_TABLE doesn't exist in UI

        # Check if record exists using DOR and Animal_ID as unique identifier
        check_query = f"SELECT rowid FROM {table_name} WHERE DOR = ? AND Animal_ID = ?"
        cursor.execute(check_query, (data_main["DOR"], data_main["Animal_ID"]))
        existing_record = cursor.fetchone()

        if existing_record:
            # Record exists - UPDATE
            record_id = existing_record[0]
            set_clause = ", ".join([f"{key} = ?" for key in data_main.keys()])
            values_to_update = tuple(data_main.values()) + (record_id,)
            sql_command = f"UPDATE {table_name} SET {set_clause} WHERE rowid = ?"
            cursor.execute(sql_command, values_to_update)
            print("[bold green]Basic info updated in database![/bold green]")
        else:
            # Record doesn't exist - INSERT
            columns_to_be_inserted = ", ".join(data_main.keys())
            placeholders_for_inserting_values = ", ".join(["?"] * len(data_main))
            values_to_be_inserted = tuple(data_main.values())
            sql_command = (
                f"INSERT INTO {table_name} ({columns_to_be_inserted}) VALUES ({placeholders_for_inserting_values})"
            )
            cursor.execute(sql_command, values_to_be_inserted)
            print("[bold green]Basic info saved to database![/bold green]")

        # ========== Save Injection History (Approach 1: DELETE + INSERT) ==========
        animal_id = data_main["Animal_ID"]

        # Step 1: Delete all existing injection records for this Animal_ID
        cursor.execute("DELETE FROM INJECTION_HISTORY WHERE Animal_ID = ?", (animal_id,))

        # Step 2: Insert all injections from the tree model
        injection_count = 0
        for row in range(self.model_injections.rowCount()):
            # Get parent items (DOI and Summary)
            parent_item = self.model_injections.item(row, 0)
            summary_item = self.model_injections.item(row, 1)

            if not parent_item or not summary_item:
                continue

            doi = parent_item.text()
            summary = summary_item.text()

            # Parse summary: "ST_Left_AAV9-ABC123 [Incubated 3w2d]"
            parts = summary.split("[")
            if len(parts) < 2:
                continue

            info_parts = parts[0].strip().split("_", 2)  # Split into mode, side, virus
            if len(info_parts) < 3:
                continue

            inj_mode = info_parts[0]
            side = info_parts[1]
            virus_short = info_parts[2]
            incubated = parts[1].replace("]", "").replace("Incubated", "").strip()

            # Extract child data
            virus_full = ""
            volume_per_shot = ""
            mix_ratio = ""
            num_of_sites = ""
            inj_coords = ""
            injectate_type = "SINGLE"  # Default

            for child_row in range(parent_item.rowCount()):
                label_item = parent_item.child(child_row, 0)
                value_item = parent_item.child(child_row, 1)

                if not label_item or not value_item:
                    continue

                label = label_item.text()
                value = value_item.text()

                if label == "Construction":
                    virus_full = value
                    # Detect if it's MIXED type (contains "+")
                    if "+" in value:
                        injectate_type = "MIXED"
                elif label == "Volume Per Shot":
                    volume_per_shot = value
                elif label == "Mixing Ratio":
                    mix_ratio = value
                elif label == "Number of Sites":
                    num_of_sites = value
                elif label == "Coordinates":
                    # Extract just the coordinates part: "[DV, ML, AP] = [-5.2, 1.5, -2.0]"
                    if "=" in value:
                        inj_coords = value.split("=")[1].strip()

            # Insert into INJECTION_HISTORY
            data_injection = {
                "Animal_ID": animal_id,
                "DOI": doi,
                "Inj_Mode": inj_mode,
                "Side": side,
                "Virus_Short": virus_short,
                "Incubated": incubated,
                "Virus_Full": virus_full,
                "Injectate_Type": injectate_type,
                "Mix_Ratio": mix_ratio,
                "Volume_Per_Shot": volume_per_shot,
                "Num_Of_Sites": num_of_sites,
                "Inj_Coords": inj_coords,
            }

            columns = ", ".join(data_injection.keys())
            placeholders = ", ".join(["?"] * len(data_injection))
            values = tuple(data_injection.values())

            cursor.execute(f"INSERT INTO INJECTION_HISTORY ({columns}) VALUES ({placeholders})", values)
            injection_count += 1

        if injection_count > 0:
            print(f"[bold green]Saved {injection_count} injection(s) to database![/bold green]")
        else:
            print("[bold yellow]No injection history to save[/bold yellow]")

        conn.commit()
        conn.close()
