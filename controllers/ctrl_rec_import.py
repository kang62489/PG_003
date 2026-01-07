## Modules
# Standard library imports
import glob
import json
import os
import sqlite3
from pathlib import Path

# Third-party imports
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from rich import print
from tabulate import tabulate

# Local application imports
from classes import DialogConfirm, DialogGetPath, ModelDynamicList
from util.constants import MODELS_DIR


class CtrlRecImport:
    def __init__(self, ui):
        self.ui = ui

        self.setup_db()

        self.model_tablesOfRecDB = ModelDynamicList(name="model_tablesOfRecDB")
        self.ui.cb_recDbTable.setModel(self.model_tablesOfRecDB)

        self.reload_rec_db_tables()
        self.connect_signals()

    def setup_db(self):
        self.db = QSqlDatabase("QSQLITE")
        self.db.setDatabaseName(str((MODELS_DIR / "rec_data.db").resolve()))
        self.db.open()

        self.model_recDB = QSqlTableModel(db=self.db)
        self.ui.tv_recDb.setModel(self.model_recDB)
        self.sm_recDB = self.ui.tv_recDb.selectionModel()

    def reload_rec_db_tables(self):
        conn = sqlite3.connect(str((MODELS_DIR / "rec_data.db").resolve()))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        fetched = cursor.fetchall()
        conn.close()
        self.list_of_recDB_tables = sorted([item[0] for item in fetched])

        self.model_tablesOfRecDB.update_list(self.list_of_recDB_tables)
        self.model_tablesOfRecDB.layoutChanged.emit()

        with open(MODELS_DIR / "menuList_tables_of_RecDB.json", "w") as f:
            json.dump(self.list_of_recDB_tables, f, indent=4)

    def connect_signals(self):
        self.ui.btn_importRecDb.clicked.connect(self.import_rec_db)
        self.ui.btn_loadRecTable.clicked.connect(self.load_rec_table)
        self.ui.btn_deleteTable.clicked.connect(self.delete_table)
        self.ui.btn_exportSummary.clicked.connect(self.export_summary)

    def rec_content_scanner(self, list_of_rec_paths):
        list_of_metadata = []
        list_of_original_content = []
        rec_filenames = []
        timestamps = []

        for rec_path in list_of_rec_paths:
            rec_filenames.append(Path(rec_path).stem)
            with open(rec_path, mode="r", encoding="utf-16-LE") as f:
                original_content = f.read().splitlines()
                list_of_original_content.append(original_content)

                for line_num, line_content in enumerate(original_content):
                    if "Time" in line_content:
                        timestamps.append(line_content.split(" ")[-1])

                    if "Comment:" in line_content:
                        extract_metadata_from = line_num + 2
                        break

                list_of_metadata.append(original_content[extract_metadata_from:])

        return list_of_metadata, rec_filenames, timestamps

    def convert_pairs_to_dict(self, list_of_pairs):
        dict_of_pairs = {}
        for item in list_of_pairs:
            # split at first ":"
            key, value = item.split(":", 1)
            dict_of_pairs[key.strip()] = value.strip()
        return dict_of_pairs

    def generate_metadata_summary(self, list_of_metadata, rec_filenames, timestamps):
        result_of_scanning = pd.DataFrame()
        for pairs_of_metadata in list_of_metadata:
            dict_metadata = self.convert_pairs_to_dict(pairs_of_metadata)
            result_of_scanning = pd.concat([result_of_scanning, pd.DataFrame([dict_metadata])]).reset_index(drop=True)

        result_of_scanning.insert(0, "Filename", rec_filenames)
        result_of_scanning.insert(1, "Timestamp", timestamps)
        result_of_scanning.replace("None", "", inplace=True)
        print(tabulate(result_of_scanning, headers="keys", tablefmt="pretty"))
        return result_of_scanning

    def import_rec_db(self):
        dlg_get_inputDir = DialogGetPath(title="Please select the folder contains .rec files")
        input_dir = dlg_get_inputDir.get_path()
        if input_dir == "":
            self.ui.tb_recDb.setText("<span style='color: white;'>[MESSAGE] No directory is selected</span>")
            return
        else:
            self.ui.tb_recDb.setText(f"<span style='color: lime;'>[INFO] Importing from {input_dir}</span>")

        # Check if the directory contains .rec files
        list_of_rec_paths = sorted(glob.glob(input_dir + "/*.rec"))
        if list_of_rec_paths == []:
            self.ui.textBroser_recDB.append(
                "<span style='color: tomato;'>[ERROR] No .rec files are found in the selected directory</span>"
            )
            return
        else:
            self.ui.tb_recDb.append("<span style='color: lime;'>[INFO] .rec files are found, scanning...</span>")
            self.ui.tb_recDb.moveCursor(QTextCursor.End)

        list_of_metadata, rec_filenames, timestamps = self.rec_content_scanner(list_of_rec_paths)
        df_summary = self.generate_metadata_summary(list_of_metadata, rec_filenames, timestamps)
        self.ui.tb_recDb.append("<span style='color: lime;'>[INFO] Scanning completed! Summary generated!</span>")
        self.ui.tb_recDb.moveCursor(QTextCursor.End)

        # Save to database
        conn = sqlite3.connect(str((MODELS_DIR / "rec_data.db").resolve()))
        # Do not use only string numbers as table name!!
        table_name_to_be_written = "REC_" + df_summary["Filename"][0].split("-")[0]
        if table_name_to_be_written not in self.list_of_recDB_tables:
            df_summary.to_sql(table_name_to_be_written, conn, index=False)
            self.ui.tb_recDb.append(
                f"<span style='color: lime;'>[INFO] New table '{table_name_to_be_written}' created in database!</span>"
            )
            self.ui.tb_recDb.moveCursor(QTextCursor.End)
            conn.close()
            self.reload_rec_db_tables()
            return

        self.ui.tb_recDb.append(
            f"<span style='color: yellow;'>[Warning] Table '{table_name_to_be_written}' already exists in database, replacing...</span>"
        )
        self.ui.tb_recDb.moveCursor(QTextCursor.End)
        df_summary.to_sql(table_name_to_be_written, conn, if_exists="replace", index=False)
        self.ui.tb_recDb.append("<span style='color: lime;'>[INFO] Summary successfully saved to database!</span>")
        self.ui.tb_recDb.moveCursor(QTextCursor.End)
        conn.close()

    def load_rec_table(self):
        self.selected_table = self.ui.cb_recDbTable.currentText()
        if self.selected_table == "":
            self.ui.tb_recDb.append(
                "<span style='color: tomato;'>[ERROR] No table is selected or the database has no table</span>"
            )
            self.ui.tb_recDb.moveCursor(QTextCursor.End)
            return
        self.model_recDB.setTable(self.selected_table)
        self.model_recDB.setSort(self.model_recDB.fieldIndex("Timestamp"), Qt.AscendingOrder)
        self.model_recDB.select()
        self.ui.tb_recDb.append(f"<span style='color: lime;'>[INFO] Table '{self.selected_table}' loaded!</span>")
        self.ui.tb_recDb.moveCursor(QTextCursor.End)

    def delete_table(self):
        self.selected_table = self.ui.cb_recDbTable.currentText()
        if self.selected_table == "":
            self.ui.tb_recDb.append(
                "<span style='color: tomato;'>[ERROR] No table is selected or the database has no table</span>"
            )
            self.ui.tb_recDb.moveCursor(QTextCursor.End)
            return

        checkDeletion = DialogConfirm(title="Warning...", msg="Delete selected table? This cannot be undone!")
        if not checkDeletion.exec():
            self.ui.tb_recDb.append("<span style='color: white;'>[MESSAGE] Deletion Cancelled!</span>")
            self.ui.tb_recDb.moveCursor(QTextCursor.End)
            return

        conn = sqlite3.connect(str((MODELS_DIR / "rec_data.db").resolve()))
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {self.selected_table}")
        conn.commit()
        conn.close()

        self.ui.tb_recDb.append(
            f"<span style='color: lime;'>[INFO] Table '{self.selected_table}' deleted from database!</span>"
        )
        self.ui.tb_recDb.moveCursor(QTextCursor.End)
        self.reload_rec_db_tables()
        self.clear_tv_rec_db()

    def clear_tv_rec_db(self):
        self.model_recDB.setTable("")
        self.model_recDB.select()

    def export_summary(self):
        selected_table = self.ui.cb_recDbTable.currentText()
        if selected_table == "":
            self.ui.tb_recDb.append(
                "<span style='color: tomato;'>[ERROR] No table is selected or the database has no table</span>"
            )
            self.ui.tb_recDb.moveCursor(QTextCursor.End)
            return

        dlg_get_outputDir = DialogGetPath(title="Select the output directory of the csv file of selected table!")
        output_dir = dlg_get_outputDir.get_path()
        if output_dir == "":
            self.ui.tb_recDb.append("<span style='color: white;'>[MESSAGE] Export canceled</span>")
            self.ui.tb_recDb.moveCursor(QTextCursor.End)
            return

        conn = sqlite3.connect(str((MODELS_DIR / "rec_data.db").resolve()))
        df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
        conn.close()

        df.to_excel(os.path.join(output_dir, f"{selected_table}.xlsx"), index=False)
        self.ui.tb_recDb.append(
            f"<span style='color: lime;'>[INFO] Table '{selected_table}' exported to {output_dir}</span>"
        )
        self.ui.tb_recDb.moveCursor(QTextCursor.End)

        pass
