## Modules
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

from classes import DialogGetPath, ModelCheckableList, ThreadTiffStacker


class CtrlTiffStacker:
    def __init__(self, ui):
        self.ui = ui
        self.model_recFileList = ModelCheckableList(name="model_recFileList")
        self.ui.listView_recFiles.setModel(self.model_recFileList)

        self.ui.checkBox_selectAllFiles.setVisible(False)

        self.connect_signals()

    def connect_signals(self):
        self.ui.btn_browse_tiffs.clicked.connect(self.browse_tiffs)
        self.ui.checkBox_selectAllFiles.stateChanged.connect(self.selectAllFiles)
        self.model_recFileList.allSelectedCheck.connect(self.check_all_selected)
        self.ui.btn_start_concatenation.clicked.connect(self.start_concatenation)

    def browse_tiffs(self):
        dlg_get_inputDir = DialogGetPath(
            title="Please select the folder contains .rec and .tif files"
        )
        self.input_dir = Path(dlg_get_inputDir.get_path())

        if str(self.input_dir) == ".":
            self.ui.textBrowser_concatenator.append(
                "<span style='color: white;'>[MESSAGE] No directory is selected</span>"
            )
            self.ui.textBrowser_concatenator.moveCursor(QTextCursor.End)
            return

        if self.ui.checkBox_includeSubfolders.isChecked():
            list_of_tiffs = sorted(self.input_dir.rglob("*.tif"))
        else:
            list_of_tiffs = sorted(self.input_dir.glob("*.tif"))

        list_of_discrete_tiffs = [
            str(item).replace("@0001", "")
            for item in list_of_tiffs
            if "@0001" in item.name
        ]
        if list_of_discrete_tiffs == []:
            self.ui.textBrowser_concatenator.append(
                "<span style='color: red;'>[ERROR] No discrete .tif files found in the selected directory</span>"
            )
            self.ui.textBrowser_concatenator.moveCursor(QTextCursor.End)
            self.ui.checkBox_selectAllFiles.setVisible(False)
            self.ui.checkBox_selectAllFiles.setChecked(False)
            self.model_recFileList.loadFileList([], False)
            return

        self.ui.checkBox_selectAllFiles.setVisible(True)
        self.ui.checkBox_selectAllFiles.setChecked(True)

        all_is_checked = self.ui.checkBox_selectAllFiles.checkState() == Qt.Checked
        self.model_recFileList.loadFileList(list_of_discrete_tiffs, all_is_checked)
        self.ui.groupBox_tiffBrowser.setTitle(str(self.input_dir))
        self.ui.textBrowser_concatenator.append(
            f"<span style='color: lime;'>[INFO] Directory selected: {str(self.input_dir)}</span>"
        )
        self.ui.textBrowser_concatenator.moveCursor(QTextCursor.End)

    def selectAllFiles(self):
        """Select or deselect all files in the list view."""
        self.model_recFileList.setAllChecked(
            self.ui.checkBox_selectAllFiles.isChecked()
        )

    def check_all_selected(self, are_all_selected):
        self.ui.checkBox_selectAllFiles.blockSignals(True)
        self.ui.checkBox_selectAllFiles.setChecked(are_all_selected)
        self.ui.checkBox_selectAllFiles.blockSignals(False)

    def start_concatenation(self):
        """Use a class to handle the concatenation process in a separate thread to avoid freezing main program."""
        to_be_concatenated = self.model_recFileList.getCheckedItems()
        if to_be_concatenated == []:
            self.ui.textBrowser_concatenator.append(
                "<span style='color: yellow;'>[WARNING] No files selected for concatenation</span>"
            )
            self.ui.textBrowser_concatenator.moveCursor(QTextCursor.End)
            return

        # Disable the start button while processing
        self.ui.btn_start_concatenation.setEnabled(False)
        self.ui.textBrowser_concatenator.append(
            "<span style='color: lime;'>[INFO] Starting concatenation process...</span>"
        )
        self.ui.textBrowser_concatenator.moveCursor(QTextCursor.End)

        # Create and set up the worker thread
        self.concatenator_thread = ThreadTiffStacker(
            to_be_concatenated, str(self.input_dir)
        )
        self.concatenator_thread.progress_update.connect(
            self.update_concatenation_progress
        )
        self.concatenator_thread.finished.connect(self.on_concatenation_finished)
        self.concatenator_thread.progress_percentage.connect(
            self.ui.progressBar_concatenation.setValue
        )
        # Start the thread
        # use start() instead of run(), because run() is a built-in method of QThread
        self.concatenator_thread.start()

    def update_concatenation_progress(self, message, color):
        self.ui.textBrowser_concatenator.append(
            f"<span style='color: {color};'>{'&nbsp;' * 7}{message}</span>"
        )
        self.ui.textBrowser_concatenator.moveCursor(QTextCursor.End)

    def on_concatenation_finished(self):
        self.ui.textBrowser_concatenator.append(
            "<span style='color: lime;'>[INFO] Concatenation process completed!</span>"
        )
        self.ui.textBrowser_concatenator.moveCursor(QTextCursor.End)
        self.ui.btn_start_concatenation.setEnabled(True)
