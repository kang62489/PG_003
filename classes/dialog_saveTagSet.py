## Author: Kang
## Last Update: 2025-Jan-22
## Usage: A class for build a dialog to open directory and save the file

import os
import json
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit
from classes.dialog_confirm import Confirm

class SaveTagSet(QDialog):
    def __init__(self, caption="Saving..."):
        super().__init__()
        self.setWindowTitle(caption)
        
        self.buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(self.buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.message = QLabel("Please input the filename: ")
        
        self.filename = QLineEdit()
        self.filename.setMaxLength(30)
        self.filename.setPlaceholderText('Enter your filename here.')
        self.filename.returnPressed.connect(self.savefile)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.filename)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
    def savefile(self, path, currentTagSet):
        if self.exec():
            filePath = os.path.join(path, 'tagSet_' + self.filename.text() +'.json')
            if os.path.isfile(filePath):
                self.overwriteCheck = Confirm(title="Warning", msg="Warning! Tag set name is exist, continue overwritting?")
                if self.overwriteCheck.exec():
                    with open(filePath, 'w') as f:
                        json.dump(currentTagSet, f, indent=4)
                else:
                    print("File saving cancelled!")
            else:
                with open(filePath, 'w') as f:
                    json.dump(currentTagSet, f, indent=4)
            
            print("Tag set saved!!")
        else:
            print("File saving cancelled!")