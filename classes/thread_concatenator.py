import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import time

import tifftools
from PySide6.QtCore import QThread, Signal


class ConcatenatorThread(QThread):
    """Thread to concatenate TIFF files in the background."""

    progress_update = Signal(str, str)  # message, color
    # finished is a built-in signal for QThread that is emitted when the thread finishes execution
    # No need to customize it explicitly (finished = Signal())
    progress_percentage = Signal(int)

    def __init__(self, files_to_process, main_dir, max_workers=2):
        super().__init__()
        self.files_to_process = files_to_process
        self.main_dir = main_dir
        self.max_workers = max_workers
        self.processed_count = 0
        self.total_count = len(files_to_process)

    def concatenate_process(self, file):
        img_dir = Path(file).parent
        img_basename = Path(file).stem
        components = sorted(img_dir.glob(f"{img_basename}@*.tif"))

        all_files = [file] + components
        output_path = f"{self.main_dir}/merged/m_{img_basename}.tif"
        original_stat = os.stat(file)
        try:
            t_start = time()

            # Use tifftools with IFDs extend approach
            combined_ifds = []
            for file_path in all_files:
                tiff_data = tifftools.read_tiff(str(file_path))
                combined_ifds.extend(tiff_data["ifds"])

            # Write combined IFDs to output file
            tifftools.write_tiff(combined_ifds, output_path)

            elaspse = time() - t_start
            os.utime(output_path, (original_stat.st_atime, original_stat.st_mtime))
            self.progress_update.emit(
                f"{img_basename} is concatenated. Time used: {elaspse:.2f} seconds.",
                "aquamarine",
            )

        except Exception as e:
            self.progress_update.emit(f"Error processing {img_basename}: {e}", "red")

        # Update progress
        self.processed_count += 1
        self.progress_percentage.emit(
            int(self.processed_count / self.total_count * 100)
        )

    def run(self):
        if not os.path.exists(os.path.join(self.main_dir, "merged")):
            os.makedirs(os.path.join(self.main_dir, "merged"))

        for file in self.files_to_process:
            self.progress_update.emit(f"{file}", "deepskyblue")

        length_horizontal_line = len(self.files_to_process[-1]) + 1
        self.progress_update.emit("-" * length_horizontal_line, "white")
        self.progress_update.emit(
            f"Total files to concatenate: {self.total_count}", "white"
        )

        # Process files in parallel
        t_start = time()

        # Process all files at once with ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self.concatenate_process, self.files_to_process)

        t_end = time() - t_start
        self.progress_update.emit(
            f"All concatenation completed in {t_end:.2f} seconds<br>", "aqua"
        )
