import os, json, glob
import pandas as pd
from pathlib import Path
from PySide6.QtCore import QModelIndex, QItemSelectionModel
from PySide6.QtWidgets import QDialog
from classes import (
    model_table_1,
    model_comboBox,
    dialog_confirm,
    dialog_addProperties,
    dialog_exportMD,
    dialog_saveTemplate
    )
from util.constants import (
    MODELS_DIR,
    BASE_DIR
    )

class HandlersExpInfo:
    def __init__(self, ui):
        self.ui = ui
        self.model_tv_01 = model_table_1.TableModel()
        self.ui.tv_expInfo.setModel(self.model_tv_01)
        self.sm_expInfo = self.ui.tv_expInfo.selectionModel()

        self.model_cb_01 = model_comboBox.SelectorModel()
        self.ui.cb_expInfo.setModel(self.model_cb_01)
        
        self.connect_signals()
        self.reloadMenuList()
        
    def connect_signals(self):
        self.ui.btn_loadTemplate.clicked.connect(self.loadTemplate)
        self.ui.btn_saveTemplate.clicked.connect(self.saveTemplate)
        self.ui.btn_deleteCurrentTemplate.clicked.connect(self.deleteTemplate)
        self.ui.btn_exportExpInfo.clicked.connect(self.exportExpInfo)
        self.ui.btn_addNewRows.clicked.connect(self.addNewRows)
        self.ui.btn_removeSelectedRows.clicked.connect(self.removeSelectedRows)
        self.ui.btn_moveUp.clicked.connect(self.moveRowUp)
        self.ui.btn_moveDown.clicked.connect(self.moveRowDown)
    
    def reloadMenuList(self):
        # cb_01
        templateFiles = [os.path.basename(i) for i in glob.glob(os.path.join(BASE_DIR,"models",'template_*.json'))]
        templateList = [Path(tempName.replace("template_","")).stem for tempName in templateFiles]
        with open(MODELS_DIR / "cb_list_01.json", "w") as f:
            json.dump(templateList, f)
        
        self.model_cb_01.updateList(templateList)
        self.model_cb_01.layoutChanged.emit()
        
    def loadTemplate(self):
            filename = self.model_cb_01.selections[self.ui.cb_expInfo.currentIndex()]
            if filename == "default":
                self.ui.btn_deleteCurrentTemplate.setEnabled(False)
            else:
                self.ui.btn_deleteCurrentTemplate.setEnabled(True)
            
            with open(MODELS_DIR / "template_{}.json".format(filename), "r") as f:
                template = pd.read_json(f, dtype=str)
            pass
                    
            self.model_tv_01.update(template)
            self.model_tv_01.layoutChanged.emit()
        
    def saveTemplate(self):
        if not self.model_tv_01._data.empty:
            self.saveCheck = dialog_confirm.Confirm(title="Checking...", msg="Save current template?")
            
            if self.saveCheck.exec():
                self.saveDialog = dialog_saveTemplate.SaveTemplate()
                self.saveDialog.savefile(os.path.join(BASE_DIR,"models"), self.model_tv_01._data)
                self.reloadMenuList()
                
                for idx, item in enumerate(self.model_cb_01.selections):
                    if item == self.saveDialog.filename.text():
                        self.ui.cb_expInfo.setCurrentIndex(idx)
                        break

            else:
                print("Save Cancelled!")
        else:
            print("Template doesn't exist!")

    def deleteTemplate(self):
        filename = self.model_cb_01.selections[self.ui.cb_expInfo.currentIndex()]
        self.deleteCheck = dialog_confirm.Confirm(title="Checking...", msg="Delete current template?")
        
        if self.deleteCheck.exec():
            os.remove(os.path.join(BASE_DIR,"models","template_{}.json".format(filename)))
            self.reloadMenuList()
            self.clearQTableView(self.model_tv_01)
            self.ui.btn_deleteCurrentTemplate.setEnabled(False)
        else:
            print("Delete Cancelled!")

    def clearQTableView(self, model):
        model.update(pd.DataFrame())
        model.layoutChanged.emit()

    def isTableViewEmpty(self):
        return self.model_tv_01._data.empty

    def addNewRows(self):
        if self.sm_expInfo.hasSelection():
            idx = self.sm_expInfo.currentIndex()
            rowNumber = idx.row()
            self.w = dialog_addProperties.AddProp()
            if self.w.exec() == QDialog.Accepted:
                print("Add data:", self.w.addData)
                self.model_tv_01.addRows(QModelIndex(), rowNumber, self.w.addData)
                new_index = self.model_tv_01.index(rowNumber + self.w.addData.shape[0], self.w.addData.shape[1]-1)
                self.sm_expInfo.setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
                print(self.sm_expInfo.currentIndex())
        else:
            if not self.isTableViewEmpty():
                rowNumber = self.model_tv_01.rowCount(QModelIndex())-1
                self.w = dialog_addProperties.AddProp()
                if self.w.exec() == QDialog.Accepted:
                    print("Add data:", self.w.addData)
                    self.model_tv_01.addRows(QModelIndex(), rowNumber+2, self.w.addData)
                    new_index = self.model_tv_01.index(rowNumber + self.w.addData.shape[0], self.w.addData.shape[1]-1)
                    self.sm_expInfo.setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
            else:
                print("Please load a template first!")

    def removeSelectedRows(self):
        selected_indexes = self.sm_expInfo.selectedIndexes()
        
        if selected_indexes:
            rows = sorted(set(index.row() for index in selected_indexes), reverse=True)
            for row in rows:
                self.model_tv_01.rmRows(QModelIndex(), row, 1)
        else:
            print("No selected row")

    def moveRowUp(self):
        if self.sm_expInfo.hasSelection():
            idx = self.sm_expInfo.currentIndex()
            rowNumber = idx.row()
            if (rowNumber-1>=0):
                self.model_tv_01.moveRows(rowNumber, rowNumber - 1)
                new_index = self.model_tv_01.index(rowNumber-1, idx.column())
                self.sm_expInfo.setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
        else:
            print("No selected row")
            
    def moveRowDown(self):
        if self.sm_expInfo.hasSelection():
            idx = self.sm_expInfo.currentIndex()
            rowNumber = idx.row()
            if (rowNumber+1 < self.model_tv_01.rowCount(QModelIndex())):
                self.model_tv_01.moveRows(rowNumber, rowNumber + 2)
                new_index = self.model_tv_01.index(rowNumber+1, idx.column())
                self.sm_expInfo.setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
        else:
            print("No selected row")

    def exportExpInfo(self):
        if not self.isTableViewEmpty():
            self.exportCheck = dialog_confirm.Confirm(title="Checking...", msg="Export current metadata?")
            
            if self.exportCheck.exec():
                self.exportDialog = dialog_exportMD.ExportMD(self.model_tv_01._data)
            else:
                print("Export Cancelled!")
        else:
            print("Please load a template first!")