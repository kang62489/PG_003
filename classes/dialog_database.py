## Standard library imports
import os
import sqlite3
from datetime import datetime

## Third-party imports
import pandas as pd
from PySide6.QtCore import Qt
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
from classes import customized_delegate, dialog_confirm
from util.constants import MODELS_DIR, STYLE_FILE, UIAlignments, UISizes


class DatabaseViewer(QDialog):
    """A class of creating a database viewer for manaing the experiment information database"""

    def __init__(self, ui, handlers_EXP):
        super().__init__()
        self.ui = ui
        self.handlers_EXP = handlers_EXP

        self.setupUI()
        self.open_DB()
        self.connect_signals()
        self.show()

    def setupUI(self):
        self.setup_dialog()
        self.setup_tableView()
        self.setup_labels()
        self.setup_buttons()
        self.setup_layouts()

    def open_DB(self):
        self.db = QSqlDatabase("QSQLITE")
        self.db.setDatabaseName(str((MODELS_DIR / "exp_data.db").resolve()))
        self.db.open()

        # Create a model for BASIC_INFO table
        self.model_basic = QSqlTableModel(db=self.db)
        self.tableView_basic.setModel(self.model_basic)
        self.sm_basic = self.tableView_basic.selectionModel()
        self.selected_table = "BASIC_INFO"
        self.model_basic.setTable(self.selected_table)
        self.model_basic.setSort(self.model_basic.fieldIndex("DOR"), Qt.DescendingOrder)
        self.model_basic.select()

        # Create a model for INJECTION_HISTORY table
        self.model_injections = QSqlTableModel(db=self.db)
        self.model_injections.setTable("INJECTION_HISTORY")
        self.tableView_injections.setModel(self.model_injections)

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

        self.layout_btns.addWidget(self.btn_load_for_edit)
        self.layout_btns.addWidget(self.btn_delete)
        self.layout_btns.addWidget(self.btn_export_selected)
        self.layout_btns.addWidget(self.btn_export_databases)

        self.layout_main.addWidget(self.lbl_exp_list)
        self.layout_main.addWidget(self.tableView_basic)
        self.layout_main.addWidget(self.lbl_inj_history)
        self.layout_main.addWidget(self.tableView_injections)
        self.layout_main.addLayout(self.layout_btns)
        self.setLayout(self.layout_main)

    def setup_labels(self):
        self.lbl_exp_list = QLabel("Experiment List")
        self.lbl_inj_history = QLabel("Injection History")

    def setup_buttons(self):
        self.btn_load_for_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete Selected Rows")
        self.btn_delete.setStyleSheet("color: red;")
        self.btn_export_selected = QPushButton("Export Selected")
        self.btn_export_databases = QPushButton("Export Databases")

        buttons = [self.btn_load_for_edit, self.btn_delete, self.btn_export_selected, self.btn_export_databases]
        for btn in buttons:
            btn.setFixedHeight(UISizes.BUTTON_GENERAL_HEIGHT)

    def setup_tableView(self):
        self.tableView_basic = QTableView()
        self.tableView_basic.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_basic.horizontalHeader().setDefaultAlignment(UIAlignments.CENTER)
        self.tableView_basic.verticalHeader().setVisible(False)
        self.tableView_basic.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView_basic.setItemDelegate(customized_delegate.CenterAlignDelegate())
        self.tableView_basic.setFixedHeight(UISizes.DATABASE_VIEWER_HEIGHT * 0.5)

        self.tableView_injections = QTableView()
        self.tableView_injections.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_injections.horizontalHeader().setDefaultAlignment(UIAlignments.CENTER)
        self.tableView_injections.verticalHeader().setVisible(False)
        self.tableView_injections.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView_injections.setItemDelegate(customized_delegate.CenterAlignDelegate())
        self.tableView_injections.setFixedHeight(UISizes.DATABASE_VIEWER_HEIGHT * 0.3)

    def connect_signals(self):
        self.sm_basic.selectionChanged.connect(self.preview_inj)
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

    def delete(self):
        # Determine which table has focus - prioritize focus over selection
        if self.tableView_injections.hasFocus():
            model = self.model_injections
            table_name = "INJECTION_HISTORY"
            selected_indexes = self.tableView_injections.selectionModel().selectedIndexes()
            use_passcode = False
        elif self.tableView_basic.hasFocus():
            model = self.model_basic
            table_name = "BASIC_INFO"
            selected_indexes = self.sm_basic.selectedIndexes()
            use_passcode = True
        elif self.tableView_injections.selectionModel().hasSelection():
            model = self.model_injections
            table_name = "INJECTION_HISTORY"
            selected_indexes = self.tableView_injections.selectionModel().selectedIndexes()
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
            checkDeletion = dialog_confirm.ConfirmWithPasscode(
                title="⚠️ Delete Confirmation",
                msg=f"Delete selected rows from {table_name}?\nThis will also delete related injection history!\nThis action cannot be undone!",
                passcode="kang",
            )
        else:
            checkDeletion = dialog_confirm.Confirm(title="Checking...", msg=f"Delete selected rows from {table_name}?")

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
