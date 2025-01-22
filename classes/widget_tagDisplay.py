## Author: Kang
## Last Update: 2025-Jan-22
## Usage: A class for make a widget that can be put in the container (QStackedWidget: sw_tags)
from PySide6.QtCore import Qt 
from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QTableView,
    QWidget
)

class TagDisp(QWidget):
    def __init__(self, page=0):
        super().__init__()
        self.layout_main = QVBoxLayout()
        
        self.lbl_page = QLabel(f"Configuration {page}")
        self.lbl_page.setAlignment(Qt.AlignCenter)
        self.lbl_page.setStyleSheet("font-size: 20px; font-weight: bold;color: green;")
        self.tv_tag = QTableView()
        
        self.layout_main.addWidget(self.lbl_page)
        self.layout_main.addWidget(self.tv_tag)
        self.setLayout(self.layout_main)