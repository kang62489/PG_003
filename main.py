## Author: Kang
## Last Update: 2025-Jan-22
## Usage: A gui interface for generating metadata tag which will be pasted to each recording file (.rec)

## Modules
from email.charset import QP
import os
import sys
import json
from tabulate import tabulate
from pathlib import Path
import glob
from rich import print
import pandas as pd
from PySide6.QtCore import Qt, QSize
from PySide6.QtCore import QModelIndex, QItemSelectionModel
from PySide6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QDialog,
    QPushButton
)
from PySide6.QtUiTools import QUiLoader

# Customized models
from classes import (
    delegate_table,
    dialog_confirm,
    dialog_saveTemplate,
    dialog_addProperties,
    dialog_exportMD,
    layout_buttonSets,
    model_table,
    model_comboBox,
    delegate_table
    )


loader = QUiLoader()
basedir = os.path.dirname(__file__)

class MainPanel:
    def __init__(self):
        super().__init__()
        self.ui = loader.load(os.path.join(basedir, "ui/metadata_generator.ui"), None)
        self.ui.setWindowTitle("Metadata Generator")
        self.ui.show()
        with open("styles/styles.qss", "r") as f:
            self.ui.setStyleSheet(f.read())
        
        # Set Models
        self.setModels()
        
        # Set UIs
        self.setUI()
        
        # Set attributes of UIs
        self.setUIAttr()

        # List object names of tab_0, tab_1
        self.tab0_objs = self.list_objs(self.ui.tab_0)
        self.tab1_objs = self.list_objs(self.ui.tab_1)
        print("Objects in Tab_0: ",self.tab0_objs)
        print("Objects in Tab_1: ",self.tab1_objs)
        
## Functions for initialization
    def list_objs(self, parent_widget):
        return [child.objectName() for child in parent_widget.children()]
    
    def setUI(self):
        # Set the button for loading a template
        self.ui.btn_loadTemplate.clicked.connect(self.loadTemplate)
        
        # Set the button for saveing a template
        self.ui.btn_saveTemplate.clicked.connect(self.saveTemplate)
        
        # Set the button for deleting current template
        self.ui.btn_deleteCurrentTemplate.clicked.connect(self.deleteTemplate)
        self.ui.btn_deleteCurrentTemplate.setEnabled(False)
        
        # Set the button for exporting metadata
        self.ui.btn_exportExpInfo.clicked.connect(self.exportExpInfo)
        
        # Set the button for adding or inserting rows of properties
        self.ui.btn_addNewRows.clicked.connect(self.addNewRows)
        
        # Set the button for removing selected rows
        self.ui.btn_removeSelectedRows.clicked.connect(self.removeSelectedRows)
        
        # Set the button for moving a row up and down
        self.ui.btn_moveUp.clicked.connect(self.moveRowUp)
        self.ui.btn_moveDown.clicked.connect(self.moveRowDown)
        
        # Set the button for load a tag set
        self.ui.btn_loadTagSet.clicked.connect(self.loadTagSet)
    
    def setUIAttr(self):
        # Set attributes of buttons
        size_01 = QSize(150, 60)
        size_02 = QSize(180, 40)
        
        self.ui.btn_loadTemplate.setMaximumSize(size_01)
        self.ui.btn_saveTemplate.setMaximumSize(size_01)
        self.ui.btn_deleteCurrentTemplate.setMaximumSize(size_01)
        self.ui.btn_exportExpInfo.setMaximumSize(size_01)
        self.ui.btn_addNewRows.setMaximumSize(size_01)
        self.ui.btn_removeSelectedRows.setMaximumSize(size_01)
        self.ui.btn_moveUp.setMaximumSize(size_01)
        self.ui.btn_moveDown.setMaximumSize(size_01)
        
        # Set attributes of QComboBox (cb_expInfo)
        self.ui.cb_expInfo.setMaximumSize(size_02)
        
        # Set attributes of QLabel (lbl_expInfo)
        self.ui.lbl_expInfo.setMaximumSize(size_02)
        self.ui.lbl_expInfo.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        
        # Set the attributes of QTableView (tv_expInfo)
        self.ui.tv_expInfo.verticalHeader().setDefaultAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.ui.tv_expInfo.horizontalHeader().setVisible(False)
        self.ui.tv_expInfo.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.ui.tv_expInfo.setItemDelegate(delegate_table.CellEditDelegate())
        

    def setModels(self):
        # Set the model displays in QTableView (tv_expInfo)
        self.model_tv_01 = model_table.TableModel()
        self.ui.tv_expInfo.setModel(self.model_tv_01)
        self.sm_expInfo = self.ui.tv_expInfo.selectionModel()
        
        # Set the model for the menu of QComboBox (cb_expInfo, cb_recTagSet)
        self.model_cb_01 = model_comboBox.SelectorModel()
        self.model_cb_02 = model_comboBox.SelectorModel()
        self.loadMenuList()
        self.ui.cb_expInfo.setModel(self.model_cb_01)
        self.ui.cb_recTagSet.setModel(self.model_cb_02)
        
    def loadMenuList(self):
        with open("models/cb_list_01.json", "r") as f:
            saved_cb_list_01= json.load(f)
        pass
        
        with open("models/cb_list_02.json", "r") as f:
            saved_cb_list_02= json.load(f)
        pass
    
        templateFiles = [os.path.basename(i) for i in glob.glob(os.path.join(basedir,"models",'template_*.json'))]
        templateList = [Path(tempName.replace("template_","")).stem for tempName in templateFiles]
        
        tagSetFiles = [os.path.basename(i) for i in glob.glob(os.path.join(basedir,"models",'tagSet_*.json'))]
        tagSetList = [Path(tempName.replace("tagSet_","")).stem for tempName in tagSetFiles]
        
        if saved_cb_list_01 != templateList:
            with open("models/cb_list_01.json", "w") as f:
                json.dump(templateList, f)
                self.model_cb_01.selections=templateList
        else:
            self.model_cb_01.selections = saved_cb_list_01
    
        if saved_cb_list_02 != tagSetList:
            with open("models/cb_list_02.json", "w") as f:
                json.dump(tagSetList, f)
                self.model_cb_02.selections=tagSetList
        else:
            self.model_cb_02.selections = saved_cb_list_02
            
    def reloadMenuList(self):
        templateFiles = [os.path.basename(i) for i in glob.glob(os.path.join(basedir,"models",'template_*.json'))]
        templateList = [Path(tempName.replace("template_","")).stem for tempName in templateFiles]
        with open("models/cb_list_01.json", "w") as f:
            json.dump(templateList, f)
        
        self.model_cb_01.updateList(templateList)
        self.model_cb_01.layoutChanged.emit()
        
        tagSetFiles = [os.path.basename(i) for i in glob.glob(os.path.join(basedir,"models",'tagSet_*.json'))]
        tagSetList = [Path(tempName.replace("tagSet_","")).stem for tempName in tagSetFiles]
        
        with open("models/cb_list_02.json", "w") as f:
            json.dump(tagSetList, f)
            self.model_cb_02.selections=tagSetList

