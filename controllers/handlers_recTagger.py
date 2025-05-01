import os, json, glob
import pandas as pd
from pathlib import Path
from PySide6.QtCore import QModelIndex, QItemSelectionModel
from PySide6.QtWidgets import QDialog
from rich import print
from classes import (
    model_list_1,
    model_table_1,
    dialog_confirm,
    dialog_addProperties,
    dialog_saveTemplate
    )
from util.constants import (
    MODELS_DIR,
    BASE_DIR,
    )

class RecTaggerHandlers:
    def __init__(self, ui):
        self.ui = ui
        self.model_tableView_customized = model_table_1.TableModel()
        self.ui.tableView_customized.setModel(self.model_tableView_customized)
        self.sm_customized = self.ui.tableView_customized.selectionModel()

        self.model_cb_01 = model_list_1.ListModel()
        self.ui.comboBox_tagTemplates.setModel(self.model_cb_01)
        
        self.connect_signals()
        self.reloadMenuList()
        
    def connect_signals(self):
        self.ui.radioBtnGroup_obj.buttonClicked.connect(self.magnificationSelected)
        self.ui.btn_loadTemplate.clicked.connect(self.loadTemplate)
        self.ui.btn_saveTemplate.clicked.connect(self.saveTemplate)
        self.ui.btn_deleteCurrentTemplate.clicked.connect(self.deleteTemplate)
        self.ui.btn_addNewRows.clicked.connect(self.addNewRows)
        self.ui.btn_removeSelectedRows.clicked.connect(self.removeSelectedRows)
        self.ui.btn_moveUp.clicked.connect(self.moveRowUp)
        self.ui.btn_moveDown.clicked.connect(self.moveRowDown)
    
    def magnificationSelected(self, selected_radio_btn):
        print(f"Selected objective: {selected_radio_btn.text()}")
    
    def reloadMenuList(self):
        # cb_01
        templateFiles = [os.path.basename(i) for i in glob.glob(os.path.join(MODELS_DIR,'template_*.json'))]
        templateList = [Path(tempName.replace("template_","")).stem for tempName in templateFiles]
        with open(MODELS_DIR / "cb_list_01.json", "w") as f:
            json.dump(templateList, f)
        
        self.model_cb_01.updateList(templateList)
        self.model_cb_01.layoutChanged.emit()
        
    def loadTemplate(self):
        filename = self.model_cb_01.selections[self.ui.comboBox_tagTemplates.currentIndex()]
        if filename == "patch":
            self.ui.btn_deleteCurrentTemplate.setEnabled(False)
        else:
            self.ui.btn_deleteCurrentTemplate.setEnabled(True)
        
        with open(MODELS_DIR / "template_{}.json".format(filename), "r") as f:
            template = pd.read_json(f, dtype=str)
        pass
                
        self.model_tableView_customized.update(template)
        self.model_tableView_customized.layoutChanged.emit()
        
    def saveTemplate(self):
        if not self.model_tableView_customized._data.empty:
            self.saveCheck = dialog_confirm.Confirm(title="Checking...", msg="Save current template?")
            
            if self.saveCheck.exec():
                self.saveDialog = dialog_saveTemplate.SaveTemplate()
                self.saveDialog.savefile(os.path.join(MODELS_DIR), self.model_tableView_customized._data)
                self.reloadMenuList()
                
                for idx, item in enumerate(self.model_cb_01.selections):
                    if item == self.saveDialog.filename.text():
                        self.ui.comboBox_tagTemplates.setCurrentIndex(idx)
                        break

            else:
                print("Save Cancelled!")
        else:
            print("Template doesn't exist!")

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

    def addNewRows(self):
        if self.sm_customized.hasSelection():
            idx = self.sm_customized.currentIndex()
            rowNumber = idx.row()
            self.w = dialog_addProperties.AddProp()
            if self.w.exec() == QDialog.Accepted:
                print("Add data:", self.w.addData)
                self.model_tableView_customized.addRows(QModelIndex(), rowNumber, self.w.addData)
                new_index = self.model_tableView_customized.index(rowNumber + self.w.addData.shape[0], self.w.addData.shape[1]-1)
                self.sm_customized.setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
                print(self.sm_customized.currentIndex())
        else:
            if not self.isTableViewEmpty():
                rowNumber = self.model_tableView_customized.rowCount(QModelIndex())-1
                self.w = dialog_addProperties.AddProp()
                if self.w.exec() == QDialog.Accepted:
                    print("Add data:", self.w.addData)
                    self.model_tableView_customized.addRows(QModelIndex(), rowNumber+2, self.w.addData)
                    new_index = self.model_tableView_customized.index(rowNumber + self.w.addData.shape[0], self.w.addData.shape[1]-1)
                    self.sm_customized.setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
            else:
                print("Please load a template first!")

    def removeSelectedRows(self):
        selected_indexes = self.sm_customized.selectedIndexes()
        
        if selected_indexes:
            rows = sorted(set(index.row() for index in selected_indexes), reverse=True)
            for row in rows:
                self.model_tableView_customized.rmRows(QModelIndex(), row, 1)
        else:
            print("No selected row")

    def moveRowUp(self):
        if self.sm_customized.hasSelection():
            idx = self.sm_customized.currentIndex()
            rowNumber = idx.row()
            if (rowNumber-1>=0):
                self.model_tableView_customized.moveRows(rowNumber, rowNumber - 1)
                new_index = self.model_tableView_customized.index(rowNumber-1, idx.column())
                self.sm_customized.setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
        else:
            print("No selected row")
            
    def moveRowDown(self):
        if self.sm_customized.hasSelection():
            idx = self.sm_customized.currentIndex()
            rowNumber = idx.row()
            if (rowNumber+1 < self.model_tableView_customized.rowCount(QModelIndex())):
                self.model_tableView_customized.moveRows(rowNumber, rowNumber + 2)
                new_index = self.model_tableView_customized.index(rowNumber+1, idx.column())
                self.sm_customized.setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
        else:
            print("No selected row")
