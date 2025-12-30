## Modules
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor

from classes import DialogGetPath, ModelCheckableList, ThreadTiffStacker


class CtrlTiffStacker:
    def __init__(self, ui):
        self.ui = ui
        self.model_recFileList = ModelCheckableList(name="model_recFileList")
        self.ui.lv_recFiles.setModel(self.model_recFileList)

        self.ui.chk_selectAllFiles.setVisible(False)

        self.connect_signals()

    def connect_signals(self):
        self.ui.btn_BrowseTiffs.clicked.connect(self.browse_tiffs)
        self.ui.chk_selectAllFiles.stateChanged.connect(self.select_all_files)
        self.model_recFileList.allSelectedCheck.connect(self.check_all_selected)
        self.ui.btn_StartConcat.clicked.connect(self.start_concat)

    def browse_tiffs(self):
        dlg_get_inputDir = DialogGetPath(title="Please select the folder contains .rec and .tif files")
        self.input_dir = Path(dlg_get_inputDir.get_path())

        if str(self.input_dir) == ".":
            self.ui.tb_concatenator.append("<span style='color: white;'>[MESSAGE] No directory is selected</span>")
            self.ui.tb_concatenator.moveCursor(QTextCursor.End)
            return

        if self.ui.chk_includeSubfolders.isChecked():
            list_of_tiffs = sorted(self.input_dir.rglob("*.tif"))
        else:
            list_of_tiffs = sorted(self.input_dir.glob("*.tif"))

        list_of_discrete_tiffs = [str(item).replace("@0001", "") for item in list_of_tiffs if "@0001" in item.name]
        if list_of_discrete_tiffs == []:
            self.ui.tb_concatenator.append(
                "<span style='color: red;'>[ERROR] No discrete .tif files found in the selected directory</span>"
            )
            self.ui.tb_concatenator.moveCursor(QTextCursor.End)
            self.ui.chk_selectAllFiles.setVisible(False)
            self.ui.chk_selectAllFiles.setChecked(False)
            self.model_recFileList.set_tiff_list([], False)
            return

        self.ui.chk_selectAllFiles.setVisible(True)
        self.ui.chk_selectAllFiles.setChecked(True)

        all_is_checked = self.ui.chk_selectAllFiles.checkState() == Qt.Checked
        self.model_recFileList.set_tiff_list(list_of_discrete_tiffs, all_is_checked)
        self.ui.gb_tiffBrowser.setTitle(str(self.input_dir))
        self.ui.tb_concatenator.append(
            f"<span style='color: lime;'>[INFO] Directory selected: {str(self.input_dir)}</span>"
        )
        self.ui.tb_concatenator.moveCursor(QTextCursor.End)

    def select_all_files(self):
        """Select or deselect all files in the list view."""
        self.model_recFileList.set_all_checked(self.ui.chk_selectAllFiles.isChecked())

    def check_all_selected(self, are_all_selected):
        self.ui.chk_selectAllFiles.blockSignals(True)
        self.ui.chk_selectAllFiles.setChecked(are_all_selected)
        self.ui.chk_selectAllFiles.blockSignals(False)

    def start_concat(self):
        """Use a class to handle the concatenation process in a separate thread to avoid freezing main program."""
        to_be_concatenated = self.model_recFileList.get_checked()
        if to_be_concatenated == []:
            self.ui.tb_concatenator.append(
                "<span style='color: yellow;'>[WARNING] No files selected for concatenation</span>"
            )
            self.ui.tb_concatenator.moveCursor(QTextCursor.End)
            return

        # Disable the start button while processing
        self.ui.btn_StartConcat.setEnabled(False)
        self.ui.tb_concatenator.append("<span style='color: lime;'>[INFO] Starting concatenation process...</span>")
        self.ui.tb_concatenator.moveCursor(QTextCursor.End)

        # Create and set up the worker thread
        self.concatenator_thread = ThreadTiffStacker(to_be_concatenated, str(self.input_dir))
        self.concatenator_thread.progress_update.connect(self.update_concatenation_progress)
        self.concatenator_thread.finished.connect(self.on_concatenation_finished)
        self.concatenator_thread.progress_percentage.connect(self.ui.pb_concatenation.setValue)
        # Start the thread
        # use start() instead of run(), because run() is a built-in method of QThread
        self.concatenator_thread.start()

    def update_concatenation_progress(self, message, color):
        self.ui.tb_concatenator.append(f"<span style='color: {color};'>{'&nbsp;' * 7}{message}</span>")
        self.ui.tb_concatenator.moveCursor(QTextCursor.End)

    def on_concatenation_finished(self):
        self.ui.tb_concatenator.append("<span style='color: lime;'>[INFO] Concatenation process completed!</span>")
        self.ui.tb_concatenator.moveCursor(QTextCursor.End)
        self.ui.btn_StartConcat.setEnabled(True)
