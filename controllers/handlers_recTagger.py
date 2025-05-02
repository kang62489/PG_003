import os, json, glob
import pandas as pd
from pathlib import Path
from PySide6.QtCore import QModelIndex, QItemSelectionModel
from PySide6.QtWidgets import QDialog, QApplication
from rich import print
from tabulate import tabulate
from classes import (
    model_list_1,
    model_table_1,
    dialog_confirm,
    dialog_insertProperties,
    dialog_saveTemplate
    )
from util.constants import (
    MODELS_DIR,
    BASE_DIR,
    )

class RecTaggerHandlers:
    def __init__(self, ui):
        self.ui = ui
        self.model_tableView_customized = model_table_1.TableModel(auto_calc=False)
        self.ui.tableView_customized.setModel(self.model_tableView_customized)
        self.sm_customized = self.ui.tableView_customized.selectionModel()

        self.model_cb_01 = model_list_1.ListModel()
        self.ui.comboBox_tagTemplates.setModel(self.model_cb_01)
        
        self.connect_signals()
        self.reloadMenuList()
        self.loadTemplate()
        
    def connect_signals(self):
        self.ui.radioBtnGroup_OBJ.buttonClicked.connect(self.updateTagOutput)
        self.ui.comboBox_EXC.activated.connect(self.updateTagOutput)
        self.ui.lineEdit_LEVEL.textChanged.connect(self.updateTagOutput)
        self.ui.lineEdit_EXPO.textChanged.connect(self.updateTagOutput)
        self.ui.comboBox_EXPO_UNITS.activated.connect(self.updateTagOutput)
        self.ui.comboBox_EMI.activated.connect(self.updateTagOutput)
        self.ui.lineEdit_FRAMES.textChanged.connect(self.updateTagOutput)
        self.ui.lineEdit_FPS.textChanged.connect(self.updateTagOutput)
        self.ui.spinBox_SLICE.valueChanged.connect(self.updateTagOutput)
        self.ui.comboBox_CAM_TRIG_MODES.activated.connect(self.updateTagOutput)
        self.ui.spinBox_SLICE.valueChanged.connect(self.updateTagOutput)
        self.ui.comboBox_LOC_TYPES.activated.connect(self.updateTagOutput)
        self.ui.spinBox_AT.valueChanged.connect(self.updateTagOutput)
        
        self.ui.comboBox_tagTemplates.activated.connect(self.loadTemplate)
        self.ui.btn_saveTemplate.clicked.connect(self.saveTemplate)
        self.ui.btn_deleteCurrentTemplate.clicked.connect(self.deleteTemplate)
        self.ui.btn_addNewRows.clicked.connect(self.insert_customized_properties)
        self.ui.btn_removeSelectedRows.clicked.connect(self.removeSelectedRows)
        self.ui.btn_moveUp.clicked.connect(self.moveRowsUp)
        self.ui.btn_moveDown.clicked.connect(self.moveRowsDown)
    
    def updateTagOutput(self):
        print(f"Selected objective: {self.ui.radioBtnGroup_OBJ.checkedButton().text()}")
    
    def reloadMenuList(self):
        templateFiles = [os.path.basename(i) for i in glob.glob(os.path.join(MODELS_DIR,'template_*.json'))]
        templateList = [Path(tempName.replace("template_","")).stem for tempName in templateFiles]
        with open(MODELS_DIR / "cb_list_01.json", "w") as f:
            json.dump(templateList, f)
        
        self.model_cb_01.updateList(templateList)
        self.model_cb_01.layoutChanged.emit()
        
    def loadTemplate(self):
        filename = self.model_cb_01.selections[self.ui.comboBox_tagTemplates.currentIndex()]
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
        self.reloadMenuList()
        
        # set the QComboBox display the saved template
        for idx, item in enumerate(self.model_cb_01.selections):
            if item == self.saveDialog.lineEdit_filename.text():
                self.ui.comboBox_tagTemplates.setCurrentIndex(idx)
                break


    def deleteTemplate(self):
        filename = self.model_cb_01.selections[self.ui.comboBox_tagTemplates.currentIndex()]
        self.deleteCheck = dialog_confirm.Confirm(title="Checking...", msg="Delete current template?")
        
        if self.deleteCheck.exec():
            os.remove(os.path.join(MODELS_DIR,"template_{}.json".format(filename)))
            self.reloadMenuList()
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
