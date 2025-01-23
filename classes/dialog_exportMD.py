## Author: Kang
## Last Update: 2025-Jan-23
## Usage: To produce a markdown format of experimental conditions for obsidian

## Modules
import os
from datetime import datetime
from PySide6.QtWidgets import QFileDialog

class ExportMD(QFileDialog):
    def __init__(self, dataframe, caption='Please choose a directory to generate a metadata common_terms file'):
        super().__init__()
        self.setWindowTitle(caption)
        self.setFileMode(QFileDialog.FileMode.Directory)

        if self.exec():
            self.dir_output = self.selectedFiles()[0]
            props = dataframe.index.tolist()
            values = [[item for item in value if item != ""] for value in dataframe.values]
            if "Date of Recording" in props:
                dateStr = dataframe.loc["Date of Recording"][0]
                prefix = datetime.strptime(dateStr, '%Y-%m-%d').strftime('%Y_%m_%d')
            else:
                prefix = datetime.today().strftime('%Y_%m_%d')
            
            with open(os.path.join(self.dir_output, prefix + '_expInfo.md'), 'w', encoding="utf-8") as f:
                f.write("---\n")
                for prop, value in zip(props, values):
                    line = prop + ": " + ", ".join(value)
                    f.write(line)
                    f.write("\n")
                f.write("---\n")
        else:
            print("Export cancelled!")



