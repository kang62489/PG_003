## Author: Kang
## Last Update: 2025-Jan-22
## Usage: A class for make a widget that can be put in the container (QGroupBox: gb_tagSwitch)

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QWidget,
)

class ButtonSet(QWidget):
    def __init__(self, numOfConfigs=3, direction="horizontal", buttonPrefix="Config_"):
        super().__init__()
        if direction == "horizontal":
            self.layout_main = QHBoxLayout()
            self.layout_main.setAlignment(Qt.AlignVCenter)
        else:
            self.layout_main = QVBoxLayout()
            self.layout_main.setAlignment(Qt.AlignHCenter)
        
        self.N = numOfConfigs
        self.prefix = buttonPrefix
        self.setButtons()
        self.setLayout(self.layout_main)
    
    def setButtons(self):
        self.btnSwitches = []
        for i in range(self.N):
            btn = QPushButton(f"{self.prefix}{i}")
            btn.setMaximumSize(QSize(200, 30))
            self.btnSwitches.append(btn)
            self.layout_main.addWidget(btn)