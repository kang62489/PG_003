import glob
import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from PySide6.QtCore import QFileSystemWatcher, QItemSelectionModel, QModelIndex, QRegularExpression, Qt
from PySide6.QtGui import QRegularExpressionValidator
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

## TODO:
# 1. [DONE] le_Level change to non-typing input (sb_LEVEL)
# 2. [DONE] le_Frames change to non-typing input (sb_FRAMES)
# 3. [DONE] remove CAM_TRIG_MODE
# 4. [DONE] Add "Side" (R, L) combobox for slice (cb_SIDE)
# 5. Make the filename of filename-serial number auto set to date of the folder
# 6. [DONE] Add Greek symbol auto-replace (via GREEK_REPLACEMENTS from constants)


class CtrlRecWriter:
    def __init__(self, ui):
        self.ui = ui
        self.model_tv_customized = ModelMetadataForm()
        self.ui.tv_customized.setModel(self.model_tv_customized)
        self.sm_customized = self.ui.tv_customized.selectionModel()

        self.model_menuList_templates = ModelDynamicList()
        self.ui.cb_TemplateLoad.setModel(self.model_menuList_templates)

        # Set validator for checking filename-SN.tif
        regex = QRegularExpression(SERIAL_NAME_REGEX)
        self.validator = QRegularExpressionValidator(regex)
        self.dateStr = datetime.today().strftime(DISPLAY_DATE_FORMAT)

        self.recBackups = dict()

        # Setup file system watcher for .rec files
        self.file_watcher = QFileSystemWatcher()

        self.connect_signals()
        self.template_reload_list()
        self.template_load()
        self.populate_rec_files()  # Check for .rec files on startup

    def connect_signals(self):
        # Toggle buttons for switching parameter pages
        self.ui.toggleBtnGroup.idClicked.connect(self.on_toggle_page)

        # Auto-select emission based on excitation
        self.ui.cb_EXC.currentIndexChanged.connect(self.auto_select_emi)

        # Template management
        self.ui.cb_TemplateLoad.activated.connect(self.template_load)
        self.ui.btn_TemplateSave.clicked.connect(self.template_save)
        self.ui.btn_TemplateDelete.clicked.connect(self.template_delete)
        self.ui.btn_InsertCustomProps.clicked.connect(self.insert_custom_props)
        self.ui.btn_RmSelectedRows.clicked.connect(self.rm_selected_rows)
        self.ui.btn_MvRowsUp.clicked.connect(self.mv_rows_up)
        self.ui.btn_MvRowsDown.clicked.connect(self.mv_rows_down)

        # File & Preview section
        self.ui.te_recDir.textChanged.connect(self.populate_rec_files)
        self.ui.btn_BrowseRecDir.clicked.connect(self.browse_rec_dir)
        self.ui.cb_recFiles.activated.connect(self.load_selected_rec_file)
        self.file_watcher.directoryChanged.connect(self.populate_rec_files)

        self.ui.le_filenameSN.textChanged.connect(self.sn_validate)

        self.ui.btn_SnInc.clicked.connect(self.sn_inc)
        self.ui.btn_SnDec.clicked.connect(self.sn_dec)
        self.ui.btn_SnReset.clicked.connect(self.sn_reset)
        self.ui.btn_SnCopy.clicked.connect(self.sn_copy)

        self.ui.btn_GenerateTags.clicked.connect(self.generate_tags_from_form)
        self.ui.btn_WriteRec.clicked.connect(self.write_rec)

    def auto_select_emi(self):
        if self.ui.cb_EXC.currentText() == "HLG":
            self.ui.cb_EMI.setCurrentIndex(0)
        elif self.ui.cb_EXC.currentText() == "LED_GREEN":
            self.ui.cb_EMI.setCurrentIndex(1)
        elif self.ui.cb_EXC.currentText() == "LED_BLUE":
            self.ui.cb_EMI.setCurrentIndex(2)

    def on_toggle_page(self, button_id):
        """Switch between Basic and Customized parameter pages"""
        self.ui.stack_parameters.setCurrentIndex(button_id)

    def generate_tags_from_form(self):
        """Generate tags from form and display in te_tags with blue color"""
        tags = self.build_tags_from_form()
        self.ui.te_tags.clear()
        self.ui.te_tags.setTextColor(Qt.red)
        self.ui.te_tags.setPlainText("\n".join(tags))

    def build_tags_from_form(self):
        """Build tags list from form widgets for writing to .rec file"""
        props = [
            "OBJ",
            "EXC",
            "LEVEL",
            "EXPO",
            "EMI",
            "FRAMES",
            "FPS",
            "SLICE",
            "AT",
        ]
        # Convert LEVEL value: 10 → "MAX", otherwise show number
        level_val = self.ui.sb_LEVEL.value()
        level_str = "MAX" if level_val == 10 else str(level_val)

        values = [
            self.ui.radioBtnGroup_OBJ.checkedButton().text(),
            self.ui.cb_EXC.currentText(),
            level_str,
            self.ui.le_EXPO.text() + self.ui.cb_EXPO_UNIT.currentText(),
            self.ui.cb_EMI.currentText(),
            str(self.ui.sb_FRAMES.value()),
            self.ui.le_FPS.text(),
            f"{self.ui.sb_SLICE.value()}{self.ui.cb_SIDE.currentText()}",
            self.ui.cb_LOC_TYPE.currentText() + str(self.ui.sb_AT.value()),
        ]

        if self.ui.chk_addCustomized.isChecked():
            for prop, val in zip(
                self.model_tv_customized._data.index.tolist(),
                self.model_tv_customized._data["VALUE_0"].tolist(),
            ):
                props.append(prop)
                values.append(val)

        return [f"{prop}: {val}" for prop, val in zip(props, values)]

    def template_reload_list(self):
        templateFiles = [os.path.basename(i) for i in glob.glob(os.path.join(MODELS_DIR, "template_*.json"))]
        templateList = [Path(tempName.replace("template_", "")).stem for tempName in templateFiles]
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
        filename = self.model_menuList_templates.list_of_options[self.ui.cb_TemplateLoad.currentIndex()]
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

        self.saveCheck = DialogConfirm(title="Checking...", msg="Save current template?")
        if not self.saveCheck.exec():
            print("[bold yellow]Save Cancelled![/bold yellow]")
            return

        self.saveDialog = DialogSaveTemplate()
        if not self.saveDialog.exec():
            print("[bold yellow]Save Cancelled![/bold yellow]")
            return

        self.saveDialog.savefile(os.path.join(MODELS_DIR), self.model_tv_customized._data)

        # reload the menu list
        self.template_reload_list()

        # set the QComboBox display the saved template
        for idx, item in enumerate(self.model_menuList_templates.list_of_options):
            if item == self.saveDialog.le_filename.text():
                self.ui.cb_TemplateLoad.setCurrentIndex(idx)
                self.template_load()
                break

    def template_delete(self):
        filename = self.model_menuList_templates.list_of_options[self.ui.cb_TemplateLoad.currentIndex()]
        self.deleteCheck = DialogConfirm(title="Checking...", msg="Delete current template?")

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

    def insert_custom_props(self):
        if self.is_table_view_empty():
            print("[bold red]Please load a template first![/bold red]")
            return

        if self.sm_customized.hasSelection():
            insert_from_this_row = self.sm_customized.currentIndex().row()
        else:
            insert_from_this_row = self.model_tv_customized.rowCount(QModelIndex()) - 1

        self.dlg_insertion = DialogInsertProps()
        if not self.dlg_insertion.exec() == QDialog.Accepted:
            print("Cancel Insertion!")
            return

        self.model_tv_customized.add_rows(QModelIndex(), insert_from_this_row, self.dlg_insertion.dataToBeAdded)
        new_index = self.model_tv_customized.index(
            insert_from_this_row + self.dlg_insertion.dataToBeAdded.shape[0],
            self.dlg_insertion.dataToBeAdded.shape[1] - 1,
        )
        self.sm_customized.setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)

    def rm_selected_rows(self):
        selected_indexes = self.sm_customized.selectedIndexes()
        if selected_indexes == []:
            print("No row is selected")
            return

        rows_to_be_removed = sorted(set(index.row() for index in selected_indexes), reverse=True)
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
            self.sm_customized.select(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

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
            self.sm_customized.select(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

    def browse_rec_dir(self):
        self.dlg_requestRecDirectory = DialogGetPath()
        self.directory = self.dlg_requestRecDirectory.get_path()
        # Only update if user selected a directory (not cancelled)
        if self.directory:
            self.ui.te_recDir.setText(self.directory)

    def populate_rec_files(self):
        """Populate the .rec file combobox with files from the current directory"""
        self.directory = self.ui.te_recDir.toPlainText()

        # Remember current selection and file list before clearing
        current_selection = self.ui.cb_recFiles.currentText()
        old_files = set(
            self.ui.cb_recFiles.itemText(i)
            for i in range(self.ui.cb_recFiles.count())
            if not self.ui.cb_recFiles.itemText(i).startswith("--")
        )

        # Remove old directory from watcher if any
        watched_dirs = self.file_watcher.directories()
        if watched_dirs:
            self.file_watcher.removePaths(watched_dirs)

        # Clear existing items
        self.ui.cb_recFiles.clear()
        self.ui.te_tags.clear()

        if not os.path.isdir(self.directory):
            self.ui.cb_recFiles.addItem("-- No RECs in current dir --")
            return

        # Add directory to watcher
        self.file_watcher.addPath(self.directory)

        # Find all .rec files
        rec_files = sorted(glob.glob(os.path.join(self.directory, "*.tif.rec")))
        rec_filenames = [os.path.basename(f) for f in rec_files]

        if not rec_filenames:
            self.ui.cb_recFiles.addItem("-- No RECs in current dir --")
        else:
            self.ui.cb_recFiles.addItems(rec_filenames)

            # Check for new files
            new_files = set(rec_filenames) - old_files

            if new_files:
                # Select the newest added file (last one alphabetically among new files)
                newest_file = sorted(new_files)[-1]
                index = self.ui.cb_recFiles.findText(newest_file)
                self.ui.cb_recFiles.setCurrentIndex(index)
            elif current_selection and not current_selection.startswith("--"):
                # Restore previous selection if it still exists
                index = self.ui.cb_recFiles.findText(current_selection)
                if index >= 0:
                    self.ui.cb_recFiles.setCurrentIndex(index)
                else:
                    self.ui.cb_recFiles.setCurrentIndex(len(rec_filenames) - 1)
            else:
                # Default to last file
                self.ui.cb_recFiles.setCurrentIndex(len(rec_filenames) - 1)

            self.load_selected_rec_file()

    def load_selected_rec_file(self):
        """Load the selected .rec file content into the preview"""
        self.directory = self.ui.te_recDir.toPlainText()
        selected_file = self.ui.cb_recFiles.currentText()

        # Skip if placeholder text
        if selected_file.startswith("--"):
            self.ui.te_tags.clear()
            return

        rec_filepath = os.path.join(self.directory, selected_file)

        if not os.path.isfile(rec_filepath):
            self.ui.te_tags.clear()
            self.ui.te_tags.setPlainText("File not found")
            return

        # Load and display the file content with black color (from file)
        tags_read, _, _ = self.scan_rec_commments(rec_filepath)
        self.ui.te_tags.clear()
        self.ui.te_tags.setTextColor(Qt.blue)
        if tags_read:
            self.ui.te_tags.setPlainText("\n".join(tags_read))
        else:
            self.ui.te_tags.setPlainText("(No tags written yet)")

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

    def backup_rec_contents(self, rec_directory, rec_filename, contents_to_be_backupped):
        # Backup before writing (can be recovered)
        if self.rec_filename in self.recBackups.keys():
            self.recBackups[rec_filename].append(contents_to_be_backupped)
        else:
            self.recBackups[rec_filename] = [contents_to_be_backupped]

        backup_path = os.path.join(rec_directory, "rec_backups.json")
        with open(backup_path, mode="w") as f:
            json.dump(self.recBackups, f, indent=4)
            print("[bold green][INFO] Backup saved![/bold green]")

    def write_rec(self):
        self.directory = self.ui.te_recDir.toPlainText()

        # Get selected file from combobox
        selected_file = self.ui.cb_recFiles.currentText()

        # Skip if placeholder text
        if selected_file.startswith("--"):
            print("[bold red][ERROR] No valid .rec file selected[/bold red]")
            return

        self.rec_filename = selected_file
        self.rec_filepath = os.path.join(self.directory, self.rec_filename)

        # Check if file exists
        if not os.path.isfile(self.rec_filepath):
            print(f"[bold red][ERROR] {self.rec_filename} is not found[/bold red]")
            return

        print(f"[bold green][INFO] {self.rec_filename} is found[/bold green]")

        # Confirm write operation
        dlg_checkWriteTags = DialogConfirm(title="Checking...", msg=f"Write tags to the {self.rec_filename}?")

        if not dlg_checkWriteTags.exec():
            print("[bold yellow][MESSAGE] Write Cancelled![/bold yellow]")
            return

        # Scan existing comments
        self.tags_read, self.preserved_content, self.original_content = self.scan_rec_commments(self.rec_filepath)

        # Use te_tags content directly (can be from form or manually edited)
        self.tags_to_be_written = self.ui.te_tags.toPlainText().splitlines()

        # Handle case with existing tags
        if self.tags_read:
            dlg_checkOverwriteTags = DialogConfirm(title="Checking...", msg="Overwrite existing tags?")

            if not dlg_checkOverwriteTags.exec():
                print("[bold yellow][MESSAGE] Overwrite Cancelled![/bold yellow]")
                return
            else:
                print("[bold yellow][WARNING] Overwrite Confirmed![/bold yellow]")

        # Backup before writing (can be recovered)
        self.backup_rec_contents(self.directory, self.rec_filename, self.original_content)

        # Track if this is an overwrite (has existing tags)
        is_overwrite = bool(self.tags_read)

        # Write tags to file (either no existing tags or overwrite confirmed)
        contents_to_be_written = self.preserved_content + self.tags_to_be_written
        with open(self.rec_filepath, mode="w", encoding="utf-16-LE") as f:
            f.write("\n".join(contents_to_be_written))
            print(f"[bold green][INFO] Tags were written to {self.rec_filename}![/bold green]")

        # Reload the written file's content (no need to repopulate combobox)
        self.load_selected_rec_file()

        # Auto-increment serial number only for new writes (not overwrites)
        if not is_overwrite:
            self.sn_inc()

    def read_rec(self):
        self.directory = self.ui.te_recDir.toPlainText()
        self.rec_filename = self.ui.le_filenameSN.text().replace(".tif", ".tif.rec")
        self.rec_filepath = os.path.join(self.directory, self.rec_filename)

        if not os.path.isfile(self.rec_filepath):
            print(f"[bold red][ERROR] {self.rec_filename} is not found[/bold red]")
            return
        else:
            print(f"[bold green][INFO] {self.rec_filename} is found[/bold green]")

        print(f"[bold green][INFO] Tags were loaded from {self.rec_filename}![/bold green]")
        self.ui.te_tags.clear()
        self.tags_read, _, _ = self.scan_rec_commments(self.rec_filepath)
        self.ui.te_tags.setPlainText("\n".join(self.tags_read))

    def revert_rec(self):
        self.directory = self.ui.te_recDir.toPlainText()
        self.rec_filename = self.ui.le_filenameSN.text().replace(".tif", ".tif.rec")
        self.rec_filepath = os.path.join(self.directory, self.rec_filename)

        if not os.path.isfile(self.rec_filepath):
            print(f"[bold red][ERROR] {self.rec_filename} is not found[/bold red]")
            return
        else:
            print(f"[bold green][INFO] {self.rec_filename} is found[/bold green]")

        recovery_filepath = os.path.join(self.directory, "rec_backups.json")
        if not os.path.isfile(recovery_filepath):
            print("[bold red][ERROR] No backup file (JSON) is found![/bold red]")
            return
        else:
            with open(recovery_filepath, mode="r") as f:
                self.recBackups = json.load(f)
            print("[bold green][INFO] Backup JSON file is Loaded![/bold green]")

        dlg_checkRecover = DialogConfirm(
            title="Checking...",
            msg=f"Recover {self.rec_filename} to the original state?",
        )
        if not dlg_checkRecover.exec():
            print("[bold yellow][MESSAGE] Recovery Cancelled![/bold yellow]")
            return
        else:
            print("[bold yellow][WARNING] Recovery Confirmed![/bold yellow]")

        with open(self.rec_filepath, mode="w", encoding="utf-16-LE") as f:
            if self.rec_filename in self.recBackups.keys():
                f.write("\n".join(self.recBackups[self.rec_filename][0]))
                print(f"[bold green][INFO] {self.rec_filename} was recovered![/bold green]")
            else:
                print(f"[bold red][ERROR] Recovery failed! {self.rec_filename} was not found in the backup![/bold red]")
