# Modules
import os, json, glob
import pandas as pd
from datetime import datetime
from pathlib import Path
from PySide6.QtCore import Qt, QSize ,QModelIndex, QItemSelectionModel
from PySide6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QDialog,
    QSizePolicy,
    QHeaderView
)
from classes import (
    model_table_2,
    model_comboBox,
    dialog_confirm,
    dialog_createTagSet,
    dialog_insertProperties,
    dialog_saveTagSet,
    widget_buttonSet,
    widget_tagDisplay,
    customized_delegate
    )
from util.constants import (
    MODELS_DIR,
    BASE_DIR,
    DATE_FORMAT
    )

class HandlersParameters:
    def __init__(self, ui):
        self.ui = ui
        self.date = datetime.today()
        self.model_cb_02 = model_comboBox.SelectorModel()
        self.ui.cb_recTagSet.setModel(self.model_cb_02)
        
        self.connect_signals()
        self.reloadMenuList()
        self.createModeSave = False
        
    def connect_signals(self):
        self.ui.btn_up.clicked.connect(self.moveUp)
        self.ui.btn_down.clicked.connect(self.moveDown)
        self.ui.btn_insert.clicked.connect(self.insert)
        self.ui.btn_rm.clicked.connect(self.rm)
        self.ui.btn_convert.clicked.connect(self.convert)
        
        self.ui.btn_loadTagSet.clicked.connect(self.loadTagSet)
        self.ui.btn_newTagSet.clicked.connect(self.newTagSet)
        self.ui.btn_discard.clicked.connect(self.discard)
        self.ui.btn_saveTagSet.clicked.connect(self.saveTagSet)
        self.ui.btn_deleteTagSet.clicked.connect(self.deleteTagSet)
        
        self.ui.btn_plus.clicked.connect(self.plus)
        self.ui.btn_minus.clicked.connect(self.minus)
        self.ui.btn_resetSerial.clicked.connect(self.resetSerial)
        self.ui.btn_copySerial.clicked.connect(self.copySerial)
        self.ui.btn_copyTag.clicked.connect(self.copyTag)
        self.ui.btn_clearTag.clicked.connect(self.clearTag)
        
    def reloadMenuList(self):
        tagSetFiles = [os.path.basename(i) for i in glob.glob(os.path.join(BASE_DIR,"models",'tagSet_*.json'))]
        tagSetList = [Path(tempName.replace("tagSet_","")).stem for tempName in tagSetFiles]
        with open(MODELS_DIR / "cb_list_02.json", "w") as f:
            json.dump(tagSetList, f)
        
        self.model_cb_02.updateList(tagSetList)
        self.model_cb_02.layoutChanged.emit()
        
    def groupBoxButtonSetting(self, tagSet):
        # Set buttons for each configuration
        btnSet = widget_buttonSet.ButtonSet(len(tagSet), direction="vertical")
        
        for i, btn in enumerate(btnSet.btnSwitches):
            btn.clicked.connect(lambda _, idx=i: self.pageSwitch(idx))
            # set btn attributes
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            btn.setFixedSize(QSize(100, 80))
        return btnSet
    
    def stackedWidgetSetting(self, tagSet):
        stackedModels = []
        stackedTabWidgets = []
        stackedSelectionModels = []
        for i in range(len(tagSet)):
            tagDisp = widget_tagDisplay.TagDisp(len(tagSet))
            tagModel = model_table_2.TableModel()
            tagDisp.tv_tag.setModel(tagModel)
            sm = tagDisp.tv_tag.selectionModel()
            self.ui.sw_tags.insertWidget(i, tagDisp)
            
            tagDisp.tv_tag.resizeColumnsToContents()
            tagDisp.tv_tag.horizontalHeader().setVisible(False)
            tagDisp.tv_tag.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            tagDisp.tv_tag.verticalHeader().setDefaultSectionSize(50)
            tagDisp.tv_tag.verticalHeader().setDefaultAlignment(Qt.AlignRight | Qt.AlignVCenter)
            tagDisp.tv_tag.setEditTriggers(QAbstractItemView.DoubleClicked | QAbstractItemView.EditKeyPressed)
            tagDisp.tv_tag.setItemDelegate(customized_delegate.CellEditDelegate())
            tagDisp.lbl_page.setText(f"Configuration {i}")
            
            tagModel.update(pd.DataFrame(tagSet[f"Config_{i}"]))
            tagModel.layoutChanged.emit()
            
            stackedModels.append(tagModel)
            stackedTabWidgets.append(tagDisp)
            stackedSelectionModels.append(sm)
            
        return [stackedTabWidgets, stackedModels, stackedSelectionModels]
    
    def pageSwitch(self, idx):
        self.ui.sw_tags.setCurrentIndex(idx)
    
    def loadTagSet(self):
        filename = self.model_cb_02.selections[self.ui.cb_recTagSet.currentIndex()]
        if filename == "default":
            self.ui.btn_deleteTagSet.setEnabled(False)
        else:
            self.ui.btn_deleteTagSet.setEnabled(True)
            
        with open(MODELS_DIR / "tagSet_{}.json".format(filename), "r") as f:
            tagSet = json.load(f)
        pass
        
        # default protection
        if self.ui.cb_recTagSet.currentText() == "default":
            self.ui.btn_deleteTagSet.setEnabled(False)
        else:
            self.ui.btn_deleteTagSet.setEnabled(True)
        
        # Set button swiches for switching configuration
        self.btnSet = self.groupBoxButtonSetting(tagSet)
        
        # Clear the layout of gb_tagSwitch
        self.clearGroupbox()
        
        # Add the widget to gb_tagSwitch
        self.ui.gb_tagSwitch.layout().addWidget(self.btnSet)
        
        # Clear the layout of sw_tags
        self.clearStackedWidget(self.ui.sw_tags)
        
        # Set the tag display for each configuration
        self.tagDisp = self.stackedWidgetSetting(tagSet)
        self.stackedTabWidgets = self.tagDisp[0]
        self.stackedModels = self.tagDisp[1]
        self.stackedSelectionModels = self.tagDisp[2]
        
    def createModeOn(self):
        self.ui.btn_loadTagSet.setVisible(False)
        self.ui.btn_newTagSet.setVisible(False)
        self.ui.btn_deleteTagSet.setVisible(False)
        self.ui.btn_discard.setVisible(True)
        self.ui.cb_recTagSet.setEnabled(False)
        self.createModeSave = True
    
    def createModeOff(self):
        self.ui.btn_loadTagSet.setVisible(True)
        self.ui.btn_newTagSet.setVisible(True)
        self.ui.btn_deleteTagSet.setVisible(True)
        self.ui.btn_discard.setVisible(False)
        self.ui.cb_recTagSet.setEnabled(True)
        self.createModeSave = False
    
    def clearStackedWidget(self, stacked_widget):
        while stacked_widget.count():
            page = stacked_widget.widget(0)
            self.clearPageWidgets(page)
            stacked_widget.removeWidget(page)
            page.deleteLater()

    def clearPageWidgets(self, page):
        layout = page.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearPageWidgets(item.layout())

    def clearGroupbox(self):
        while self.ui.gb_tagSwitch.layout().count():
            item = self.ui.gb_tagSwitch.layout().takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        
    def newTagSet(self):
        self.checkCreate = dialog_confirm.Confirm(title="Checking...", msg="Create new tag set?")
        if self.checkCreate.exec():
            self.create = dialog_createTagSet.CreateTagSet()
            if self.create.exec():
                self.createModeOn()
                self.unsaved = self.create.le_name.text()
                # generate models for editing
                self.create.generateModel()
                
                # set the model for the menu of QComboBox (cb_recTagSet)
                self.model_cb_02.selections.append(f"{self.create.le_name.text()}(Unsaved)")
                self.model_cb_02.layoutChanged.emit()
                
                # set the QComboBox display the temporary name of the new tag set
                for idx, item in enumerate(self.model_cb_02.selections):
                    if item == f"{self.create.le_name.text()}(Unsaved)":
                        self.ui.cb_recTagSet.setCurrentIndex(idx)
                        break
                    
                self.btnSet = self.groupBoxButtonSetting(self.create.dfs)
                
                # Clear the layout of gb_tagSwitch
                self.clearGroupbox()
                
                # Add the widget to gb_tagSwitch
                self.ui.gb_tagSwitch.layout().addWidget(self.btnSet)
                
                self.tagDisp = self.stackedWidgetSetting(self.create.dfs)
                
                # Clear the layout of sw_tags
                self.clearStackedWidget(self.ui.sw_tags)
                
                # Set the tag display for each configuration
                self.tagDisp = self.stackedWidgetSetting(self.create.dfs)
                self.stackedTabWidgets = self.tagDisp[0]
                self.stackedModels = self.tagDisp[1]
                self.stackedSelectionModels = self.tagDisp[2]
                
            else:
                self.createModeOff()
                print("Creation Cancelled!")
            
        else:
            print("Creation Cancelled!")
    
    def discard(self):
        self.createModeOff()
        self.clearStackedWidget(self.ui.sw_tags)
        self.clearGroupbox()
        self.reloadMenuList()
    
    def saveTagSet(self):
        if self.ui.sw_tags.widget(0) is not None:
            self.saveCheck = dialog_confirm.Confirm(title="Checking...", msg="Save current tag set?")
            if self.saveCheck.exec():
                toBeSavedTagSet = {}
                for model in self.stackedModels:
                    toBeSavedTagSet[f"Config_{self.stackedModels.index(model)}"] = model._data.to_dict()
                
                if not self.createModeSave:
                    self.unsaved = ""
                
                self.saveDialog = dialog_saveTagSet.SaveTagSet(os.path.join(BASE_DIR,"models"), self.unsaved, toBeSavedTagSet)
                
                if self.createModeSave:
                    # No need to ask for the filename
                    self.saveDialog.savefileMode2()
                    self.createModeOff()
                else:
                    self.saveDialog.savefileMode1()
                    
                self.reloadMenuList()
                for idx, item in enumerate(self.model_cb_02.selections):
                    if item == self.saveDialog.filename:
                        self.ui.cb_recTagSet.setCurrentIndex(idx)
                        break
            else:
                print("Save Cancelled!")
        else:
            print("Please create or load a tag set first!")
    
    def deleteTagSet(self):
        filename = self.model_cb_02.selections[self.ui.cb_recTagSet.currentIndex()]
        self.deleteCheck = dialog_confirm.Confirm(title="Checking...", msg="Delete current tag set?")
        
        if self.deleteCheck.exec():
            os.remove(os.path.join(BASE_DIR,"models","tagSet_{}.json".format(filename)))
            self.reloadMenuList()
            self.clearGroupbox()
            self.clearStackedWidget(self.ui.sw_tags)
            self.ui.btn_deleteTagSet.setEnabled(False)
        else:
            print("Delete Cancelled!")
    
    def moveUp(self):
        if hasattr(self, "stackedSelectionModels"):
            page = self.ui.sw_tags.currentIndex()
            if self.stackedSelectionModels[page].hasSelection():
                idx = self.stackedSelectionModels[page].currentIndex()
                rowNumber = idx.row()
                if (rowNumber-1>=0):
                    self.stackedModels[page].moveRows(rowNumber, rowNumber - 1)
                    new_index = self.stackedModels[page].index(rowNumber-1, idx.column())
                    self.stackedSelectionModels[page].setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
            else:
                print("No selected row")
            
        else:
            print("Please load a tag set first!")
            
    def moveDown(self):
        if hasattr(self, "stackedSelectionModels"):
            page = self.ui.sw_tags.currentIndex()
            if self.stackedSelectionModels[page].hasSelection():
                idx = self.stackedSelectionModels[page].currentIndex()
                rowNumber = idx.row()
                if (rowNumber+1 < self.stackedModels[page].rowCount(QModelIndex())):
                    self.stackedModels[page].moveRows(rowNumber, rowNumber + 2)
                    new_index = self.stackedModels[page].index(rowNumber+1, idx.column())
                    self.stackedSelectionModels[page].setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
            else:
                print("No selected row")
            
        else:
            print("Please load a tag set first!")
    
    def insert(self):
        if hasattr(self, "stackedSelectionModels"):
            page = self.ui.sw_tags.currentIndex()
            if self.stackedSelectionModels[page].hasSelection():
                idx = self.stackedSelectionModels[page].currentIndex()
                rowNumber = idx.row()
                self.w = dialog_insertProperties.InsertProp()
                if self.w.exec() == QDialog.Accepted:
                    print("Insert data:", self.w.addData)
                    self.stackedModels[page].addRows(QModelIndex(), rowNumber, self.w.addData)
                    new_index = self.stackedModels[page].index(rowNumber + self.w.addData.shape[0], self.w.addData.shape[1]-1)
                    self.stackedSelectionModels[page].setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
                else:
                    print("Cancel Insertion!")
            else:
                rowNumber = self.stackedModels[page].rowCount(QModelIndex())-1
                self.w = dialog_insertProperties.InsertProp()
                if self.w.exec() == QDialog.Accepted:
                    print("Insert data:", self.w.addData)
                    self.stackedModels[page].addRows(QModelIndex(), rowNumber+2, self.w.addData)
                    new_index = self.stackedModels[page].index(rowNumber + self.w.addData.shape[0], self.w.addData.shape[1]-1)
                    self.stackedSelectionModels[page].setCurrentIndex(new_index, QItemSelectionModel.ClearAndSelect)
                else:
                    print("Cancel Insertion!")
        else:
            print("Please load a tag set first!")
    
    def rm(self):
        if hasattr(self, "stackedSelectionModels"):
            page = self.ui.sw_tags.currentIndex()
            if self.stackedSelectionModels[page].hasSelection():
                selected_indexes = self.stackedSelectionModels[page].selectedIndexes()
                rows = sorted(set(index.row() for index in selected_indexes), reverse=True)
                for row in rows:
                    self.stackedModels[page].rmRows(QModelIndex(), row, 1)
            else:
                print("No selected row")
        else:
            print("Please load a tag set first!")
    
    def convert(self):
        self.clearTag()
        if hasattr(self, "stackedModels"):
            page = self.ui.sw_tags.currentIndex()
            rowNames = self.stackedModels[page]._data.index.tolist()
            values = [val[0] for val in self.stackedModels[page]._data.values]
            for prop, val in zip(rowNames, values):
                self.ui.te_clipboard.append(f"{prop}: {val}")
            self.plus()
        else:
            print("Please load a tag set first!")
    
    def plus(self):
        latest_value = (self.ui.le_serialName.text().split("-")[1].split(".")[0])
        self.Serial = int(latest_value)
        if self.Serial < 9999:
            self.Serial += 1
            self.ui.le_serialName.setText(f"{self.date.strftime(DATE_FORMAT)}-{self.Serial:04d}.tif")
        elif self.Serial == 9999:
            self.Serial = 0
            self.ui.le_serialName.setText(f"{self.date.strftime(DATE_FORMAT)}-{self.Serial:04d}.tif")
            
    def minus(self):
        latest_value = (self.ui.le_serialName.text().split("-")[1].split(".")[0])
        self.Serial = int(latest_value)
        if self.Serial > 0:
            self.Serial -= 1
            self.ui.le_serialName.setText(f"{self.date.strftime(DATE_FORMAT)}-{self.Serial:04d}.tif")
        elif self.Serial == 0:
            self.Serial = 0
            self.ui.le_serialName.setText(f"{self.date.strftime(DATE_FORMAT)}-{self.Serial:04d}.tif")
    
    def resetSerial(self):
        self.Serial = 0
        self.ui.le_serialName.setText(f"{self.date.strftime(DATE_FORMAT)}-{self.Serial:04d}.tif")
    
    def copySerial(self):
        QApplication.clipboard().setText(self.ui.le_serialName.text())
    
    def copyTag(self):
        QApplication.clipboard().setText(self.ui.te_clipboard.toPlainText())
    
    def clearTag(self):
        self.ui.te_clipboard.clear()
        QApplication.clipboard().clear()