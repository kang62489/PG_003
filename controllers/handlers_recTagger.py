import os, json, glob
import pandas as pd
from datetime import datetime
from pathlib import Path
from PySide6.QtCore import QModelIndex, QItemSelectionModel, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QDialog, QApplication
from rich import print
from classes import (
    model_list_1,
    model_table_1,
    dialog_confirm,
    dialog_insertProperties,
    dialog_saveTemplate,
    dialog_getPath
    )
from util.constants import (
    MODELS_DIR,
    DISPLAY_DATE_FORMAT,
    SERIAL_NAME_REGEX
    )

class RecTaggerHandlers:
    def __init__(self, ui):
        self.ui = ui
        self.model_tableView_customized = model_table_1.TableModel()
        self.ui.tableView_customized.setModel(self.model_tableView_customized)
        self.sm_customized = self.ui.tableView_customized.selectionModel()

        self.model_menuList_templates = model_list_1.ListModel()
        self.ui.comboBox_tagTemplates.setModel(self.model_menuList_templates)
        
        # Set validtor for cheking filename-SN.tif
        regex = QRegularExpression(SERIAL_NAME_REGEX)
        self.validator = QRegularExpressionValidator(regex)
        self.dateStr = datetime.today().strftime(DISPLAY_DATE_FORMAT)
        
        self.recBackups = dict()
        
        self.connect_signals()
        self.updateTagOutput()
        self.reloadMenuList_templates()
        self.loadTemplate()
        
    def connect_signals(self):
        self.ui.radioBtnGroup_OBJ.buttonClicked.connect(self.updateTagOutput)
        self.ui.comboBox_EXC.activated.connect(self.updateTagOutput)
        self.ui.comboBox_EXC.currentIndexChanged.connect(self.autoSelectEMI)
        self.ui.lineEdit_LEVEL.textChanged.connect(self.updateTagOutput)
        self.ui.lineEdit_EXPO.textChanged.connect(self.updateTagOutput)
        self.ui.comboBox_EXPO_UNITS.activated.connect(self.updateTagOutput)
        self.ui.comboBox_EMI.activated.connect(self.updateTagOutput)
        self.ui.comboBox_EMI.currentIndexChanged.connect(self.autoSelectEXC)
        self.ui.lineEdit_FRAMES.textChanged.connect(self.updateTagOutput)
        self.ui.lineEdit_FPS.textChanged.connect(self.updateTagOutput)
        self.ui.spinBox_SLICE.valueChanged.connect(self.updateTagOutput)
        self.ui.comboBox_CAM_TRIG_MODES.activated.connect(self.updateTagOutput)
        self.ui.spinBox_SLICE.valueChanged.connect(self.updateTagOutput)
        self.ui.comboBox_LOC_TYPES.activated.connect(self.updateTagOutput)
        self.ui.spinBox_AT.valueChanged.connect(self.updateTagOutput)
        self.ui.checkBox_addCustomized.stateChanged.connect(self.updateTagOutput)
        
        # Emit signal to update tag output when the table in the QTableView (tableView_customized) is changed
        self.model_tableView_customized.dataChanged.connect(self.updateTagOutput)
        self.model_tableView_customized.layoutChanged.connect(self.updateTagOutput)
        
        self.ui.comboBox_tagTemplates.activated.connect(self.loadTemplate)
        self.ui.btn_saveTemplate.clicked.connect(self.saveTemplate)
        self.ui.btn_deleteCurrentTemplate.clicked.connect(self.deleteTemplate)
        self.ui.btn_addNewRows.clicked.connect(self.insert_customized_properties)
        self.ui.btn_removeSelectedRows.clicked.connect(self.removeSelectedRows)
        self.ui.btn_moveUp.clicked.connect(self.moveRowsUp)
        self.ui.btn_moveDown.clicked.connect(self.moveRowsDown)
        
        self.ui.lineEdit_recDir.textChanged.connect(self.isRecDirectoryValid)
        self.ui.btn_browse.clicked.connect(self.browseRecDirectory)
        
        self.ui.lineEdit_filenameSN.textChanged.connect(self.isFilenameSNValid)
        
        self.ui.btn_increaseSN.clicked.connect(self.increaseSN)
        self.ui.btn_decreaseSN.clicked.connect(self.decreaseSN)
        self.ui.btn_resetSN.clicked.connect(self.resetSN)
        self.ui.btn_copyFilenameSN.clicked.connect(self.copyFilenameSN)
        
        self.ui.btn_writeToRec.clicked.connect(self.writeToRec)
        self.ui.btn_loadFromRec.clicked.connect(self.loadFromRec)
        self.ui.btn_recoverRec.clicked.connect(self.recoverRec)
    
    def autoSelectEMI(self):
        if self.ui.comboBox_EXC.currentText() == "HLG":
            self.ui.comboBox_EMI.setCurrentIndex(0)
        elif self.ui.comboBox_EXC.currentText() == "LED_GREEN":
            self.ui.comboBox_EMI.setCurrentIndex(1)
        elif self.ui.comboBox_EXC.currentText() == "LED_BLUE":
            self.ui.comboBox_EMI.setCurrentIndex(2)
    
    def autoSelectEXC(self):
        if self.ui.comboBox_EMI.currentText() == "IR":
            self.ui.comboBox_EXC.setCurrentIndex(0)
        elif self.ui.comboBox_EMI.currentText() == "RED":
            self.ui.comboBox_EXC.setCurrentIndex(1)
        elif self.ui.comboBox_EMI.currentText() == "GREEN":
            self.ui.comboBox_EXC.setCurrentIndex(2)
    
    
    def updateTagOutput(self):
        self.clearTagOutput()
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
            self.ui.comboBox_EXC.currentText(),
            self.ui.lineEdit_LEVEL.text(),
            self.ui.lineEdit_EXPO.text() + self.ui.comboBox_EXPO_UNITS.currentText(),
            self.ui.comboBox_EMI.currentText(),
            self.ui.lineEdit_FRAMES.text(),
            self.ui.lineEdit_FPS.text(),
            self.ui.comboBox_CAM_TRIG_MODES.currentText(),
            self.ui.spinBox_SLICE.value(),
            self.ui.comboBox_LOC_TYPES.currentText() + str(self.ui.spinBox_AT.value())
        ]
        
        if self.ui.checkBox_addCustomized.isChecked():
            for prop, val in zip(self.model_tableView_customized._data.index.tolist(), self.model_tableView_customized._data["VALUE_0"].tolist()):
                props.append(prop)
                values.append(val)
        
        for prop, val in zip(props, values):
            self.ui.textEdit_tags.append(f"{prop}: {val}")
    
    def clearTagOutput(self):
        self.ui.textEdit_tags.clear()
        
    def reloadMenuList_templates(self):
        templateFiles = [os.path.basename(i) for i in glob.glob(os.path.join(MODELS_DIR,'template_*.json'))]
        templateList = [Path(tempName.replace("template_","")).stem for tempName in templateFiles]
        for file in templateList:
            if file == "patch_default":
                templateList.remove(file)
                templateList.insert(0, file)
            elif file == "puff_default":
                templateList.remove(file)
                templateList.insert(1, file)
        
        with open(MODELS_DIR / "menuList_templates.json", "w") as f:
            json.dump(templateList, f, indent=4)
        
        self.model_menuList_templates.updateList(templateList)
        self.model_menuList_templates.layoutChanged.emit()
        
    def loadTemplate(self):
        filename = self.model_menuList_templates.list_of_options[self.ui.comboBox_tagTemplates.currentIndex()]
        self.ui.btn_deleteCurrentTemplate.setEnabled(False)
        
        if filename not in ["patch_default", "puff_default"] :
            self.ui.btn_deleteCurrentTemplate.setEnabled(True)
        
        with open(MODELS_DIR / "template_{}.json".format(filename), "r") as f:
            template = pd.read_json(f, dtype=str)
            self.model_tableView_customized.update(template)
            self.model_tableView_customized.layoutChanged.emit()
        
    def saveTemplate(self):
        if self.model_tableView_customized._data.empty:
            print("[bold red]Template doesn't exist![/bold red]")
            return
        
        self.saveCheck = dialog_confirm.Confirm(title="Checking...", msg="Save current template?")
        if not self.saveCheck.exec():
            print("[bold yellow]Save Cancelled![/bold yellow]")
            return
            
        self.saveDialog = dialog_saveTemplate.SaveTemplate()
        if not self.saveDialog.exec():
            print("[bold yellow]Save Cancelled![/bold yellow]")
            return
        
        self.saveDialog.savefile(os.path.join(MODELS_DIR), self.model_tableView_customized._data)
        
        # reload the menu list
        self.reloadMenuList_templates()
        
        # set the QComboBox display the saved template
        for idx, item in enumerate(self.model_menuList_templates.list_of_options):
            if item == self.saveDialog.lineEdit_filename.text():
                self.ui.comboBox_tagTemplates.setCurrentIndex(idx)
                self.loadTemplate()
                break

    def deleteTemplate(self):
        filename = self.model_menuList_templates.list_of_options[self.ui.comboBox_tagTemplates.currentIndex()]
        self.deleteCheck = dialog_confirm.Confirm(title="Checking...", msg="Delete current template?")
        
        if self.deleteCheck.exec():
            os.remove(os.path.join(MODELS_DIR,"template_{}.json".format(filename)))
            self.reloadMenuList_templates()
            self.clearQTableView(self.model_tableView_customized)
            self.ui.btn_deleteCurrentTemplate.setEnabled(False)
        else:
            print("Delete Cancelled!")

    def clearQTableView(self, model):
        model.update(pd.DataFrame())
        model.layoutChanged.emit()

    def isTableViewEmpty(self):
        return self.model_tableView_customized._data.empty

    def insert_customized_properties(self):
        if self.isTableViewEmpty():
            print("[bold red]Please load a template first![/bold red]")
            return
        
        if self.sm_customized.hasSelection():
            insert_from_this_row = self.sm_customized.currentIndex().row()
        else:
            insert_from_this_row = self.model_tableView_customized.rowCount(QModelIndex())-1
            
            
        self.dlg_insertion = dialog_insertProperties.InsertProp()
        if not self.dlg_insertion.exec() == QDialog.Accepted:
            print("Cancel Insertion!")
            return
        
        self.model_tableView_customized.addRows(QModelIndex(), insert_from_this_row, self.dlg_insertion.dataToBeAdded)
        new_index = self.model_tableView_customized.index(insert_from_this_row + self.dlg_insertion.dataToBeAdded.shape[0], self.dlg_insertion.dataToBeAdded.shape[1]-1)
        self.sm_customized.setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
        
    def removeSelectedRows(self):
        selected_indexes = self.sm_customized.selectedIndexes()
        if selected_indexes == []:
            print("No row is selected")
            return
        
        rows_to_be_removed = sorted(set(index.row() for index in selected_indexes), reverse=True)
        for row in rows_to_be_removed:
            self.model_tableView_customized.rmRows(QModelIndex(), row, 1)

    def moveRowsUp(self):
        selected_indexes = self.sm_customized.selectedIndexes()
        if not selected_indexes:
            print("No row is selected")
            return
        
        # Get indices of selected rows
        rows = sorted(set(index.row() for index in selected_indexes))
        
        # Move rows up
        new_positions_of_moved_rows = self.model_tableView_customized.moveRows(rows, -1)
        # Reselect the moved rows
        self.sm_customized.clearSelection()
        for row in new_positions_of_moved_rows:
            index = self.model_tableView_customized.index(row, 0)
            self.sm_customized.select(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
            
    def moveRowsDown(self):
        selected_indexes = self.sm_customized.selectedIndexes()
        if not selected_indexes:
            print("No row is selected")
            return
        
        # Get indices of selected rows
        rows = sorted(set(index.row() for index in selected_indexes))
        
        # Move rows down
        new_positions_of_moved_rows = self.model_tableView_customized.moveRows(rows, 1)
        # Reselect the moved rows
        self.sm_customized.clearSelection()
        for row in new_positions_of_moved_rows:
            index = self.model_tableView_customized.index(row, 0)
            self.sm_customized.select(index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
            
    def browseRecDirectory(self):
        self.dlg_requestRecDirectory = dialog_getPath.GetPath()
        self.directory = self.dlg_requestRecDirectory.get_path()
        if self.directory == "":
            self.ui.lineEdit_recDir.setText("No selected directory")
        else:
            self.ui.lineEdit_recDir.setText(self.directory)
            
    def isRecDirectoryValid(self):
        self.directory = self.ui.lineEdit_recDir.text()
        prefix_text = self.ui.lbl_recDir.text()
        if not os.path.isdir(self.directory):
            dirCheckText = prefix_text + " (Invalid)"
            self.ui.lbl_recDir.setText(dirCheckText)
            self.ui.lbl_recDir.setStyleSheet("color: tomato;")
        else:
            direCheckText = prefix_text + " (Valid)"
            self.ui.lbl_recDir.setText(direCheckText)
            self.ui.lbl_recDir.setStyleSheet("color: green;")
    
    def isFilenameSNValid(self):
        self.ui.lineEdit_filenameSN.setValidator(self.validator)
        if self.ui.lineEdit_filenameSN.hasAcceptableInput():
            self.ui.lineEdit_filenameSN.setStyleSheet("QLineEdit { color: green; }")
            self.ui.btn_copyFilenameSN.setEnabled(True)
            self.ui.lineEdit_filenameSN.setValidator(None)
        else:
            self.ui.lineEdit_filenameSN.setStyleSheet("QLineEdit { color: tomato; }")
            self.ui.btn_copyFilenameSN.setEnabled(False)
            self.ui.lineEdit_filenameSN.setValidator(None)
        
    def increaseSN(self):
        self.dateStr = self.ui.lineEdit_filenameSN.text().split("-")[0]
        latest_value = (self.ui.lineEdit_filenameSN.text().split("-")[1].split(".")[0])
        self.Serial = int(latest_value)
        if self.Serial < 9999:
            self.Serial += 1
            self.ui.lineEdit_filenameSN.setText(f"{self.dateStr}-{self.Serial:04d}.tif")
        elif self.Serial == 9999:
            self.Serial = 0
            self.ui.lineEdit_filenameSN.setText(f"{self.dateStr}-{self.Serial:04d}.tif")
            
    def decreaseSN(self):
        self.dateStr = self.ui.lineEdit_filenameSN.text().split("-")[0]
        latest_value = (self.ui.lineEdit_filenameSN.text().split("-")[1].split(".")[0])
        self.Serial = int(latest_value)
        if self.Serial > 0:
            self.Serial -= 1
            self.ui.lineEdit_filenameSN.setText(f"{self.dateStr}-{self.Serial:04d}.tif")
        elif self.Serial == 0:
            self.Serial = 0
            self.ui.lineEdit_filenameSN.setText(f"{self.dateStr}-{self.Serial:04d}.tif")
    
    def resetSN(self):
        self.dateStr = self.ui.lineEdit_filenameSN.text().split("-")[0]
        self.Serial = 0
        self.ui.lineEdit_filenameSN.setText(f"{self.dateStr}-{self.Serial:04d}.tif")
    
    def copyFilenameSN(self):
        QApplication.clipboard().setText(self.ui.lineEdit_filenameSN.text())
        
    def scan_rec_commments(self, rec_filepath):
        with open(rec_filepath, mode="r", encoding="utf-16-LE") as f:
            original_content = f.read().splitlines()
            write_from_line = 0
            keep_to_line = 0
            for line_num, line_content in enumerate(original_content):
                if 'Comment:' in line_content:
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
    
        backup_path=os.path.join(rec_directory, f"rec_backups.json")
        with open(backup_path, mode="w") as f:
            json.dump(self.recBackups, f, indent=4)
            self.ui.textBrowser_status.append("<span style='color: lime;'>[INFO] Backup saved!</span>")
        
    def writeToRec(self):
        # Prepare filename and path
        self.rec_filename = self.ui.lineEdit_filenameSN.text().replace(".tif", ".tif.rec")
        self.rec_filepath = os.path.join(self.directory, self.rec_filename)
        
        # Check if file exists
        if not os.path.isfile(self.rec_filepath):
            self.ui.textBrowser_status.setText(f"<span style='color: tomato;'>[ERROR] {self.rec_filename} is not found</span>")
            return
        
        self.ui.textBrowser_status.setText(f"<span style='color: lime;'>[INFO] {self.rec_filename} is found</span>")
        
        # Confirm write operation
        dlg_checkWriteTags = dialog_confirm.Confirm(
            title="Checking...", 
            msg=f"Write tags to the {self.rec_filename}?"
        )
        
        if not dlg_checkWriteTags.exec():
            self.ui.textBrowser_status.append("<span style='color: white;'>[MESSAGE] Write Cancelled!</span>")
            return
        
        # Scan existing comments
        self.tags_read, self.preserved_content, self.original_content = self.scan_rec_commments(self.rec_filepath)
        self.tags_to_be_written = self.ui.textEdit_tags.toPlainText().splitlines()

        # Handle case with existing tags
        if self.tags_read:
            dlg_checkOverwriteTags = dialog_confirm.Confirm(
                title="Checking...", 
                msg="Overwrite existing tags?"
            )
            
            if not dlg_checkOverwriteTags.exec():
                self.ui.textBrowser_status.append("<span style='color: white;'>[MESSAGE] Overwrite Cancelled!</span>")
                return
            else:
                self.ui.textBrowser_status.append("<span style='color: yellow;'>[WARNING] Overwrite Confirmed!</span>")

        # Backup before writing (can be recovered)
        self.backup_rec_contents(self.directory, self.rec_filename, self.original_content)
        
        # Write tags to file (either no existing tags or overwrite confirmed)
        contents_to_be_written = self.preserved_content + self.tags_to_be_written
        print("contents_to_be_written:",contents_to_be_written)
        with open(self.rec_filepath, mode="w", encoding="utf-16-LE") as f:
            f.write("\n".join(contents_to_be_written))
            self.ui.textBrowser_status.append(f"<span style='color: lime;'>[INFO] Tags were written to {self.rec_filename}!</span>")

        self.increaseSN()

    def loadFromRec(self):
        self.directory = self.ui.lineEdit_recDir.text()
        self.rec_filename = self.ui.lineEdit_filenameSN.text().replace(".tif", ".tif.rec")
        self.rec_filepath = os.path.join(self.directory, self.rec_filename)
        
        if not os.path.isfile(self.rec_filepath):    
            self.ui.textBrowser_status.setText(f"<span style='color: tomato;'>[ERROR] {self.rec_filename} is not found</span>")
            return
        else:
            self.ui.textBrowser_status.setText(f"<span style='color: lime;'>[INFO] {self.rec_filename} is found</span>")
        
        self.ui.textBrowser_status.append(f"<span style='color: lime;'>[INFO] Tags were loaded from {self.rec_filename}!</span>")
        self.ui.textEdit_tags.clear()
        self.tags_read, _, _ = self.scan_rec_commments(self.rec_filepath)
        self.ui.textEdit_tags.setPlainText("\n".join(self.tags_read))

    def recoverRec(self):
        self.directory = self.ui.lineEdit_recDir.text()
        self.rec_filename = self.ui.lineEdit_filenameSN.text().replace(".tif", ".tif.rec")
        self.rec_filepath = os.path.join(self.directory, self.rec_filename)
        
        if not os.path.isfile(self.rec_filepath):    
            self.ui.textBrowser_status.setText(f"<span style='color: tomato;'>[ERROR] {self.rec_filename} is not found</span>")
            return
        else:
            self.ui.textBrowser_status.setText(f"<span style='color: lime;'>[INFO] {self.rec_filename} is found</span>")
        
        recovery_filepath = os.path.join(self.directory, "rec_backups.json")
        if not os.path.isfile(recovery_filepath):
            self.ui.textBrowser_status.append("<span style='color: tomato;'>[ERROR] No backup file (JSON) is found!</span>")
            return
        else:
            with open(recovery_filepath, mode="r") as f:
                self.recBackups = json.load(f)
            self.ui.textBrowser_status.append("<span style='color: lime;'>[INFO] Backup JSON file is Loaded!</span>")
    
        dlg_checkRecover = dialog_confirm.Confirm(title="Checking...", msg=f"Recover {self.rec_filename} to the original state?")
        if not dlg_checkRecover.exec():
            self.ui.textBrowser_status.append("<span style='color: white;'>[MESSAGE] Recovery Cancelled!</span>")
            return
        else:
            self.ui.textBrowser_status.append("<span style='color: yellow;'>[WARNING] Recovery Confirmed!</span>")
        
        with open(self.rec_filepath, mode="w", encoding="utf-16-LE") as f:
            if self.rec_filename in self.recBackups.keys():
                f.write("\n".join(self.recBackups[self.rec_filename][0]))
                self.ui.textBrowser_status.append(f"<span style='color: lime;'>[INFO] {self.rec_filename} was recovered!</span>")
            else:
                self.ui.textBrowser_status.append(f"<span style='color: tomato;'>[ERROR] Recovery failed! {self.rec_filename} was not found in the backup!</span>")