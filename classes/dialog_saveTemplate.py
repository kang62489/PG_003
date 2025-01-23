## Author: Kang
## Last Update: 2025-Jan-23
## Usage: A class for build a dialog to open directory and save the file

import os
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit
from classes.dialog_confirm import Confirm

class SaveTemplate(QDialog):
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
        self.filename.returnPressed.connect(self.accept)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.filename)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
    def savefile(self, path, currentTemplate):
        if self.exec():
            filePath = os.path.join(path, 'template_' + self.filename.text() +'.json')
            if os.path.isfile(filePath):
                self.overwriteCheck = Confirm(title="Warning", msg="Warning! Template name is exist, continue overwritting?")
                if self.overwriteCheck.exec():
                    currentTemplate.to_json(filePath, orient='columns', indent=4)
                else:
                    print("File saving cancelled!")
            else:
                currentTemplate.to_json(filePath, orient='columns', indent=4)
            
            print("Template Saved!!")
        else:
            print("File saving cancelled!")