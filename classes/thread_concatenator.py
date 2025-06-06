import os, tifftools
from pathlib import Path
from time import time
from PySide6.QtCore import QThread, Signal

class ConcatenatorThread(QThread):
    """Thread to concatenate TIFF files in the background."""
    progress_update = Signal(str, str)  # message, color
    # finished is a built-in signal for QThread that is emitted when the thread finishes execution
    # No need to customize it explicitly (finished = Signal())
    
    def __init__(self, files_to_process, main_dir):
        super().__init__()
        self.files_to_process = files_to_process
        self.main_dir = main_dir

    def run(self):
        t_start = time()
        if not os.path.exists('merged'):
            os.makedirs('merged')
        
        for file in self.files_to_process:
            self.progress_update.emit(f"{file}", "deepskyblue")

        length_horizontal_line = len(self.files_to_process[-1])+1
        self.progress_update.emit("-"*length_horizontal_line, "white")
        
        for n, file in enumerate(self.files_to_process):
            img_dir = Path(file).parent
            img_basename = Path(file).stem
            components = sorted(img_dir.glob(f"{img_basename}@*.tif"))
            
            self.progress_update.emit(f"Processing {img_basename} [{n+1}/{len(self.files_to_process)}]", "aquamarine")
            all = [file] + components
            try:
                tifftools.tiff_concat(all, f"{self.main_dir}/merged/m_{img_basename}.tif", overwrite=True)
                
                elapse = time() - t_start
                self.progress_update.emit(f"Concatenated {img_basename} in {elapse:.2f} seconds<br>", "aqua")
            except Exception as e:
                self.progress_update.emit(f"Error processing {img_basename}: {e}", "red")
