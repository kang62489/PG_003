## Modules
# Standard library imports
from pathlib import Path

# Third-party imports
from PySide6.QtCore import QFileSystemWatcher, Signal
from rich import print


class DirWatcher(QFileSystemWatcher):
    """A class to watch a directory for specific filetype changes and update a target combobox"""

    # Custom signal to indicate file list renewal
    filelistRenewed = Signal()

    def __init__(self, filetype=".rec", target_cb=None):
        super().__init__()
        self.filetype = filetype
        self.target_cb = target_cb
        self.directoryChanged.connect(self.scan_filetype)

    def set_watched_dir(self, dir_path):
        if self.directories():
            self.removePaths(self.directories())

        self.addPath(dir_path)
        self.scan_filetype()

    def scan_filetype(self):
        """Scan the watched directory for files of the specified filetype and update the target combobox"""
        if self.target_cb is None:
            print("[bold red]No target combobox assigned to DirWatcher[/bold red]")
            return

        # Remember current selection and file list before clearing
        current_selection = self.target_cb.currentText()
        old_files = set(
            self.target_cb.itemText(i)
            for i in range(self.target_cb.count())
            if not self.target_cb.itemText(i).startswith("--")
        )

        # clear target combobox
        self.target_cb.clear()

        if not self.directories():
            print("[bold red]No directory is being watched by DirWatcher[/bold red]")
            return

        watched_dir = Path(self.directories()[0])
        if watched_dir.exists() is False:
            self.target_cb.addItem("-- Input directory does not exist --")
            return

        filtered_filenames = sorted([path.name for path in list(watched_dir.glob(f"*{self.filetype}"))])

        if not filtered_filenames:
            self.target_cb.addItem(f"-- No {self.filetype.replace('.', '').upper()}s in current dir --")
        else:
            self.target_cb.addItems(filtered_filenames)

            # Check for new files
            new_files = set(filtered_filenames) - old_files

            if new_files:
                # Select the newest added file (last one alphabetically among new files)
                newest_file = sorted(new_files)[-1]
                index = self.target_cb.findText(newest_file)
                self.target_cb.setCurrentIndex(index)
            elif current_selection and not current_selection.startswith("--"):
                # Restore previous selection if it still exists
                index = self.target_cb.findText(current_selection)
                if index >= 0:
                    self.target_cb.setCurrentIndex(index)
                else:
                    self.target_cb.setCurrentIndex(len(filtered_filenames) - 1)
            else:
                # Default to last file
                self.target_cb.setCurrentIndex(len(filtered_filenames) - 1)

            # Emit signal indicating file list has been renewed
            self.filelistRenewed.emit()