## Functions for buttons in Tab_0    
    def loadTemplate(self):
        filename = self.model_cb_01.selections[self.ui.cb_expInfo.currentIndex()]
        if filename == "default":
            self.ui.btn_deleteCurrentTemplate.setEnabled(False)
        else:
            self.ui.btn_deleteCurrentTemplate.setEnabled(True)
        
        with open("models/template_{}.json".format(filename), "r") as f:
            template = pd.read_json(f, dtype=str)
        pass
                 
        self.model_tv_01.update(template)
        self.ui.tv_expInfo.resizeColumnsToContents()
        self.model_tv_01.layoutChanged.emit()
    
    def saveTemplate(self):
        if not self.model_tv_01._data.empty:
            self.saveCheck = dialog_confirm.Confirm(title="Checking...", msg="Save current template?")
            
            if self.saveCheck.exec():
                self.saveDialog = dialog_saveTemplate.SaveTemplate()
                self.saveDialog.savefile(os.path.join(basedir,"models"), self.model_tv_01._data)
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
            os.remove(os.path.join(basedir,"models","template_{}.json".format(filename)))
            self.reloadMenuList()
            self.clearQTableView(self.model_tv_01)
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

## Functions for buttons in Tab_1
    def loadTagSet(self):
        filename = self.model_cb_02.selections[self.ui.cb_recTagSet.currentIndex()]
        if filename == "default":
            self.ui.btn_deleteTagSet.setEnabled(False)
        else:
            self.ui.btn_deleteTagSet.setEnabled(True)
            
        with open("models/tagSet_{}.json".format(filename), "r") as f:
            tagSet = json.load(f)
        pass
        
        # Set buttons for each configuration
        self.btnSet = layout_buttonSets.TagSwitch(numOfConfigs=len(tagSet))
        lo = self.btnSet.output_layout()
        
        # Create a widget to hold the layout
        widget = QPushButton()
        # widget.setLayout(lo)
        
        # Add the widget to gb_tagSwitch
        self.ui.gb_tagSwitch.layout().addWidget(widget)
        self.ui.page.layout().addWidget(widget)

        
            
    
app = QApplication(sys.argv)
window = MainPanel()


app.exec()

# if __name__ == "__main__":
#     pass
