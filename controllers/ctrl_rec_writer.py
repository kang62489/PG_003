import glob
import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from PySide6.QtCore import QItemSelectionModel, QModelIndex, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QTextCursor
from PySide6.QtWidgets import QApplication, QDialog
from rich import print

from classes import (
    DialogConfirm,
    DialogGetPath,
    DialogInsertProps,
    DialogSaveTemplate,
    ModelDynamicList,
    ModelMetadataForm,
)
from util.constants import DISPLAY_DATE_FORMAT, MODELS_DIR, SERIAL_NAME_REGEX


class CtrlRecWriter:
    def __init__(self, ui):
        self.ui = ui
        self.model_tv_customized = ModelMetadataForm()
        self.ui.tv_customized.setModel(self.model_tv_customized)
        self.sm_customized = self.ui.tv_customized.selectionModel()

        self.model_menuList_templates = ModelDynamicList()
        self.ui.cb_TemplateLoad.setModel(self.model_menuList_templates)

        # Set validtor for cheking filename-SN.tif
        regex = QRegularExpression(SERIAL_NAME_REGEX)
        self.validator = QRegularExpressionValidator(regex)
        self.dateStr = datetime.today().strftime(DISPLAY_DATE_FORMAT)

        self.recBackups = dict()

        self.connect_signals()
        self.update_tag_output()
        self.template_reload_list()
        self.template_load()

    def connect_signals(self):
        self.ui.radioBtnGroup_OBJ.buttonClicked.connect(self.update_tag_output)
        self.ui.cb_EXC.activated.connect(self.update_tag_output)
        self.ui.cb_EXC.currentIndexChanged.connect(self.auto_select_emi)
        self.ui.le_LEVEL.textChanged.connect(self.update_tag_output)
        self.ui.le_EXPO.textChanged.connect(self.update_tag_output)
        self.ui.cb_EXPO_UNIT.activated.connect(self.update_tag_output)
        self.ui.cb_EMI.activated.connect(self.update_tag_output)
        self.ui.le_FRAMES.textChanged.connect(self.update_tag_output)
        self.ui.le_FPS.textChanged.connect(self.update_tag_output)
        self.ui.sb_SLICE.valueChanged.connect(self.update_tag_output)
        self.ui.cb_CAM_TRIG_MODE.activated.connect(self.update_tag_output)
        self.ui.sb_SLICE.valueChanged.connect(self.update_tag_output)
        self.ui.cb_LOC_TYPE.activated.connect(self.update_tag_output)
        self.ui.sb_AT.valueChanged.connect(self.update_tag_output)
        self.ui.chk_addCustomized.stateChanged.connect(self.update_tag_output)

        # Emit signal to update tag output when the table in the QTableView (tv_customized) is changed
        self.model_tv_customized.dataChanged.connect(self.update_tag_output)
        self.model_tv_customized.layoutChanged.connect(self.update_tag_output)

        self.ui.cb_TemplateLoad.activated.connect(self.template_load)
        self.ui.btn_TemplateSave.clicked.connect(self.template_save)
        self.ui.btn_TemplateDelete.clicked.connect(self.template_delete)
        self.ui.btn_InsertCustomizedProperties.clicked.connect(self.insert_customized_properties)
        self.ui.btn_RmSelectedRows.clicked.connect(self.rm_selected_rows)
        self.ui.btn_MvRowsUp.clicked.connect(self.mv_rows_up)
        self.ui.btn_MvRowsDown.clicked.connect(self.mv_rows_down)

        self.ui.le_recDir.textChanged.connect(self.validate_rec_dir)
        self.ui.btn_BrowseRecDir.clicked.connect(self.browse_rec_dir)

        self.ui.le_filenameSN.textChanged.connect(self.sn_validate)

        self.ui.btn_SnInc.clicked.connect(self.sn_inc)
        self.ui.btn_SnDec.clicked.connect(self.sn_dec)
        self.ui.btn_SnReset.clicked.connect(self.sn_reset)
        self.ui.btn_SnCopy.clicked.connect(self.sn_copy)

        self.ui.btn_WriteRec.clicked.connect(self.write_rec)
        self.ui.btn_ReadRec.clicked.connect(self.read_rec)
        self.ui.btn_RevertRec.clicked.connect(self.revert_rec)

    def auto_select_emi(self):
        if self.ui.cb_EXC.currentText() == "HLG":
            self.ui.cb_EMI.setCurrentIndex(0)
        elif self.ui.cb_EXC.currentText() == "LED_GREEN":
            self.ui.cb_EMI.setCurrentIndex(1)
        elif self.ui.cb_EXC.currentText() == "LED_BLUE":
            self.ui.cb_EMI.setCurrentIndex(2)

    def update_tag_output(self):
        self.clear_tag_output()
        props = [
            "OBJ",
            "EXC",
            "LEVEL",
            "EXPO",
            "EMI",
            "FRAMES",
            "FPS",
            "CAM_TRIG_MODE",
            "SLICE",
            "AT",
        ]
        values = [
            self.ui.radioBtnGroup_OBJ.checkedButton().text(),
            self.ui.cb_EXC.currentText(),
            self.ui.le_LEVEL.text(),
            self.ui.le_EXPO.text() + self.ui.cb_EXPO_UNIT.currentText(),
            self.ui.cb_EMI.currentText(),
            self.ui.le_FRAMES.text(),
            self.ui.le_FPS.text(),
            self.ui.cb_CAM_TRIG_MODE.currentText(),
            self.ui.sb_SLICE.value(),
            self.ui.cb_LOC_TYPE.currentText() + str(self.ui.sb_AT.value()),
        ]

        if self.ui.chk_addCustomized.isChecked():
            for prop, val in zip(
                self.model_tv_customized._data.index.tolist(),
                self.model_tv_customized._data["VALUE_0"].tolist(),
            ):
                props.append(prop)
                values.append(val)

        for prop, val in zip(props, values):
            self.ui.te_tags.append(f"{prop}: {val}")

    def clear_tag_output(self):
        self.ui.te_tags.clear()

    def template_reload_list(self):
        templateFiles = [
            os.path.basename(i)
            for i in glob.glob(os.path.join(MODELS_DIR, "template_*.json"))
        ]
        templateList = [
            Path(tempName.replace("template_", "")).stem for tempName in templateFiles
        ]
        for file in templateList:
            if file == "patch_default":
                templateList.remove(file)
                templateList.insert(0, file)
            elif file == "puff_default":
                templateList.remove(file)
                templateList.insert(1, file)

        with open(MODELS_DIR / "menuList_templates.json", "w") as f:
            json.dump(templateList, f, indent=4)

        self.model_menuList_templates.update_list(templateList)
        self.model_menuList_templates.layoutChanged.emit()

    def template_load(self):
        filename = self.model_menuList_templates.list_of_options[
            self.ui.cb_TemplateLoad.currentIndex()
        ]
        self.ui.btn_TemplateDelete.setEnabled(False)

        if filename not in ["patch_default", "puff_default"]:
            self.ui.btn_TemplateDelete.setEnabled(True)

        with open(MODELS_DIR / "template_{}.json".format(filename), "r") as f:
            template = pd.read_json(f, dtype=str)
            self.model_tv_customized.update(template)
            self.model_tv_customized.layoutChanged.emit()

    def template_save(self):
        if self.model_tv_customized._data.empty:
            print("[bold red]Template doesn't exist![/bold red]")
            return

        self.saveCheck = DialogConfirm(
            title="Checking...", msg="Save current template?"
        )
        if not self.saveCheck.exec():
            print("[bold yellow]Save Cancelled![/bold yellow]")
            return

        self.saveDialog = DialogSaveTemplate()
        if not self.saveDialog.exec():
            print("[bold yellow]Save Cancelled![/bold yellow]")
            return

        self.saveDialog.savefile(
            os.path.join(MODELS_DIR), self.model_tv_customized._data
        )

        # reload the menu list
        self.template_reload_list()

        # set the QComboBox display the saved template
        for idx, item in enumerate(self.model_menuList_templates.list_of_options):
            if item == self.saveDialog.le_filename.text():
                self.ui.cb_TemplateLoad.setCurrentIndex(idx)
                self.template_load()
                break

    def template_delete(self):
        filename = self.model_menuList_templates.list_of_options[
            self.ui.cb_TemplateLoad.currentIndex()
        ]
        self.deleteCheck = DialogConfirm(
            title="Checking...", msg="Delete current template?"
        )

        if self.deleteCheck.exec():
            os.remove(os.path.join(MODELS_DIR, "template_{}.json".format(filename)))
            self.template_reload_list()
            self.clear_qtable_view(self.model_tv_customized)
            self.ui.btn_TemplateDelete.setEnabled(False)
        else:
            print("Delete Cancelled!")

    def clear_qtable_view(self, model):
        model.update(pd.DataFrame())
        model.layoutChanged.emit()

    def is_table_view_empty(self):
        return self.model_tv_customized._data.empty

    def insert_customized_properties(self):
        if self.is_table_view_empty():
            print("[bold red]Please load a template first![/bold red]")
            return

        if self.sm_customized.hasSelection():
            insert_from_this_row = self.sm_customized.currentIndex().row()
        else:
            insert_from_this_row = (
                self.model_tv_customized.rowCount(QModelIndex()) - 1
            )

        self.dlg_insertion = DialogInsertProps()
        if not self.dlg_insertion.exec() == QDialog.Accepted:
            print("Cancel Insertion!")
            return

        self.model_tv_customized.add_rows(
            QModelIndex(), insert_from_this_row, self.dlg_insertion.dataToBeAdded
        )
        new_index = self.model_tv_customized.index(
            insert_from_this_row + self.dlg_insertion.dataToBeAdded.shape[0],
            self.dlg_insertion.dataToBeAdded.shape[1] - 1,
        )
        self.sm_customized.setCurrentIndex(
            new_index, QItemSelectionModel.ClearAndSelect
        )

    def rm_selected_rows(self):
        selected_indexes = self.sm_customized.selectedIndexes()
        if selected_indexes == []:
            print("No row is selected")
            return

        rows_to_be_removed = sorted(
            set(index.row() for index in selected_indexes), reverse=True
        )
        for row in rows_to_be_removed:
            self.model_tv_customized.rm_rows(QModelIndex(), row, 1)

    def mv_rows_up(self):
        selected_indexes = self.sm_customized.selectedIndexes()
        if not selected_indexes:
            print("No row is selected")
            return

        # Get indices of selected rows
        rows = sorted(set(index.row() for index in selected_indexes))

        # Move rows up
        new_positions_of_moved_rows = self.model_tv_customized.mv_rows(rows, -1)
        # Reselect the moved rows
        self.sm_customized.clearSelection()
        for row in new_positions_of_moved_rows:
            index = self.model_tv_customized.index(row, 0)
            self.sm_customized.select(
                index, QItemSelectionModel.Select | QItemSelectionModel.Rows
            )

    def mv_rows_down(self):
        selected_indexes = self.sm_customized.selectedIndexes()
        if not selected_indexes:
            print("No row is selected")
            return

        # Get indices of selected rows
        rows = sorted(set(index.row() for index in selected_indexes))

        # Move rows down
        new_positions_of_moved_rows = self.model_tv_customized.mv_rows(rows, 1)
        # Reselect the moved rows
        self.sm_customized.clearSelection()
        for row in new_positions_of_moved_rows:
            index = self.model_tv_customized.index(row, 0)
            self.sm_customized.select(
                index, QItemSelectionModel.Select | QItemSelectionModel.Rows
            )

    def browse_rec_dir(self):
        self.dlg_requestRecDirectory = DialogGetPath()
        self.directory = self.dlg_requestRecDirectory.get_path()
        if self.directory == "":
            self.ui.le_recDir.setText("No selected directory")
        else:
            self.ui.le_recDir.setText(self.directory)

    def validate_rec_dir(self):
        self.directory = self.ui.le_recDir.text()
        prefix_text = self.ui.lbl_recDir.text()
        if not os.path.isdir(self.directory):
            dirCheckText = prefix_text + " (Invalid)"
            self.ui.lbl_recDir.setText(dirCheckText)
            self.ui.lbl_recDir.setStyleSheet("color: tomato;")
        else:
            direCheckText = prefix_text + " (Valid)"
            self.ui.lbl_recDir.setText(direCheckText)
            self.ui.lbl_recDir.setStyleSheet("color: green;")

    def sn_validate(self):
        self.ui.le_filenameSN.setValidator(self.validator)
        if self.ui.le_filenameSN.hasAcceptableInput():
            self.ui.le_filenameSN.setStyleSheet("QLineEdit { color: green; }")
            self.ui.btn_SnCopy.setEnabled(True)
            self.ui.le_filenameSN.setValidator(None)
        else:
            self.ui.le_filenameSN.setStyleSheet("QLineEdit { color: tomato; }")
            self.ui.btn_SnCopy.setEnabled(False)
            self.ui.le_filenameSN.setValidator(None)

    def sn_inc(self):
        self.dateStr = self.ui.le_filenameSN.text().split("-")[0]
        latest_value = self.ui.le_filenameSN.text().split("-")[1].split(".")[0]
        self.Serial = int(latest_value)
        if self.Serial < 9999:
            self.Serial += 1
            self.ui.le_filenameSN.setText(f"{self.dateStr}-{self.Serial:04d}.tif")
        elif self.Serial == 9999:
            self.Serial = 0
            self.ui.le_filenameSN.setText(f"{self.dateStr}-{self.Serial:04d}.tif")

    def sn_dec(self):
        self.dateStr = self.ui.le_filenameSN.text().split("-")[0]
        latest_value = self.ui.le_filenameSN.text().split("-")[1].split(".")[0]
        self.Serial = int(latest_value)
        if self.Serial > 0:
            self.Serial -= 1
            self.ui.le_filenameSN.setText(f"{self.dateStr}-{self.Serial:04d}.tif")
        elif self.Serial == 0:
            self.Serial = 0
            self.ui.le_filenameSN.setText(f"{self.dateStr}-{self.Serial:04d}.tif")

    def sn_reset(self):
        self.dateStr = self.ui.le_filenameSN.text().split("-")[0]
        self.Serial = 0
        self.ui.le_filenameSN.setText(f"{self.dateStr}-{self.Serial:04d}.tif")

    def sn_copy(self):
        QApplication.clipboard().setText(self.ui.le_filenameSN.text())

    def scan_rec_commments(self, rec_filepath):
        with open(rec_filepath, mode="r", encoding="utf-16-LE") as f:
            original_content = f.read().splitlines()
            write_from_line = 0
            keep_to_line = 0
            for line_num, line_content in enumerate(original_content):
                if "Comment:" in line_content:
                    keep_to_line = line_num + 1
                    write_from_line = line_num + 2
                    break

            tags = original_content[write_from_line:]
            preserved_content = original_content[:keep_to_line]
            preserved_content.append("")

        return tags, preserved_content, original_content

    def backup_rec_contents(
        self, rec_directory, rec_filename, contents_to_be_backupped
    ):
        # Backup before writing (can be recovered)
        if self.rec_filename in self.recBackups.keys():
            self.recBackups[rec_filename].append(contents_to_be_backupped)
        else:
            self.recBackups[rec_filename] = [contents_to_be_backupped]

        backup_path = os.path.join(rec_directory, "rec_backups.json")
        with open(backup_path, mode="w") as f:
            json.dump(self.recBackups, f, indent=4)
            self.ui.tb_status.append(
                "<span style='color: lime;'>[INFO] Backup saved!</span>"
            )
            self.ui.tb_status.moveCursor(QTextCursor.End)

    def write_rec(self):
        self.directory = self.ui.le_recDir.text()

        # Prepare filename and path
        self.rec_filename = self.ui.le_filenameSN.text().replace(
            ".tif", ".tif.rec"
        )
        self.rec_filepath = os.path.join(self.directory, self.rec_filename)

        # Check if file exists
        if not os.path.isfile(self.rec_filepath):
            self.ui.tb_status.setText(
                f"<span style='color: tomato;'>[ERROR] {self.rec_filename} is not found</span>"
            )
            return

        self.ui.tb_status.setText(
            f"<span style='color: lime;'>[INFO] {self.rec_filename} is found</span>"
        )

        # Confirm write operation
        dlg_checkWriteTags = DialogConfirm(
            title="Checking...", msg=f"Write tags to the {self.rec_filename}?"
        )

        if not dlg_checkWriteTags.exec():
            self.ui.tb_status.append(
                "<span style='color: white;'>[MESSAGE] Write Cancelled!</span>"
            )
            self.ui.tb_status.moveCursor(QTextCursor.End)
            return

        # Scan existing comments
        self.tags_read, self.preserved_content, self.original_content = (
            self.scan_rec_commments(self.rec_filepath)
        )
        self.tags_to_be_written = self.ui.te_tags.toPlainText().splitlines()

        # Handle case with existing tags
        if self.tags_read:
            dlg_checkOverwriteTags = DialogConfirm(
                title="Checking...", msg="Overwrite existing tags?"
            )

            if not dlg_checkOverwriteTags.exec():
                self.ui.tb_status.append(
                    "<span style='color: white;'>[MESSAGE] Overwrite Cancelled!</span>"
                )
                self.ui.tb_status.moveCursor(QTextCursor.End)
                return
            else:
                self.ui.tb_status.append(
                    "<span style='color: yellow;'>[WARNING] Overwrite Confirmed!</span>"
                )
                self.ui.tb_status.moveCursor(QTextCursor.End)

        # Backup before writing (can be recovered)
        self.backup_rec_contents(
            self.directory, self.rec_filename, self.original_content
        )

        # Write tags to file (either no existing tags or overwrite confirmed)
        contents_to_be_written = self.preserved_content + self.tags_to_be_written
        print("contents_to_be_written:", contents_to_be_written)
        with open(self.rec_filepath, mode="w", encoding="utf-16-LE") as f:
            f.write("\n".join(contents_to_be_written))
            self.ui.tb_status.append(
                f"<span style='color: lime;'>[INFO] Tags were written to {self.rec_filename}!</span>"
            )
            self.ui.tb_status.moveCursor(QTextCursor.End)

        self.sn_inc()

    def read_rec(self):
        self.directory = self.ui.le_recDir.text()
        self.rec_filename = self.ui.le_filenameSN.text().replace(
            ".tif", ".tif.rec"
        )
        self.rec_filepath = os.path.join(self.directory, self.rec_filename)

        if not os.path.isfile(self.rec_filepath):
            self.ui.tb_status.setText(
                f"<span style='color: tomato;'>[ERROR] {self.rec_filename} is not found</span>"
            )
            return
        else:
            self.ui.tb_status.setText(
                f"<span style='color: lime;'>[INFO] {self.rec_filename} is found</span>"
            )

        self.ui.tb_status.append(
            f"<span style='color: lime;'>[INFO] Tags were loaded from {self.rec_filename}!</span>"
        )
        self.ui.tb_status.moveCursor(QTextCursor.End)
        self.ui.te_tags.clear()
        self.tags_read, _, _ = self.scan_rec_commments(self.rec_filepath)
        self.ui.te_tags.setPlainText("\n".join(self.tags_read))

    def revert_rec(self):
        self.directory = self.ui.le_recDir.text()
        self.rec_filename = self.ui.le_filenameSN.text().replace(
            ".tif", ".tif.rec"
        )
        self.rec_filepath = os.path.join(self.directory, self.rec_filename)

        if not os.path.isfile(self.rec_filepath):
            self.ui.tb_status.setText(
                f"<span style='color: tomato;'>[ERROR] {self.rec_filename} is not found</span>"
            )
            return
        else:
            self.ui.tb_status.setText(
                f"<span style='color: lime;'>[INFO] {self.rec_filename} is found</span>"
            )

        recovery_filepath = os.path.join(self.directory, "rec_backups.json")
        if not os.path.isfile(recovery_filepath):
            self.ui.tb_status.append(
                "<span style='color: tomato;'>[ERROR] No backup file (JSON) is found!</span>"
            )
            self.ui.tb_status.moveCursor(QTextCursor.End)
            return
        else:
            with open(recovery_filepath, mode="r") as f:
                self.recBackups = json.load(f)
            self.ui.tb_status.append(
                "<span style='color: lime;'>[INFO] Backup JSON file is Loaded!</span>"
            )
            self.ui.tb_status.moveCursor(QTextCursor.End)

        dlg_checkRecover = DialogConfirm(
            title="Checking...",
            msg=f"Recover {self.rec_filename} to the original state?",
        )
        if not dlg_checkRecover.exec():
            self.ui.tb_status.append(
                "<span style='color: white;'>[MESSAGE] Recovery Cancelled!</span>"
            )
            self.ui.tb_status.moveCursor(QTextCursor.End)
            return
        else:
            self.ui.tb_status.append(
                "<span style='color: yellow;'>[WARNING] Recovery Confirmed!</span>"
            )
            self.ui.tb_status.moveCursor(QTextCursor.End)

        with open(self.rec_filepath, mode="w", encoding="utf-16-LE") as f:
            if self.rec_filename in self.recBackups.keys():
                f.write("\n".join(self.recBackups[self.rec_filename][0]))
                self.ui.tb_status.append(
                    f"<span style='color: lime;'>[INFO] {self.rec_filename} was recovered!</span>"
                )
                self.ui.tb_status.moveCursor(QTextCursor.End)
            else:
                self.ui.tb_status.append(
                    f"<span style='color: tomato;'>[ERROR] Recovery failed! {self.rec_filename} was not found in the backup!</span>"
                )
                self.ui.tb_status.moveCursor(QTextCursor.End)
