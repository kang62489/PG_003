# Modules
import os, sqlite3, glob, json
from pathlib import Path
import pandas as pd
from rich import print
from tabulate import tabulate
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtCore import Qt
from classes import (
    model_list_1,
    dialog_confirm,
    dialog_getPath
)
from util.constants import MODELS_DIR

class RecDBHandlers:
    def __init__(self, ui):
        self.ui = ui
        
        self.setup_DB()
        
        self.model_tablesOfRecDB = model_list_1.ListModel(name="model_tablesOfRecDB")
        self.ui.comboBox_tableOfRecDB.setModel(self.model_tablesOfRecDB)
        
        self.reload_menuList_tablesOfRecDB()
        self.connect_signals()
    
    def setup_DB(self):
        self.db = QSqlDatabase('QSQLITE')
        self.db.setDatabaseName(str((MODELS_DIR / "records.db").resolve()))
        self.db.open()
        
        self.model_recDB = QSqlTableModel(db=self.db)
        self.ui.tableView_recDB.setModel(self.model_recDB)
        self.sm_recDB = self.ui.tableView_recDB.selectionModel()
        
    def reload_menuList_tablesOfRecDB(self):
        conn = sqlite3.connect(str((MODELS_DIR / "records.db").resolve()))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        fetched = cursor.fetchall()
        conn.close()
        self.list_of_recDB_tables = sorted([item[0] for item in fetched])
        
        self.model_tablesOfRecDB.updateList(self.list_of_recDB_tables)
        self.model_tablesOfRecDB.layoutChanged.emit()
        
        with open(MODELS_DIR / "menuList_tables_of_RecDB.json", "w") as f:
            json.dump(self.list_of_recDB_tables, f, indent=4)
        
    def connect_signals(self):
        self.ui.btn_importRecDB.clicked.connect(self.import_recDB)
        self.ui.btn_loadRecDB.clicked.connect(self.loadRecDB)
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
    
    def generate_summary_dateFrame_of_metadata(self, list_of_metadata, rec_filenames, timestamps):
        result_of_scanning = pd.DataFrame()
        for pairs_of_metadata in list_of_metadata:
            dict_metadata = self.convert_pairs_to_dict(pairs_of_metadata)
            result_of_scanning = pd.concat([result_of_scanning, pd.DataFrame([dict_metadata])]).reset_index(drop=True)
        
        result_of_scanning.insert(0, "Filename", rec_filenames)
        result_of_scanning.insert(1, "Timestamp", timestamps)
        result_of_scanning.replace('None','', inplace=True)
        print(tabulate(result_of_scanning, headers="keys", tablefmt="pretty"))
        return result_of_scanning

    def import_recDB(self):
        dlg_get_inputDir = dialog_getPath.GetPath(title="Please select the folder contains .rec files")
        input_dir = dlg_get_inputDir.get_path()
        if input_dir == "":
            self.ui.textBrowser_recDB.setText("<span style='color: white;'>[MESSAGE] No directory is selected</span>")
            return
        else:
            self.ui.textBrowser_recDB.setText(f"<span style='color: lime;'>[INFO] Importing from {input_dir}</span>")
        
        # Check if the directory contains .rec files
        list_of_rec_paths = sorted(glob.glob(input_dir + '/*.rec'))
        if list_of_rec_paths == []:
            self.ui.textBroser_recDB.append("<span style='color: tomato;'>[ERROR] No .rec files are found in the selected directory</span>")
            return
        else:
            self.ui.textBrowser_recDB.append("<span style='color: lime;'>[INFO] .rec files are found, scanning...</span>")

        list_of_metadata, rec_filenames, timestamps = self.rec_content_scanner(list_of_rec_paths)
        df_summary = self.generate_summary_dateFrame_of_metadata(list_of_metadata, rec_filenames, timestamps)
        self.ui.textBrowser_recDB.append("<span style='color: lime;'>[INFO] Scanning completed! Summary generated!</span>")
        
        # Save to database
        conn = sqlite3.connect(str((MODELS_DIR / "records.db").resolve()))
        # Do not use only string numbers as table name!!
        table_name_to_be_written = "REC_" + df_summary['Filename'][0].split("-")[0]
        if table_name_to_be_written not in self.list_of_recDB_tables:
            df_summary.to_sql(table_name_to_be_written, conn, index=False)
            self.ui.textBrowser_recDB.append(f"<span style='color: lime;'>[INFO] New table '{table_name_to_be_written}' created in database!</span>")
            conn.close()
            self.reload_menuList_tablesOfRecDB()
            return
        
        self.ui.textBrowser_recDB.append(f"<span style='color: yellow;'>[Warning] Table '{table_name_to_be_written}' already exists in database, replacing...</span>")
        df_summary.to_sql(table_name_to_be_written, conn, if_exists="replace", index=False)
        self.ui.textBrowser_recDB.append("<span style='color: lime;'>[INFO] Summary successfully saved to database!</span>")
        conn.close()
        
    def loadRecDB(self):
        self.selected_table = self.ui.comboBox_tableOfRecDB.currentText()
        if self.selected_table == "":
            self.ui.textBrowser_recDB.append("<span style='color: tomato;'>[ERROR] No table is selected or the database has no table</span>")
            return
        self.model_recDB.setTable(self.selected_table)
        self.model_recDB.setSort(self.model_recDB.fieldIndex('Timestamp'), Qt.AscendingOrder)
        self.model_recDB.select()
        self.ui.textBrowser_recDB.append(f"<span style='color: lime;'>[INFO] Table '{self.selected_table}' loaded!</span>")

    def delete_table(self):
        self.selected_table = self.ui.comboBox_tableOfRecDB.currentText()
        if self.selected_table == "":
            self.ui.textBrowser_recDB.append("<span style='color: tomato;'>[ERROR] No table is selected or the database has no table</span>")
            return
        
        checkDeletion = dialog_confirm.Confirm(title="Warning...", msg="Delete selected table? This cannot be undone!")
        if not checkDeletion.exec():
            self.ui.textBrowser_recDB.append("<span style='color: white;'>[MESSAGE] Deletion Cancelled!</span>")
            return
        
        conn = sqlite3.connect(str((MODELS_DIR / "records.db").resolve()))
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {self.selected_table}")
        conn.commit()
        conn.close()
        
        self.ui.textBrowser_recDB.append(f"<span style='color: lime;'>[INFO] Table '{self.selected_table}' deleted from database!</span>")
        self.reload_menuList_tablesOfRecDB()
        self.clear_tableview_recDB()

    def clear_tableview_recDB(self):
        self.model_recDB.setTable("")
        self.model_recDB.select()
        
    def export_summary(self):
        selected_table = self.ui.comboBox_tableOfRecDB.currentText()
        if selected_table == "":
            self.ui.textBrowser_recDB.append("<span style='color: tomato;'>[ERROR] No table is selected or the database has no table</span>")
            return
        
        dlg_get_outputDir = dialog_getPath.GetPath(title="Select the output directory of the csv file of selected table!")
        output_dir = dlg_get_outputDir.get_path()
        if output_dir == "":
            self.ui.textBrowser_recDB.append("<span style='color: white;'>[MESSAGE] Export canceled</span>")
            return
        
        conn = sqlite3.connect(str((MODELS_DIR / "records.db").resolve()))
        df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
        conn.close()
        
        df.to_excel(os.path.join(output_dir, f"{selected_table}.xlsx"), index=False)
        self.ui.textBrowser_recDB.append(f"<span style='color: lime;'>[INFO] Table '{selected_table}' exported to {output_dir}</span>")
    
        pass