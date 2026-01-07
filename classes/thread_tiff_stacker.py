## Modules
# Standard library imports
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import time

# Third-party imports
import numpy as np
import tifffile
from PySide6.QtCore import QThread, Signal


class ThreadTiffStacker(QThread):
    """Thread to concatenate TIFF files in the background."""

    progress_update = Signal(str, str)  # message, color
    # finished is a built-in signal for QThread that is emitted when the thread finishes execution
    # No need to customize it explicitly (finished = Signal())
    progress_percentage = Signal(int)

    def __init__(self, files_to_process, main_dir, max_workers=2):
        super().__init__()
        # files_to_process can be either a list (old behavior) or dict (grouped by directory)
        if isinstance(files_to_process, dict):
            self.files_by_dir = files_to_process
            self.files_to_process = []
            for files in files_to_process.values():
                self.files_to_process.extend(files)
        else:
            # Old behavior: all files in main_dir
            self.files_by_dir = {main_dir: files_to_process}
            self.files_to_process = files_to_process

        self.main_dir = main_dir
        self.max_workers = max_workers
        self.processed_count = 0
        self.total_count = len(self.files_to_process)

    def concatenate_process(self, file):
        img_dir = Path(file).parent
        img_basename = Path(file).stem
        components = sorted(img_dir.glob(f"{img_basename}@*.tif"))

        all_files = [file] + components
        # Create merged folder in the file's parent directory
        merged_dir = img_dir / "merged"
        output_path = merged_dir / f"m_{img_basename}.tif"
        original_stat = os.stat(file)
        try:
            t_start = time()

            # Use faster approach - read full files and append
            # metadata=None prevents writing incorrect frame count from first fragment
            for i, tiff_file in enumerate(all_files):
                data = tifffile.imread(tiff_file)
                # First file creates, rest append
                if i == 0:
                    stacked_data = data
                else:
                    stacked_data = np.concatenate((stacked_data, data), axis=0)

            tifffile.imwrite(str(output_path), stacked_data, metadata=None, imagej=True)
            del data, stacked_data

            elaspse = time() - t_start
            os.utime(str(output_path), (original_stat.st_atime, original_stat.st_mtime))
            self.progress_update.emit(
                f"{img_basename} is concatenated. Time used: {elaspse:.2f} seconds.",
                "aquamarine",
            )

        except Exception as e:
            self.progress_update.emit(f"Error processing {img_basename}: {e}", "red")

        # Update progress
        self.processed_count += 1
        self.progress_percentage.emit(int(self.processed_count / self.total_count * 100))

    def run(self):
        # Create merged folders for each directory
        from rich import print
        for parent_dir in self.files_by_dir.keys():
            merged_path = Path(parent_dir) / "merged"
            if not merged_path.exists():
                merged_path.mkdir(parents=True, exist_ok=True)
                print(f"[cyan]Created merged folder: {merged_path}[/cyan]")

        for file in self.files_to_process:
            self.progress_update.emit(f"{Path(file).name}", "deepskyblue")

        length_horizontal_line = max(len(Path(f).name) for f in self.files_to_process) + 1
        self.progress_update.emit("-" * length_horizontal_line, "white")
        self.progress_update.emit(f"Total files to concatenate: {self.total_count}", "white")

        # Process files in parallel
        t_start = time()

        # Process all files at once with ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self.concatenate_process, self.files_to_process)

        t_end = time() - t_start
        self.progress_update.emit(f"All concatenation completed in {t_end:.2f} seconds<br>", "aqua")
