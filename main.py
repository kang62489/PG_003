## Author: Kang
## Last Update: 2025-Jan-22
## Usage: A gui interface for generating metadata tag which will be pasted to each recording file (.rec)

## Modules
import os
import sys
import json
from datetime import datetime
from pathlib import Path
import glob
from rich import print
import pandas as pd
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import Qt, QSize , QRegularExpression
from PySide6.QtCore import QModelIndex, QItemSelectionModel
from PySide6.QtWidgets import (
    QApplication,
    QAbstractItemView,
    QDialog,
    QSizePolicy,
    QHeaderView
)
from PySide6.QtUiTools import QUiLoader

# Import customized modules
from classes import (
    customized_delegate,
    dialog_addProperties,
    dialog_confirm,
    dialog_createTagSet,
    dialog_exportMD,
    dialog_insertProperties,
    dialog_saveTagSet,
    dialog_saveTemplate,
    model_comboBox,
    model_table_1,
    model_table_2,
    widget_buttonSet,
    widget_tagDisplay
)

loader = QUiLoader()
basedir = os.path.dirname(__file__)
qssdir = Path(__file__).parent / "styles"
modeldir = Path(__file__).parent / "models"

class MainPanel:
    def __init__(self):
        super().__init__()
        self.ui = loader.load(os.path.join(basedir, "ui/metadata_generator.ui"), None)
        self.ui.setWindowTitle("Metadata Generator")
        self.ui.show()
        with open(qssdir / "styles.qss", "r") as f:
            self.ui.setStyleSheet(f.read())
        
        # Set Models
        self.setModels()
        self.setButtons()
        
        # Set attributes of UIs
        self.setAttrs()

        # List object names of tab_0, tab_1
        self.tab0_objs = self.list_objs(self.ui.tab_0)
        self.tab1_objs = self.list_objs(self.ui.tab_1)
        
        # Set default tag set saving mode
        self.createModeSave = False
        
