## Author: Kang
## Last Update: 2025-Jan-22
## Usage: A class for build a dialog to create a new tag set

from logging.handlers import QueueHandler
import pandas as pd
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QLineEdit
)

class CreateTagSet(QDialog):
    def __init__(self, caption="New Tag Set"):
        super().__init__()
        self.setWindowTitle(caption)
        
        self.buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(self.buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.message = QLabel("Please input the name of the set: ")
        self.lbl_name = QLabel("Name: ")
        self.le_name = QLineEdit("new_0")
        self.le_name.setMaxLength(30)
        
        self.lbl_numOfConfigs = QLabel("Number of Configurations: ")
        self.le_NOC = QLineEdit()
        self.le_NOC.setPlaceholderText("Input the number of configurations")
        self.le_NOC.setText("1")
        validator = QIntValidator(1, 10, self)
        self.le_NOC.setValidator(validator)
        
        self.layout_main = QVBoxLayout()
        self.layout_name = QHBoxLayout()
        self.layout_numOfConfigs = QHBoxLayout()
        
        self.layout_main.addWidget(self.message)
        self.layout_name.addWidget(self.lbl_name)
        self.layout_name.addWidget(self.le_name)
        self.layout_numOfConfigs.addWidget(self.lbl_numOfConfigs)
        self.layout_numOfConfigs.addWidget(self.le_NOC)
        self.layout_main.addLayout(self.layout_name)
        self.layout_main.addLayout(self.layout_numOfConfigs)
        self.layout_main.addWidget(self.buttonBox)
        self.setLayout(self.layout_main)
        
    def generateModel(self):
        rowNames = [
            "OBJ",
            "EXC",
            "LEVEL",
            "EMI",
            "SLICE",
            "SAMPLE",
            "FRAMES",
            "FPS",
            "CAM.TRIG.MODE"
        ]
        
        columnNames = ["VALUE"]
        values = [""]*len(rowNames)
        
        self.N = int(self.le_NOC.text())
        self.dfs = {}
        for i in range(self.N):
            df = pd.DataFrame({columnNames[0]: values}, index=rowNames)
            self.dfs[f"Config_{i}"] = df.to_dict(orient="dict")