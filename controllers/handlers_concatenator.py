## Modules
import os, glob
import tifffile
from pathlib import Path
from rich import print
from classes import (
    model_list_2,
    dialog_getPath
    )
from PySide6.QtCore import Qt

class ConcatenatorHandlers:
    def __init__(self, ui):
        self.ui = ui
        self.model_recFileList = model_list_2.ListModel(name="model_recFileList")
        self.ui.listView_recFiles.setModel(self.model_recFileList)
        
        self.ui.checkBox_selectAllFiles.setVisible(False)
        
        self.connect_signals()
        
    def connect_signals(self):
        self.ui.btn_browse_tiffs.clicked.connect(self.browse_tiffs)
        self.ui.checkBox_selectAllFiles.stateChanged.connect(self.selectAllFiles)
        self.model_recFileList.allSelectedCheck.connect(self.check_all_selected)
        
    def browse_tiffs(self):
        dlg_get_inputDir = dialog_getPath.GetPath(title="Please select the folder contains .rec and .tif files")
        input_dir = dlg_get_inputDir.get_path()
        if input_dir == "":
            self.ui.textBrowser_concatenator.append("<span style='color: white;'>[MESSAGE] No directory is selected</span>")
            return
        
        list_of_tiffs = sorted(glob.glob(input_dir + '/*.tif'))
        list_of_discrete_tiffs = [item.split("@")[0] for item in list_of_tiffs if "@0001" in item]
        
        if list_of_discrete_tiffs == []:
            self.ui.textBrowser_concatenator.append("<span style='color: red;'>[ERROR] No discrete .tif files found in the selected directory</span>")
            self.ui.checkBox_selectAllFiles.setVisible(False)
            self.ui.checkBox_selectAllFiles.setChecked(False)
            self.model_recFileList.loadFileList([], False)
            return
        
        self.ui.checkBox_selectAllFiles.setVisible(True)
        self.ui.checkBox_selectAllFiles.setChecked(True)
        
        all_is_checked = self.ui.checkBox_selectAllFiles.checkState()==Qt.Checked
        self.model_recFileList.loadFileList(list_of_discrete_tiffs, all_is_checked)
        self.ui.lbl_tiffDir.setText(input_dir)
        self.ui.textBrowser_concatenator.append(f"<span style='color: lime;'>[INFO] Directory selected: {input_dir}</span>")
    
    def selectAllFiles(self):
        """Select or deselect all files in the list view."""
        self.model_recFileList.setAllChecked(self.ui.checkBox_selectAllFiles.isChecked())
        
    def check_all_selected(self, are_all_selected):
        self.ui.checkBox_selectAllFiles.blockSignals(True)
        self.ui.checkBox_selectAllFiles.setChecked(are_all_selected)
        self.ui.checkBox_selectAllFiles.blockSignals(False)