## Functions for initialization
    def list_objs(self, parent_widget):
        return [child.objectName() for child in parent_widget.children()]
    
    def setButtons(self):
        ## Tab_0
        self.ui.btn_loadTemplate.clicked.connect(self.loadTemplate)
        self.ui.btn_saveTemplate.clicked.connect(self.saveTemplate)
        self.ui.btn_deleteCurrentTemplate.clicked.connect(self.deleteTemplate)
        self.ui.btn_exportExpInfo.clicked.connect(self.exportExpInfo)
        self.ui.btn_addNewRows.clicked.connect(self.addNewRows)
        self.ui.btn_removeSelectedRows.clicked.connect(self.removeSelectedRows)
        self.ui.btn_moveUp.clicked.connect(self.moveRowUp)
        self.ui.btn_moveDown.clicked.connect(self.moveRowDown)
        
        ## Tab_1
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
    
    def setAttrs(self):
    ## Set default tab index
        self.ui.tab_main.setCurrentIndex(0)
    ## Set spaces
        ## Tab_0
        self.ui.verticalLayout_7.setSpacing(5)
        self.ui.verticalLayout_11.setSpacing(5)
        
        self.ui.verticalLayout_7.insertSpacing(2, 200)
        self.ui.verticalLayout_11.insertSpacing(0, 300)
        
    ## Set attributes of buttons
        # Sizes
        size_btn_01 = QSize(180, 80)
        size_btn_02 = QSize(100, 80)
        size_btn_03 = QSize(80, 40)
        size_btn_04 = QSize(60, 30)
        size_btn_05 = QSize(125, 40)
        
        size_lbl_01 = QSize(180, 40)
        size_lbl_02 = QSize(200, 40)
        
        size_cb_01 = QSize(180, 40)
        size_cb_02 = QSize(200, 40)
        
        # Tab_0
        self.ui.btn_loadTemplate.setFixedSize(size_btn_01)
        self.ui.btn_saveTemplate.setFixedSize(size_btn_01)
        self.ui.btn_deleteCurrentTemplate.setFixedSize(size_btn_01)
        self.ui.btn_exportExpInfo.setFixedSize(size_btn_01)
        self.ui.btn_addNewRows.setFixedSize(size_btn_01)
        self.ui.btn_removeSelectedRows.setFixedSize(size_btn_01)
        self.ui.btn_moveUp.setFixedSize(size_btn_01)
        self.ui.btn_moveDown.setFixedSize(size_btn_01)
        
        # button status
        self.ui.btn_deleteCurrentTemplate.setEnabled(False)
        
        ## Tab_1
        self.ui.btn_up.setFixedSize(size_btn_02)
        self.ui.btn_down.setFixedSize(size_btn_02)
        self.ui.btn_insert.setFixedSize(size_btn_02)
        self.ui.btn_rm.setFixedSize(size_btn_02)
        self.ui.btn_convert.setFixedSize(size_btn_02)
        
        self.ui.btn_loadTagSet.setFixedSize(size_btn_03)
        self.ui.btn_newTagSet.setFixedSize(size_btn_03)
        self.ui.btn_discard.setFixedSize(size_btn_03)
        self.ui.btn_saveTagSet.setFixedSize(size_btn_03)
        self.ui.btn_deleteTagSet.setFixedSize(size_btn_03)
        
        self.ui.btn_plus.setFixedSize(size_btn_04)
        self.ui.btn_minus.setFixedSize(size_btn_04)
        self.ui.btn_resetSerial.setFixedSize(size_btn_04)
        self.ui.btn_copySerial.setFixedSize(size_btn_04)
        self.ui.btn_copyTag.setFixedSize(size_btn_05)
        self.ui.btn_clearTag.setFixedSize(size_btn_05)
        
        # button status
        self.ui.btn_deleteTagSet.setEnabled(False)
        self.ui.btn_discard.setVisible(False)
        
        
    # Set attributes of QComboBox (cb_expInfo)
        #Tab_0
        self.ui.cb_expInfo.setFixedSize(size_cb_01)
        
        #Tab_1
        self.ui.cb_recTagSet.setFixedSize(size_cb_02)
        
        # comboBox alignment
        center_aligment = customized_delegate.CenterAlignDelegate()
        self.ui.cb_recTagSet.setItemDelegate(center_aligment)
        
    # Set attributes of QLabel (lbl_expInfo)
        #Tab_0
        self.ui.lbl_expInfo.setFixedSize(size_lbl_01)
        
        #label alignment
        self.ui.lbl_expInfo.setAlignment(Qt.AlignCenter)
        
        #Tab_1
        self.ui.lbl_DOR.setFixedSize(size_lbl_02)
        self.ui.lbl_date.setFixedSize(size_lbl_02)
        
        #label alignment
        self.ui.lbl_date.setAlignment(Qt.AlignCenter)
        
        #label text
        self.date = datetime.today()
        self.ui.lbl_date.setText(f"{self.date.strftime('%Y-%m-%d')}")
        
    # Set the attributes of QTableView
        #Tab_0
        # table alignment
        self.ui.tv_expInfo.verticalHeader().setDefaultAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # table display settings
        self.ui.tv_expInfo.horizontalHeader().setVisible(False)
        self.ui.tv_expInfo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tv_expInfo.verticalHeader().setDefaultSectionSize(50)
        self.ui.tv_expInfo.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.ui.tv_expInfo.setItemDelegate(customized_delegate.CellEditDelegate())
        
    # Set the attributes of QGroupBox
        # gruopbox title
        self.ui.gb_tagSwitch.setTitle("Button Switches")
        
        # groupbox width
        self.ui.gb_tagSwitch.setFixedWidth(150)
        
    # Set the attributes of lineEdit
        self.ui.le_serialName.setFixedHeight(60)
        self.ui.le_serialName.setAlignment(Qt.AlignCenter)
        
        regex = QRegularExpression(r"^\d{8}-\d{4}\.tif$")
        self.validator = QRegularExpressionValidator(regex)
        self.ui.le_serialName.setValidator(self.validator)
        self.ui.le_serialName.setPlaceholderText("YYYYMMDD-0000")
        self.ui.le_serialName.textChanged.connect(self.validate_serial)
        self.ui.le_serialName.setValidator(None)
        
        self.serial = 0
        self.ui.le_serialName.setText(f"{self.date.strftime('%Y%m%d')}-{self.serial:04d}.tif")
    # Set the attributes of status bar
        self.ui.statusbar.showMessage("Metadata Generator 1.1.2, Author: Kang, Last Update: 2025-Jan-23, Made in OIST")
    
    def setModels(self):
        # Set the model displays in QTableView (tv_expInfo)
        self.model_tv_01 = model_table_1.TableModel()
        self.ui.tv_expInfo.setModel(self.model_tv_01)
        self.sm_expInfo = self.ui.tv_expInfo.selectionModel()
        
        # Set the model for the menu of QComboBox (cb_expInfo, cb_recTagSet)
        self.model_cb_01 = model_comboBox.SelectorModel()
        self.model_cb_02 = model_comboBox.SelectorModel()
        self.loadMenuList()
        self.ui.cb_expInfo.setModel(self.model_cb_01)
        self.ui.cb_recTagSet.setModel(self.model_cb_02)
        
    def loadMenuList(self):
        with open(modeldir / "cb_list_01.json", "r") as f:
            saved_cb_list_01= json.load(f)
        pass
        
        with open(modeldir / "cb_list_02.json", "r") as f:
            saved_cb_list_02= json.load(f)
        pass
    
        templateFiles = [os.path.basename(i) for i in glob.glob(os.path.join(basedir,"models",'template_*.json'))]
        templateList = [Path(tempName.replace("template_","")).stem for tempName in templateFiles]
        
        tagSetFiles = [os.path.basename(i) for i in glob.glob(os.path.join(basedir,"models",'tagSet_*.json'))]
        tagSetList = [Path(tempName.replace("tagSet_","")).stem for tempName in tagSetFiles]
        
        if saved_cb_list_01 != templateList:
            with open(modeldir / "cb_list_01.json", "w") as f:
                json.dump(templateList, f)
                self.model_cb_01.selections=templateList
        else:
            self.model_cb_01.selections = saved_cb_list_01
    
        if saved_cb_list_02 != tagSetList:
            with open(modeldir / "cb_list_02.json", "w") as f:
                json.dump(tagSetList, f)
                self.model_cb_02.selections=tagSetList
        else:
            self.model_cb_02.selections = saved_cb_list_02
            
    def reloadMenuList(self):
        # cb_01
        templateFiles = [os.path.basename(i) for i in glob.glob(os.path.join(basedir,"models",'template_*.json'))]
        templateList = [Path(tempName.replace("template_","")).stem for tempName in templateFiles]
        with open(modeldir / "cb_list_01.json", "w") as f:
            json.dump(templateList, f)
        
        self.model_cb_01.updateList(templateList)
        self.model_cb_01.layoutChanged.emit()
        
        #cb_02
        tagSetFiles = [os.path.basename(i) for i in glob.glob(os.path.join(basedir,"models",'tagSet_*.json'))]
        tagSetList = [Path(tempName.replace("tagSet_","")).stem for tempName in tagSetFiles]
        with open(modeldir / "cb_list_02.json", "w") as f:
            json.dump(tagSetList, f)
        
        self.model_cb_02.updateList(tagSetList)
        self.model_cb_02.layoutChanged.emit()

