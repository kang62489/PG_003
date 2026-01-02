## Standard library imports
import os
import sqlite3
from datetime import datetime

## Third-party imports
import pandas as pd
from PySide6.QtCore import QItemSelectionModel, Qt
from PySide6.QtGui import QColor, QStandardItem
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableView,
    QVBoxLayout,
)
from rich import print
from tabulate import tabulate

## Local application imports
from util.constants import MODELS_DIR, STYLE_FILE, UIAlignments, UISizes

from .delegate_custom import DelegateCenterAlign
from .dialog_confirm import DialogConfirm, DialogConfirmPasscode


class DialogExpDb(QDialog):
    """A class of creating a database viewer for manaing the experiment information database"""

    def __init__(self, ui, ctrl_exp_info):
        super().__init__()
        self.ui = ui
        self.ctrl_exp_info_ins = ctrl_exp_info
        self.tree_model = self.ctrl_exp_info_ins.model_injections

        self.setup_uis()
        self.open_db()
        self.connect_signals()
        self.show()

    def setup_uis(self):
        self.setup_dialog()
        self.setup_tableview()
        self.setup_labels()
        self.setup_buttons()
        self.setup_layouts()

    def open_db(self):
        self.db = QSqlDatabase("QSQLITE")
        self.db.setDatabaseName(str((MODELS_DIR / "exp_data.db").resolve()))
        self.db.open()

        # Create a model for BASIC_INFO table
        self.model_basic = QSqlTableModel(db=self.db)
        self.tv_basic.setModel(self.model_basic)
        self.sm_basic = self.tv_basic.selectionModel()
        self.selected_table = "BASIC_INFO"
        self.model_basic.setTable(self.selected_table)
        self.model_basic.setSort(self.model_basic.fieldIndex("DOR"), Qt.DescendingOrder)
        self.model_basic.select()

        # Create a model for INJECTION_HISTORY table
        self.model_injections = QSqlTableModel(db=self.db)
        self.model_injections.setTable("INJECTION_HISTORY")
        self.tv_injections.setModel(self.model_injections)

    def setup_dialog(self):
        self.setWindowTitle("Database Viewer")
        with open(STYLE_FILE, "r") as f:
            self.setStyleSheet(f.read())
        self.resize(UISizes.DATABASE_VIEWER_WIDTH, UISizes.DATABASE_VIEWER_HEIGHT)
        # self.setModal(True) # This will block the main window

        parent_geometry = self.ui.geometry()
        child_geometry = self.frameGeometry()
        # Calculate center position
        parent_center = parent_geometry.center()
        child_geometry.moveCenter(parent_center)

        # Move window to centered position
        self.move(child_geometry.topLeft())

    def setup_layouts(self):
        self.layout_main = QVBoxLayout()
        self.layout_btns = QHBoxLayout()

        self.layout_btns.addWidget(self.btn_LoadToTab0)
        self.layout_btns.addWidget(self.btn_delete)
        self.layout_btns.addWidget(self.btn_export_selected)
        self.layout_btns.addWidget(self.btn_export_databases)

        self.layout_main.addWidget(self.lbl_exp_list)
        self.layout_main.addWidget(self.tv_basic)
        self.layout_main.addWidget(self.lbl_inj_history)
        self.layout_main.addWidget(self.tv_injections)
        self.layout_main.addLayout(self.layout_btns)
        self.setLayout(self.layout_main)

    def setup_labels(self):
        self.lbl_exp_list = QLabel("Experiment List")
        self.lbl_inj_history = QLabel("Injection History")

    def setup_buttons(self):
        self.btn_LoadToTab0 = QPushButton("Edit in Main Window")
        self.btn_delete = QPushButton("Delete Selected Rows")
        self.btn_delete.setObjectName("btn_deleteFromDb")
        self.btn_export_selected = QPushButton("Export Selected")
        self.btn_export_databases = QPushButton("Export Databases")

        buttons = [self.btn_LoadToTab0, self.btn_delete, self.btn_export_selected, self.btn_export_databases]
        for btn in buttons:
            btn.setFixedHeight(UISizes.BUTTON_GENERAL_HEIGHT)

    def setup_tableview(self):
        self.tv_basic = QTableView()
        self.tv_basic.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tv_basic.horizontalHeader().setDefaultAlignment(UIAlignments.CENTER)
        self.tv_basic.verticalHeader().setVisible(False)
        self.tv_basic.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tv_basic.setItemDelegate(DelegateCenterAlign())
        self.tv_basic.setFixedHeight(UISizes.DATABASE_VIEWER_HEIGHT * 0.5)
        # Make selection more prominent
        self.tv_basic.setStyleSheet("""
            QTableView::item:selected {
                background-color: #4A90E2;
                color: white;
            }
        """)

        self.tv_injections = QTableView()
        self.tv_injections.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tv_injections.horizontalHeader().setDefaultAlignment(UIAlignments.CENTER)
        self.tv_injections.verticalHeader().setVisible(False)
        self.tv_injections.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tv_injections.setItemDelegate(DelegateCenterAlign())
        self.tv_injections.setFixedHeight(UISizes.DATABASE_VIEWER_HEIGHT * 0.3)
        # Make selection more prominent
        self.tv_injections.setStyleSheet("""
            QTableView::item:selected {
                background-color: #4A90E2;
                color: white;
            }
        """)

    def connect_signals(self):
        self.sm_basic.selectionChanged.connect(self.preview_inj)
        self.btn_LoadToTab0.clicked.connect(self.load_to_tab0)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_export_selected.clicked.connect(self.export_selected)
        self.btn_export_databases.clicked.connect(self.export_databases)

    def preview_inj(self):
        selected_indexes = self.sm_basic.selectedIndexes()
        if not selected_indexes:
            print("No row is selected")
            return

        # Get unique Animal_IDs from selected rows (column 1)
        animal_ids = list({self.model_basic.index(idx.row(), 1).data() for idx in selected_indexes})

        # Build filter
        ids_str = "', '".join(animal_ids)
        self.model_injections.setFilter(f"Animal_ID IN ('{ids_str}')")
        self.model_injections.select()

    def load_to_tab0(self):
        """Load the selected experiment to the main window for editing"""
        # Determine which table has focus - prioritize focus over selection
        if self.tv_injections.hasFocus():
            table_name = "INJECTION_HISTORY"
            selected_indexes = self.tv_injections.selectionModel().selectedIndexes()
        elif self.tv_basic.hasFocus():
            table_name = "BASIC_INFO"
            selected_indexes = self.sm_basic.selectedIndexes()
        elif self.tv_injections.selectionModel().hasSelection():
            table_name = "INJECTION_HISTORY"
            selected_indexes = self.tv_injections.selectionModel().selectedIndexes()
        elif self.sm_basic.hasSelection():
            table_name = "BASIC_INFO"
            selected_indexes = self.sm_basic.selectedIndexes()
        else:
            print("No row is selected")
            return

        if not selected_indexes:
            print("No row is selected")
            return

        # Get the LASTLY (most recently) selected row - the current index
        if table_name == "BASIC_INFO":
            last_row = self.sm_basic.currentIndex().row()
        else:  # INJECTION_HISTORY
            last_row = self.tv_injections.selectionModel().currentIndex().row()

        # Show only the row is selected lastly - clear other selections
        if table_name == "BASIC_INFO":
            # Bitwise OR combines flags is used for "model" selection, for select the entire row not just one cell
            # There is another way to do this: self.tv_basic.selectRow(last_row) from the perspective of view
            self.sm_basic.clearSelection()
            self.sm_basic.select(
                self.model_basic.index(last_row, 0), QItemSelectionModel.Select | QItemSelectionModel.Rows
            )
            animal_id = self.model_basic.index(last_row, 1).data()  # Column 1 of BASIC_INFO is Animal_ID
        else:  # INJECTION_HISTORY
            self.tv_injections.selectionModel().clearSelection()
            self.tv_injections.selectionModel().select(
                self.model_injections.index(last_row, 0),
                QItemSelectionModel.Select | QItemSelectionModel.Rows,
            )

            # Find the corresponding row in BASIC_INFO table
            animal_id = self.model_injections.index(last_row, 0).data()  # Column 0 of INJECTION_HISTORY is Animal_ID
            print(f"Animal_ID: {animal_id}")
            row_in_basic_info = self.model_basic.match(
                self.model_basic.index(0, 1), Qt.DisplayRole, animal_id, 1, Qt.MatchExactly
            )[0].row()
            self.tv_basic.selectRow(row_in_basic_info)

        # Filled in the main window based on selected tables
        conn = sqlite3.connect(MODELS_DIR / "exp_data.db")
        query_basic = """
                SELECT b.* FROM BASIC_INFO b
                WHERE b.Animal_ID = ?
            """

        query_injection = """
            SELECT i.* FROM INJECTION_HISTORY i
            WHERE i.Animal_ID = ?
        """
        df_basic_selected = pd.read_sql_query(query_basic, conn, params=(animal_id,))
        df_injection_selected = pd.read_sql_query(query_injection, conn, params=(animal_id,))
        conn.close()

        basic_columns = df_basic_selected.columns.to_list()
        injection_columns = df_injection_selected.columns.to_list()
        print("Properties in BASIC_INFO:", basic_columns)
        print("Properties in INJECTION_HISTORY:", injection_columns)

        self.ui.de_DOR.setDate(datetime.strptime(df_basic_selected["DOR"][0], "%Y_%m_%d"))
        self.ui.le_project.setText(df_basic_selected["Project_Code"][0])
        self.ui.cb_ACUC.setCurrentIndex(self.ui.cb_ACUC.findText(df_basic_selected["ACUC_Protocol"][0]))
        self.ui.le_cuttingOS.setText(df_basic_selected["CuttingOS"][0].astype(str))
        self.ui.le_holdingOS.setText(df_basic_selected["HoldingOS"][0].astype(str))
        self.ui.le_recordingOS.setText(df_basic_selected["RecordingOS"][0].astype(str))

        self.ui.le_AnimalID.setText(df_basic_selected["Animal_ID"][0])
        self.ui.cb_Genotype.setCurrentIndex(self.ui.cb_Genotype.findText(df_basic_selected["Genotype"][0]))
        self.ui.cb_Species.setCurrentIndex(self.ui.cb_Species.findText(df_basic_selected["Species"][0]))

        self.ui.de_DOB.setDate(datetime.strptime(df_basic_selected["DOB"][0], "%Y_%m_%d"))
        self.ui.le_ages.setText(df_basic_selected["Ages"][0])
        self.ui.cb_Sex.setCurrentIndex(self.ui.cb_Sex.findText(df_basic_selected["Sex"][0]))

        ## Injection History
        # Clear existing injection tree
        self.tree_model.removeRows(0, self.tree_model.rowCount())
        # ========== Gather Data ==========
        for i in range(df_injection_selected.shape[0]):
            inj_side = df_injection_selected["Side"][i]
            injectate_type = df_injection_selected["Injectate_Type"][i]

            mode_abbr = df_injection_selected["Inj_Mode"][i]

            # ========== Build Injectate Info ==========
            injectate_short = df_injection_selected["Virus_Short"][i]
            construction_full = df_injection_selected["Virus_Full"][i]

            # ========== Create Parent Row ==========
            incubation_text = df_injection_selected["Incubated"][i]

            item_DOI = QStandardItem(df_injection_selected["DOI"][i])
            item_DOI.setForeground(Qt.darkGreen)  # Green color for DOI

            item_summary = QStandardItem(f"{mode_abbr}_{inj_side}_{injectate_short} [{incubation_text}]")

            self.tree_model.appendRow([item_DOI, item_summary])
            parent = item_DOI

            # ========== Add Children (Conditionally) ==========
            child_row = 0

            # 1. Construction (shown in one row for both SINGLE and MIXED)
            label_construction = QStandardItem("Construction")
            label_construction.setForeground(QColor("#8A2BE2"))
            parent.setChild(child_row, 0, label_construction)
            parent.setChild(child_row, 1, QStandardItem(construction_full))
            child_row += 1

            # 2. Volume Per Shot (always shown)
            volume = df_injection_selected["Volume_Per_Shot"][i]
            label_volume = QStandardItem("Volume Per Shot")
            label_volume.setForeground(QColor("#8A2BE2"))
            parent.setChild(child_row, 0, label_volume)
            parent.setChild(child_row, 1, QStandardItem(volume))
            child_row += 1

            # 3. Mixing Ratio (only for MIXED)
            if injectate_type == "MIXED":
                ratio = df_injection_selected["Mix_Ratio"][i]

                label_ratio = QStandardItem("Mixing Ratio")
                label_ratio.setForeground(QColor("#8A2BE2"))
                parent.setChild(child_row, 0, label_ratio)
                parent.setChild(child_row, 1, QStandardItem(ratio))
                child_row += 1

            # 4. Coordinates (only for Stereotaxic, not Retro-orbital)
            if mode_abbr == "ST":
                # Get number of sites
                num_of_sites = df_injection_selected["Num_Of_Sites"][i]
                label_n_sites = QStandardItem("Number of Sites")
                label_n_sites.setForeground(QColor("#8A2BE2"))
                parent.setChild(child_row, 0, label_n_sites)
                parent.setChild(child_row, 1, QStandardItem(num_of_sites))
                child_row += 1

                # Get coordinates
                Inj_Coords = df_injection_selected["Inj_Coords"][i]
                coords = f"[DV, ML, AP] = {Inj_Coords}"
                label_coords = QStandardItem("Coordinates")
                label_coords.setForeground(QColor("#8A2BE2"))
                parent.setChild(child_row, 0, label_coords)
                parent.setChild(child_row, 1, QStandardItem(coords))
                child_row += 1

        # ========== Sort model by DOI (column 0, descending = newest first) ==========
        self.tree_model.sort(0, Qt.DescendingOrder)

        # ========== Update TreeView ==========
        self.ui.tree_injections.setModel(self.tree_model)
        self.close()

    def delete(self):
        # Determine which table has focus - prioritize focus over selection
        if self.tv_injections.hasFocus():
            model = self.model_injections
            table_name = "INJECTION_HISTORY"
            selected_indexes = self.tv_injections.selectionModel().selectedIndexes()
            use_passcode = False
        elif self.tv_basic.hasFocus():
            model = self.model_basic
            table_name = "BASIC_INFO"
            selected_indexes = self.sm_basic.selectedIndexes()
            use_passcode = True
        elif self.tv_injections.selectionModel().hasSelection():
            model = self.model_injections
            table_name = "INJECTION_HISTORY"
            selected_indexes = self.tv_injections.selectionModel().selectedIndexes()
            use_passcode = False
        elif self.sm_basic.hasSelection():
            model = self.model_basic
            table_name = "BASIC_INFO"
            selected_indexes = self.sm_basic.selectedIndexes()
            use_passcode = True
        else:
            print("No row is selected")
            return

        if not selected_indexes:
            print("No row is selected")
            return

        # Choose confirmation dialog based on table
        if use_passcode:
            checkDeletion = DialogConfirmPasscode(
                title="⚠️ Delete Confirmation",
                msg=f"Delete selected rows from {table_name}?\nThis will also delete related injection history!\nThis action cannot be undone!",
                passcode="kang",
            )
        else:
            checkDeletion = DialogConfirm(title="Checking...", msg=f"Delete selected rows from {table_name}?")

        if not checkDeletion.exec():
            print("Delete Cancelled!")
            return

        # For BASIC_INFO: manually delete related INJECTION_HISTORY first
        if table_name == "BASIC_INFO":
            # Get Animal_IDs to be deleted
            rows = sorted(set(index.row() for index in selected_indexes))
            animal_ids = [model.index(row, 1).data() for row in rows]  # Column 1 is Animal_ID

            # Delete related injection history first
            conn = sqlite3.connect(MODELS_DIR / "exp_data.db")
            cursor = conn.cursor()
            for animal_id in animal_ids:
                cursor.execute("DELETE FROM INJECTION_HISTORY WHERE Animal_ID = ?", (animal_id,))
                print(f"[yellow]Deleted injection history for Animal_ID: {animal_id}[/yellow]")
            conn.commit()
            conn.close()

            # Refresh injection model
            self.model_injections.select()

        # Now delete from the selected table
        rows_to_be_removed = sorted(set(index.row() for index in selected_indexes), reverse=True)
        for row in rows_to_be_removed:
            model.removeRows(row, 1)

        # Submit and save the changes to the sql table model
        if model.submitAll():
            print(f"[bold green]Data deleted from {table_name}![/bold green]")
        else:
            print(f"[bold red]Failed to delete data from {table_name}! The model is reverted![/bold red]")
            model.revertAll()

        # Refresh the view
        model.select()

    def export_selected(self):
        selected_indexes = self.sm_basic.selectedIndexes()
        dlg_get_outputDir = QFileDialog()
        dlg_get_outputDir.setWindowTitle("Select the output directory")
        dlg_get_outputDir.setFileMode(QFileDialog.FileMode.Directory)
        dlg_get_outputDir.setDirectory("")

        if not dlg_get_outputDir.exec():
            print("Export cancelled!")
            return

        dir_output = dlg_get_outputDir.selectedFiles()[0]

        if not selected_indexes:
            print("No row is selected")
            return

        # Get unique Animal_IDs from selected rows (column 1)
        animal_ids = list({self.model_basic.index(idx.row(), 1).data() for idx in selected_indexes})

        for animal_id in animal_ids:
            # connect to database for retrieving the data
            conn = sqlite3.connect(MODELS_DIR / "exp_data.db")
            query_basic = """
                SELECT b.* FROM BASIC_INFO b
                WHERE b.Animal_ID = ?
            """

            query_injection = """
                SELECT i.* FROM INJECTION_HISTORY i
                WHERE i.Animal_ID = ?
            """
            df_basic = pd.read_sql_query(query_basic, conn, params=(animal_id,))
            df_injection = pd.read_sql_query(query_injection, conn, params=(animal_id,))
            conn.close()

            with open(
                os.path.join(dir_output, df_basic["DOR"][0] + "_expInfo.md"),
                "w",
                encoding="utf-8",
            ) as f:
                f.write("# Experiment Information\n")
                f.write("Date of Recording: " + df_basic["DOR"][0] + "\n")
                f.write("Project Code: " + df_basic["Project_Code"][0] + "\n\n")

                f.write("# ACSF Solutions\n")
                f.write("Cutting Solution: " + df_basic["CuttingOS"][0].astype(str) + " mOsm/L" + "\n")
                f.write("Holding Solution: " + df_basic["HoldingOS"][0].astype(str) + " mOsm/L" + "\n")
                f.write("Recording Solution: " + df_basic["RecordingOS"][0].astype(str) + " mOsm/L" + "\n\n")

                f.write("# Animal Information\n")
                f.write("Animal ID: " + df_basic["Animal_ID"][0] + "\n")
                f.write("Date of Birth: " + df_basic["DOB"][0] + "\n")
                f.write("Ages: " + df_basic["Ages"][0] + "\n")
                f.write("Genotype: " + df_basic["Genotype"][0] + "\n")
                f.write("Species: " + df_basic["Species"][0] + "\n")
                f.write("Sex: " + df_basic["Sex"][0] + "\n")
                f.write("Protocol: " + df_basic["ACUC_Protocol"][0] + "\n\n")

                f.write("=" * 65 + "  Injection History  " + "=" * 65 + "\n\n\n")
                if df_injection.empty:
                    f.write("No injection history\n")
                else:
                    df_to_be_written_summary = df_injection.drop(
                        columns=[
                            "Animal_ID",
                            "Virus_Full",
                            "Injectate_Type",
                            "Mix_Ratio",
                            "Volume_Per_Shot",
                            "Num_Of_Sites",
                            "Inj_Coords",
                        ]
                    )
                    f.write(tabulate(df_to_be_written_summary, headers="keys", tablefmt="pretty"))

                    f.write("\n\n\n")
                    df_to_be_written_details = df_injection.drop(
                        columns=[
                            "Animal_ID",
                            "DOI",
                            "Inj_Mode",
                            "Side",
                            "Virus_Short",
                            "Incubated",
                        ]
                    )
                    f.write(tabulate(df_to_be_written_details, headers="keys", tablefmt="pretty"))

        print("File exported!")
        self.close()

    def export_databases(self):
        dlg_get_outputDir = QFileDialog()
        dlg_get_outputDir.setWindowTitle("Select the output directory")
        dlg_get_outputDir.setFileMode(QFileDialog.FileMode.Directory)
        dlg_get_outputDir.setDirectory("")

        if not dlg_get_outputDir.exec():
            print("Export cancelled!")
            return

        dir_output = dlg_get_outputDir.selectedFiles()[0]
        conn = sqlite3.connect(MODELS_DIR / "exp_data.db")
        df_basic = pd.read_sql_query("SELECT * FROM BASIC_INFO", conn)
        df_injection = pd.read_sql_query("SELECT * FROM INJECTION_HISTORY", conn)
        conn.close()

        df_basic.to_excel(
            os.path.join(dir_output, f"OUTPUT {datetime.now().strftime('%Y%m%d_%H%M%S')}_BASIC_INFO.xlsx"), index=False
        )
        df_injection.to_excel(
            os.path.join(dir_output, f"OUTPUT {datetime.now().strftime('%Y%m%d_%H%M%S')}_INJECTION_HISTORY.xlsx"),
            index=False,
        )
