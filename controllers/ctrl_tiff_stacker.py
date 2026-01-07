## Modules
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor
from rich import print

from classes import DialogGetPath, DirWatcher, ModelCheckableList, ThreadTiffStacker


class CtrlTiffStacker:
    def __init__(self, ui):
        self.ui = ui
        self.model_tiffFileList = ModelCheckableList(name="model_tiffFileList")
        self.ui.lv_tiffFiles.setModel(self.model_tiffFileList)

        self.ui.chk_selectAllFiles.setVisible(False)

        # Set up DirWatcher for monitoring TIFF files
        self.tiff_watcher = DirWatcher(filetype=".tif", target_cb=None)
        self.watching_dir = None
        self.tiff_file_map = {}  # Maps display name -> (full_path, parent_dir)

        self.connect_signals()

    def connect_signals(self):
        self.ui.btn_browseTiffs.clicked.connect(self.browse_tiffs)
        self.ui.chk_selectAllFiles.stateChanged.connect(self.select_all_files)
        self.model_tiffFileList.allSelectedCheck.connect(self.check_all_selected)
        self.ui.btn_startConcat.clicked.connect(self.start_concat)
        self.tiff_watcher.fileListScanned.connect(self.update_tiff_list)

    def browse_tiffs(self):
        dlg_get_inputDir = DialogGetPath(title="Please select the folder contains .rec and .tif files")
        self.input_dir = Path(dlg_get_inputDir.get_path())

        if str(self.input_dir) == ".":
            self.ui.tb_stacker.append("<span style='color: white;'>[MESSAGE] No directory is selected</span>")
            self.ui.tb_stacker.moveCursor(QTextCursor.End)
            print("[yellow]No directory selected[/yellow]")
            return

        # Set up directory watcher
        self.watching_dir = str(self.input_dir)
        self.tiff_watcher.set_watched_dir(self.watching_dir)

        self.ui.gb_tiffBrowser.setTitle(str(self.input_dir))
        self.ui.tb_stacker.append(
            f"<span style='color: lime;'>[INFO] Directory selected: {str(self.input_dir)}</span>"
        )
        self.ui.tb_stacker.moveCursor(QTextCursor.End)
        print(f"[cyan]Watching TIFF directory: {self.watching_dir}[/cyan]")

    def update_tiff_list(self, filenames):
        """Called when DirWatcher detects changes in the TIFF directory"""
        if self.ui.chk_includeSubDir.isChecked():
            list_of_tiffs = sorted(Path(self.watching_dir).rglob("*.tif"))
        else:
            list_of_tiffs = [Path(self.watching_dir) / name for name in filenames]

        # Filter discrete tiffs and track their directory info
        self.tiff_file_map = {}  # Maps display name -> (full_path, parent_dir)
        base_path = Path(self.watching_dir)

        for item in list_of_tiffs:
            if "@0001" not in item.name:
                continue

            filename = item.name.replace("@0001", "")
            parent = item.parent

            # Determine directory label
            if parent == base_path:
                dir_label = "(Root)"
            else:
                # Get relative path from base to parent
                rel_path = parent.relative_to(base_path)
                dir_label = f"({rel_path})"

            display_name = f"{filename} {dir_label}"
            self.tiff_file_map[display_name] = (str(item.with_name(filename)), str(parent))

        if not self.tiff_file_map:
            self.ui.tb_stacker.append(
                "<span style='color: red;'>[ERROR] No discrete .tif files found in the selected directory</span>"
            )
            self.ui.tb_stacker.moveCursor(QTextCursor.End)
            self.ui.chk_selectAllFiles.setVisible(False)
            self.ui.chk_selectAllFiles.setChecked(False)
            self.model_tiffFileList.set_tiff_list([], False)
            print("[yellow]No discrete TIFF files found[/yellow]")
            return

        self.ui.chk_selectAllFiles.setVisible(True)

        all_is_checked = self.ui.chk_selectAllFiles.checkState() == Qt.Checked
        self.model_tiffFileList.set_tiff_list(list(self.tiff_file_map.keys()), all_is_checked)
        print(f"[green]Found {len(self.tiff_file_map)} discrete TIFF file(s)[/green]")

    def select_all_files(self):
        """Select or deselect all files in the list view."""
        self.model_tiffFileList.set_all_checked(self.ui.chk_selectAllFiles.isChecked())

    def check_all_selected(self, are_all_selected):
        self.ui.chk_selectAllFiles.blockSignals(True)
        self.ui.chk_selectAllFiles.setChecked(are_all_selected)
        self.ui.chk_selectAllFiles.blockSignals(False)

    def start_concat(self):
        """Use a class to handle the concatenation process in a separate thread to avoid freezing main program."""
        checked_display_names = self.model_tiffFileList.get_checked()
        if checked_display_names == []:
            self.ui.tb_stacker.append(
                "<span style='color: yellow;'>[WARNING] No files selected for concatenation</span>"
            )
            self.ui.tb_stacker.moveCursor(QTextCursor.End)
            print("[yellow]No files selected for concatenation[/yellow]")
            return

        # Group files by their parent directory
        files_by_dir = {}
        for display_name in checked_display_names:
            if display_name in self.tiff_file_map:
                full_path, parent_dir = self.tiff_file_map[display_name]
                if parent_dir not in files_by_dir:
                    files_by_dir[parent_dir] = []
                files_by_dir[parent_dir].append(full_path)

        # Disable the start button while processing
        self.ui.btn_startConcat.setEnabled(False)
        self.ui.pb_concatenation.setValue(0)
        self.ui.tb_stacker.append("<span style='color: lime;'>[INFO] Starting concatenation process...</span>")
        self.ui.tb_stacker.moveCursor(QTextCursor.End)
        total_files = sum(len(files) for files in files_by_dir.values())
        print(f"[cyan]Starting concatenation of {total_files} file(s) in {len(files_by_dir)} director(ies)...[/cyan]")

        # Create and set up the worker thread with directory grouping
        self.concatenator_thread = ThreadTiffStacker(files_by_dir, str(self.input_dir))
        self.concatenator_thread.progress_update.connect(self.update_concatenation_progress)
        self.concatenator_thread.finished.connect(self.on_concatenation_finished)
        self.concatenator_thread.progress_percentage.connect(self.ui.pb_concatenation.setValue)
        # Start the thread
        # use start() instead of run(), because run() is a built-in method of QThread
        self.concatenator_thread.start()

    def update_concatenation_progress(self, message, color):
        self.ui.tb_stacker.append(f"<span style='color: {color};'>{'&nbsp;' * 7}{message}</span>")
        self.ui.tb_stacker.moveCursor(QTextCursor.End)

    def on_concatenation_finished(self):
        self.ui.tb_stacker.append("<span style='color: lime;'>[INFO] Concatenation process completed!</span>")
        self.ui.tb_stacker.moveCursor(QTextCursor.End)
        self.ui.btn_startConcat.setEnabled(True)
        print("[green]Concatenation process completed![/green]")