## Functions for buttons in Tab_0    
    def loadTemplate(self):
        filename = self.model_cb_01.selections[self.ui.cb_expInfo.currentIndex()]
        if filename == "default":
            self.ui.btn_deleteCurrentTemplate.setEnabled(False)
        else:
            self.ui.btn_deleteCurrentTemplate.setEnabled(True)
        
        with open(modeldir / "template_{}.json".format(filename), "r") as f:
            template = pd.read_json(f, dtype=str)
        pass
                 
        self.model_tv_01.update(template)
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

## Functions for buttons in Tab_1
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
            tagDisp.tv_tag.setEditTriggers(QAbstractItemView.DoubleClicked)
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
            
        with open(modeldir / "tagSet_{}.json".format(filename), "r") as f:
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
                
                self.saveDialog = dialog_saveTagSet.SaveTagSet(os.path.join(basedir,"models"), self.unsaved, toBeSavedTagSet)
                
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
            os.remove(os.path.join(basedir,"models","tagSet_{}.json".format(filename)))
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
        else:
            print("Please load a tag set first!")
    
    def plus(self):
        latest_value = (self.ui.le_serialName.text().split("-")[1].split(".")[0])
        self.Serial = int(latest_value)
        if self.Serial < 9999:
            self.Serial += 1
            self.ui.le_serialName.setText(f"{self.date.strftime('%Y%m%d')}-{self.Serial:04d}.tif")
        elif self.Serial == 9999:
            self.Serial = 0
            self.ui.le_serialName.setText(f"{self.date.strftime('%Y%m%d')}-{self.Serial:04d}.tif")
            
    def minus(self):
        latest_value = (self.ui.le_serialName.text().split("-")[1].split(".")[0])
        self.Serial = int(latest_value)
        if self.Serial > 0:
            self.Serial -= 1
            self.ui.le_serialName.setText(f"{self.date.strftime('%Y%m%d')}-{self.Serial:04d}.tif")
        elif self.Serial == 0:
            self.Serial = 0
            self.ui.le_serialName.setText(f"{self.date.strftime('%Y%m%d')}-{self.Serial:04d}.tif")
    
    def resetSerial(self):
        self.Serial = 0
        self.ui.le_serialName.setText(f"{self.date.strftime('%Y%m%d')}-{self.Serial:04d}.tif")
    
    def validate_serial(self):
        self.ui.le_serialName.setValidator(self.validator)
        if self.ui.le_serialName.hasAcceptableInput():
            self.ui.le_serialName.setStyleSheet("QLineEdit { color: green; }")
            self.ui.btn_copySerial.setEnabled(True)
            self.ui.le_serialName.setValidator(None)
        else:
            self.ui.le_serialName.setStyleSheet("QLineEdit { color: red; }")
            self.ui.btn_copySerial.setEnabled(False)
            self.ui.le_serialName.setValidator(None)
    
    def copySerial(self):
        QApplication.clipboard().setText(self.ui.le_serialName.text())
    
    def copyTag(self):
        QApplication.clipboard().setText(self.ui.te_clipboard.toPlainText())
    
    def clearTag(self):
        self.ui.te_clipboard.clear()
        QApplication.clipboard().clear()
    
app = QApplication(sys.argv)
window = MainPanel()


app.exec()

if __name__ == "__main__":
    pass
