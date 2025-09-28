## Standard library imports
import os
import sqlite3
from datetime import datetime

## Third-party imports
import pandas as pd

## Local application imports
from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QPushButton,
    QTableView,
    QVBoxLayout,
)
from rich import print

from classes import customized_delegate, dialog_confirm
from util.constants import MODELS_DIR, STYLE_FILE, UIAlignments, UISizes


class DatabaseViewer(QDialog):
    """A class of creating a database viewer for manaing the experiment information database"""

    def __init__(self, ui, main):
        super().__init__()
        self.ui = ui
        self.main = main

        self.setupUI()
        self.setup_DB()
        self.connect_signals()
        self.show()

    def setupUI(self):
        self.setup_dialog()
        self.setup_tableView()
        self.setup_buttons()
        self.setup_layouts()

    def setup_DB(self):
        self.db = QSqlDatabase("QSQLITE")
        self.db.setDatabaseName(str((MODELS_DIR / "expInfo.db").resolve()))
        self.db.open()

        self.model_expInfoDB = QSqlTableModel(db=self.db)
        self.tableView_expInfoDB.setModel(self.model_expInfoDB)
        self.sm_expInfoDB = self.tableView_expInfoDB.selectionModel()
        self.selected_table = self.ui.comboBox_tableOfExpInfoDB.currentText()
        self.model_expInfoDB.setTable(self.selected_table)
        self.model_expInfoDB.setSort(
            self.model_expInfoDB.fieldIndex("DOR"), Qt.DescendingOrder
        )
        self.model_expInfoDB.select()

    def setup_dialog(self):
        self.setWindowTitle("Database Viewer")
        with open(STYLE_FILE, "r") as f:
            self.setStyleSheet(f.read())
        self.resize(UISizes.DATABASE_VIEWER_WIDTH, UISizes.DATABASE_VIEWER_HEIGHT)
        self.setModal(True)

    def setup_layouts(self):
        self.layout_main = QVBoxLayout()
        self.layout_btns = QHBoxLayout()

        self.layout_btns.addWidget(self.btn_load)
        self.layout_btns.addWidget(self.btn_delete)
        self.layout_btns.addWidget(self.btn_export)
        self.layout_main.addWidget(self.tableView_expInfoDB)
        self.layout_main.addLayout(self.layout_btns)
        self.setLayout(self.layout_main)

    def setup_buttons(self):
        self.btn_load = QPushButton("Load")
        self.btn_delete = QPushButton("Delete")
        self.btn_export = QPushButton("Export")

        buttons = [self.btn_load, self.btn_delete, self.btn_export]
        for btn in buttons:
            btn.setFixedSize(UISizes.BUTTON_SMALL)

    def setup_tableView(self):
        self.tableView_expInfoDB = QTableView()
        self.tableView_expInfoDB.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_expInfoDB.horizontalHeader().setDefaultAlignment(
            UIAlignments.CENTER
        )
        self.tableView_expInfoDB.verticalHeader().setVisible(False)
        self.tableView_expInfoDB.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self.tableView_expInfoDB.setItemDelegate(
            customized_delegate.CenterAlignDelegate()
        )

    def connect_signals(self):
        self.btn_load.clicked.connect(self.load)
        self.btn_delete.clicked.connect(self.delete)
        self.btn_export.clicked.connect(self.export)

    def load(self):
        selected_row = self.sm_expInfoDB.currentIndex().row()
        if not self.sm_expInfoDB.hasSelection():
            print("No row is selected")
            return
        primary_key = self.model_expInfoDB.index(selected_row, 0).data()

        # connect to database for retrieving the data
        conn = sqlite3.connect(str((MODELS_DIR / "expInfo.db").resolve()))
        df = pd.read_sql_query(
            f"SELECT * FROM {self.selected_table} WHERE id = {primary_key}", conn
        )
        conn.close()

        self.ui.dateEdit_DOR.setDate(datetime.strptime(df["DOR"][0], "%Y_%m_%d"))
        self.ui.lineEdit_experimenters.setText(df["Experimenters"][0])
        self.ui.comboBox_ACUC.setCurrentText(df["ACUC_Protocol"][0])
        self.ui.lineEdit_animalID.setText(df["Animal_ID"][0])
        self.ui.comboBox_species.setCurrentText(df["Species"][0])
        self.ui.comboBox_genotype.setCurrentText(df["Genotype"][0])
        self.ui.comboBox_sex.setCurrentText(df["Sex"][0])
        self.ui.dateEdit_DOB.setDate(datetime.strptime(df["DOB"][0], "%Y_%m_%d"))
        self.ui.dateEdit_DOI.setDate(datetime.strptime(df["DOI"][0], "%Y_%m_%d"))
        self.ui.lineEdit_CuttingOS.setText(df["CuttingOS"][0])
        self.ui.lineEdit_HoldingOS.setText(df["HoldingOS"][0])
        self.ui.lineEdit_RecordingOS.setText(df["RecordingOS"][0])

        if df["Enable_R"][0] == "True":
            self.ui.checkBox_ST_R.setCheckState(Qt.Checked)
            self.main.groupBox_R_available(Qt.Checked)
            self.ui.lineEdit_volume_R.setText(df["Inj_Volume_R"][0])
            self.ui.comboBox_volumeUnit_R.setCurrentText(df["Inj_Volume_Unit_R"][0])
            self.ui.comboBox_injectionMode_R.setCurrentText(df["Inj_Mode_R"][0])
            self.ui.lineEdit_Coord_DV_R.setText(df["Inj_Coord_DV_R"][0])
            self.ui.lineEdit_Coord_ML_R.setText(df["Inj_Coord_ML_R"][0])
            self.ui.lineEdit_Coord_AP_R.setText(df["Inj_Coord_AP_R"][0])
            self.ui.comboBox_virus_R.setCurrentText(df["Inj_virus_R"][0])
        else:
            self.ui.checkBox_ST_R.setCheckState(Qt.Unchecked)
            self.main.groupBox_R_available(Qt.Unchecked)

        if df["Enable_L"][0] == "True":
            self.ui.checkBox_ST_L.setCheckState(Qt.Checked)
            self.main.groupBox_L_available(Qt.Checked)
            self.ui.lineEdit_volume_L.setText(df["Inj_Volume_L"][0])
            self.ui.comboBox_volumeUnit_L.setCurrentText(df["Inj_Volume_Unit_L"][0])
            self.ui.comboBox_injectionMode_L.setCurrentText(df["Inj_Mode_L"][0])
            self.ui.lineEdit_Coord_DV_L.setText(df["Inj_Coord_DV_L"][0])
            self.ui.lineEdit_Coord_ML_L.setText(df["Inj_Coord_ML_L"][0])
            self.ui.lineEdit_Coord_AP_L.setText(df["Inj_Coord_AP_L"][0])
            self.ui.comboBox_virus_L.setCurrentText(df["Inj_virus_L"][0])
        else:
            self.ui.checkBox_ST_L.setCheckState(Qt.Unchecked)
            self.main.groupBox_L_available(Qt.Unchecked)

        print("Date loaded!")
        self.close()

    def delete(self):
        selected_indexes = self.sm_expInfoDB.selectedIndexes()
        if selected_indexes == []:
            print("No row is selected")
            return

        checkDeletion = dialog_confirm.Confirm(
            title="Checking...", msg="Delete selected rows?"
        )
        if not checkDeletion.exec():
            print("Delete Cancelled!")
            return

        rows_to_be_removed = sorted(
            set(index.row() for index in selected_indexes), reverse=True
        )
        for row in rows_to_be_removed:
            self.model_expInfoDB.removeRows(row, 1)

        # Submit and save the changes to the sql table model
        if self.model_expInfoDB.submitAll():
            print("[bold green]Data deleted from database![/bold green]")
        else:
            print(
                "[bold red]Failed to delete data from database! The model is reverted![/bold red]"
            )
            self.model_expInfoDB.revertAll()

        # Refresh the view
        self.model_expInfoDB.select()

    def export(self):
        selected_row = self.sm_expInfoDB.currentIndex().row()
        if not self.sm_expInfoDB.hasSelection():
            print("No row is selected")
            return

        primary_key = self.model_expInfoDB.index(selected_row, 0).data()

        # connect to database for retrieving the data
        conn = sqlite3.connect(str((MODELS_DIR / "expInfo.db").resolve()))
        df = pd.read_sql_query(
            f"SELECT * FROM {self.selected_table} WHERE id = {primary_key}", conn
        )
        conn.close()

        dlg_get_outputDir = QFileDialog()
        dlg_get_outputDir.setWindowTitle(
            "Select the output directory of the markdown file of selected expinfo!"
        )
        dlg_get_outputDir.setFileMode(QFileDialog.FileMode.Directory)
        dlg_get_outputDir.setDirectory("")

        if not dlg_get_outputDir.exec():
            print("Export cancelled!")
            return

        dir_output = dlg_get_outputDir.selectedFiles()[0]
        props = df.columns.tolist()
        values = df.values.tolist()[0]

        with open(
            os.path.join(dir_output, df["DOR"][0] + "_expInfo.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("---\n")
            for prop, value in zip(props, values):
                if prop in ["id", "Enable_R", "Enable_L"]:
                    continue
                elif value is None:
                    continue
                elif prop in ["Ages", "Incubation"]:
                    value = f"{value} weeks"
                elif prop == "Inj_Volume_R" or prop == "Inj_Volume_L":
                    unit_name = f"{prop}".replace("Volume", "Volume_Unit")
                    value = f"{value} {df[unit_name][0]}"
                elif prop == "Inj_Volume_Unit_R" or prop == "Inj_Volume_Unit_L":
                    continue

                f.write(f"{prop}: {value}")
                f.write("\n")
            f.write("---\n")
            print("File exported!")
        self.close()
