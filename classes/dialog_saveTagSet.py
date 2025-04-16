import os
import json
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit
from classes.dialog_confirm import Confirm

class SaveTagSet(QDialog):
    def __init__(self, path, filename, data_to_be_saved):
        super().__init__()
        self.path = path
        self.caption = "Saving File"
        self.filename = filename
        self.data_to_be_saved = data_to_be_saved
        
    def savefileMode1(self):
        print("Save Mode: Normal")
        self.setWindowTitle(self.caption)
        self.layout = QVBoxLayout()
        self.buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(self.buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.message = QLabel("Please input the filename: ")
        self.le_filename = QLineEdit()
        self.le_filename.setMaxLength(30)
        self.le_filename.setPlaceholderText('Enter your filename here.')
        self.le_filename.returnPressed.connect(self.accept)
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.le_filename)
        self.layout.addWidget(self.buttonBox)
        self.message.setStyleSheet("font-size: 14px;")
        self.message.setFixedSize(QSize(200, 50))
        self.message.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)
        
        if self.exec():
            self.filename = self.le_filename.text()
            filePath = os.path.join(self.path, 'tagSet_' + self.filename +'.json')
            print("File Path: ", filePath)
            if os.path.isfile(filePath):
                overwriteCheck = Confirm(title="Warning", msg="Warning! Tag set name is exist, continue overwritting?")
                if overwriteCheck.exec():
                    with open(filePath, 'w') as f:
                        json.dump(self.data_to_be_saved, f, indent=4)
                    
                    print("Original file overwritten!")
                else:
                    print("File saving cancelled!")
            else:
                with open(filePath, 'w') as f:
                    json.dump(self.data_to_be_saved, f, indent=4)
                print("File saved!")
        else:
            print("File saving cancelled!")


    def savefileMode2(self):
        print("Save Mode: Create")
        filePath = os.path.join(self.path, 'tagSet_' + self.filename +'.json')
        if os.path.isfile(filePath):
            self.overwriteCheck = Confirm(title="Warning", msg="Warning! Tag set name is exist, continue overwritting?")
            if self.overwriteCheck.exec():
                with open(filePath, 'w') as f:
                    json.dump(self.data_to_be_saved, f, indent=4)
                    
                print("Original file overwritten!")
            else:
                print("File saving cancelled!")
        else:
            with open(filePath, 'w') as f:
                json.dump(self.data_to_be_saved, f, indent=4)
            print("File saved!")
        
