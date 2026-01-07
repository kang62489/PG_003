## Modules
# Standard library imports
import re
from datetime import datetime
from pathlib import Path

# Third-party imports
import pandas as pd
import pyabf
from PySide6.QtCore import QItemSelectionModel, Qt
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PySide6.QtWidgets import QLineEdit

# Local application imports
from classes import DialogConfirm, DirWatcher
from util.constants import MODELS_DIR


class CtrlAbfNote:
    def __init__(self, main_ui):
        self.ui = main_ui
        self.setup_db()

        # Set watcher for ABF files
        self.abf_watcher = DirWatcher(filetype=".abf", target_cb=self.ui.cb_currentAbf)
        self.watching_dir = self.ui.te_recDir.toPlainText()
        self.abf_watcher.set_watched_dir(self.watching_dir)

        # Initialize ABF attributes (will be updated when ABF file is detected)
        self.abf_protocol = ""
        self.abf_timestamp = ""

        self.connect_signals()

    def connect_signals(self):
        self.ui.de_abfDate.dateChanged.connect(self.filter_by_date)

        self.ui.btn_clearCellParams.clicked.connect(self.clear_cell_parameters)
        self.ui.btn_logCellParams.clicked.connect(self.log_cell_params)
        self.ui.btn_deleteSelected.clicked.connect(self.delete_selected)
        self.ui.btn_toggleCellParams.clicked.connect(self.toggle_cell_params)
        self.ui.btn_exportXlsx.clicked.connect(self.export_xlsx)
        self.ui.btn_logProtocol.clicked.connect(self.log_protocol)

        self.ui.tabs.currentChanged.connect(self.check_watching_dir)

        # the last step of watcher is set the current index to the last one, therefore this signal should use currentIndexChanged
        self.abf_watcher.filelistRenewed.connect(self.new_abf_detected)

    def clear_cell_parameters(self):
        line_edits_to_clear = self.ui.gb_cellParams.findChildren(QLineEdit)
        for line_edit in line_edits_to_clear:
            line_edit.clear()

    def setup_db(self):
        self.abf_db = QSqlDatabase("QSQLITE")
        self.abf_db.setDatabaseName(str((MODELS_DIR / "abf_note.db").resolve()))
        self.abf_db.open()

        # create table if not exists
        query = QSqlQuery(self.abf_db)
        query.exec("""
            CREATE TABLE IF NOT EXISTS ABF_NOTES (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                DOR TEXT NOT NULL,
                Timestamp TEXT,
                ABF_filename TEXT,
                Protocol TEXT,
                Slice TEXT,
                At TEXT,
                Rt TEXT,
                Rm TEXT,
                Cm TEXT,
                Ra TEXT,
                Tau TEXT,
                Hold TEXT
            )
        """)

        self.model_abfNote = QSqlTableModel(db=self.abf_db)
        self.model_abfNote.setTable("ABF_NOTES")
        self.model_abfNote.setSort(0, Qt.AscendingOrder)
        self.model_abfNote.select()
        self.ui.tv_abfNote.setModel(self.model_abfNote)
        self.ui.tv_abfNote.setColumnHidden(0, True)  # Hide the ID column

        # Initialize toggle button state
        self.ui.btn_toggleCellParams.setCheckable(True)
        self.ui.btn_toggleCellParams.setChecked(False)
        self.toggle_cell_params()  # Apply initial state

        self.sm_abfNote = self.ui.tv_abfNote.selectionModel()

    def filter_by_date(self):
        selected_date = self.ui.de_abfDate.date().toPython().strftime("%Y_%m_%d")
        self.model_abfNote.setFilter(f"DOR = '{selected_date}'")
        self.model_abfNote.select()

    def log_cell_params(self):
        # Get form data
        data = {
            "DOR": self.ui.de_abfDate.date().toPython().strftime("%Y_%m_%d"),
            "Timestamp": datetime.now().strftime("%H:%M:%S"),
            "Protocol": "manual_log",
            "Slice": str(self.ui.sb_abfSlice.value()) + self.ui.cb_abfSide.currentText(),
            "At": self.ui.cb_abfAtType.currentText() + str(self.ui.sb_abfAt.value()),
            "Rt": self.ui.le_abfRt.text(),
            "Rm": self.ui.le_abfRm.text(),
            "Cm": self.ui.le_abfCm.text(),
            "Ra": self.ui.le_abfRa.text(),
            "Tau": self.ui.le_abfTau.text(),
            "Hold": self.ui.le_abfHold.text(),
        }

        # Check if all param values are empty
        param_values = list(data.values())[5:11]
        if all(value == "" for value in param_values):
            return

        # Insert into database
        record = self.model_abfNote.record()
        for key, value in data.items():
            record.setValue(key, value)

        self.model_abfNote.insertRecord(-1, record)
        self.ui.le_abfProtocol.setText("manual_log")
        self.model_abfNote.select()  # Refresh view

    def delete_selected(self):
        dlg_confirm = DialogConfirm(title="Checking...", msg="Delete selected rows?")
        if not dlg_confirm.exec():
            return

        rows = self.sm_abfNote.selectedRows()
        for row in reversed(rows):
            self.model_abfNote.removeRow(row.row())
        self.model_abfNote.select()

    def toggle_cell_params(self):
        # Column indices for Rt, Rm, Cm, Ra, Tau, Hold
        param_columns = [7, 8, 9, 10, 11, 12]

        # Check if button is checked
        is_checked = self.ui.btn_toggleCellParams.isChecked()

        for col in param_columns:
            self.ui.tv_abfNote.setColumnHidden(col, not is_checked)

        # Update button text based on state
        self.ui.btn_toggleCellParams.setText("Hide Cell Params" if is_checked else "Show Cell Params")

    def export_xlsx(self):
        # Get current filter (date)
        selected_date = self.ui.de_abfDate.date().toPython().strftime("%Y_%m_%d")
        df_note_to_export = pd.read_sql_query(f"SELECT * FROM ABF_NOTES WHERE DOR = '{selected_date}'", self.abf_db)

        # Save to Excel
        filename = f"abf_notes_{self.ui.de_abfDate.date().toPython().strftime('%Y_%m_%d')}.xlsx"
        df_note_to_export.to_excel(filename, index=False)

    def check_watching_dir(self):
        if self.ui.tabs.currentIndex() != 2:
            return

        date_pattern = r"\d{4}_\d{2}_\d{2}"

        if self.watching_dir != self.ui.te_recDir.toPlainText():
            self.watching_dir = self.ui.te_recDir.toPlainText()
            self.abf_watcher.set_watched_dir(self.watching_dir)

            match = re.search(date_pattern, self.watching_dir)
            if match:
                self.ui.de_abfDate.setDate(datetime.strptime(match.group(), "%Y_%m_%d"))
                self.ui.de_abfDate.clearFocus()

    def new_abf_detected(self):
        current_abf = self.ui.cb_currentAbf.currentText()
        if current_abf.startswith("--"):
            return

        query = QSqlQuery(self.abf_db)
        is_record_exist = query.exec(
            f"SELECT * FROM ABF_NOTES WHERE ABF_filename = '{current_abf}' AND DOR = '{self.ui.de_abfDate.date().toPython().strftime('%Y_%m_%d')}'"
        )
        # if the current_abf file is already in the database, then return
        if is_record_exist and query.next():
            return

        abf_filepath = Path(self.watching_dir) / current_abf
        abf_info = pyabf.ABF(abf_filepath)
        self.abf_protocol = abf_info.protocol
        self.ui.le_abfProtocol.setText(self.abf_protocol)
        self.abf_timestamp = abf_info.abfDateTime.strftime("%H:%M:%S")

    def log_protocol(self):
        # Check if protocol field is empty (no ABF file detected yet)
        if self.ui.le_abfProtocol.text() == "":
            return

        current_abf = self.ui.cb_currentAbf.currentText()
        current_date = self.ui.de_abfDate.date().toPython().strftime("%Y_%m_%d")

        # Check if this ABF file already has a real protocol logged (not manual_log)
        query = QSqlQuery(self.abf_db)
        is_record_exist = query.exec(
            f"SELECT * FROM ABF_NOTES WHERE ABF_filename = '{current_abf}' AND DOR = '{current_date}' AND Protocol != 'manual_log'"
        )

        # If real protocol already logged, skip
        if is_record_exist and query.next():
            return

        # Log the protocol with ABF info
        data = {
            "DOR": current_date,
            "Timestamp": self.abf_timestamp,
            "ABF_filename": current_abf,
            "Protocol": self.abf_protocol,
            "Slice": str(self.ui.sb_abfSlice.value()) + self.ui.cb_abfSide.currentText(),
            "At": self.ui.cb_abfAtType.currentText() + str(self.ui.sb_abfAt.value()),
            "Rt": self.ui.le_abfRt.text(),
            "Rm": self.ui.le_abfRm.text(),
            "Cm": self.ui.le_abfCm.text(),
            "Ra": self.ui.le_abfRa.text(),
            "Tau": self.ui.le_abfTau.text(),
            "Hold": self.ui.le_abfHold.text(),
        }

        record = self.model_abfNote.record()
        for key, value in data.items():
            record.setValue(key, value)

        self.model_abfNote.insertRecord(-1, record)

        # Reset UI field to show actual protocol
        self.ui.le_abfProtocol.setText(self.abf_protocol)
        self.model_abfNote.select()
