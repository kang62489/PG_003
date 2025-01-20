## Author: Kang
## Last Update: 2025-Jan-20
## Usage: A class for creating an inputing window for QTableView

import pandas as pd
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QDialog
)

class AddProp(QDialog):
    def __init__(self, parent=None, propertyNum=1, valueNum=2):
        super().__init__(parent)
        self.layout_main = QVBoxLayout()
        self.layout_values = QVBoxLayout()
        self.layout_inputting = QHBoxLayout()
        self.layout_properties = QVBoxLayout()
        
        
        self.label_properties = QLabel("Property Names")
        self.layout_properties.addWidget(self.label_properties)
        self.label_values = QLabel("Values")
        self.layout_values.addWidget(self.label_values)
        
        
        self.properties = [f"Property {i:02d}" for i in range(propertyNum)]
        self.values = [f"Value {i:02d}" for i in range(valueNum)]
                
        
        self.lineEdit_properties = []
        for item in self.properties:
            lineEdit_prop = QLineEdit()
            lineEdit_prop.setPlaceholderText(item)
            self.layout_properties.addWidget(lineEdit_prop)
            self.lineEdit_properties.append(lineEdit_prop)
        
        
        
        self.layoutSet_values = []
        for row in range(propertyNum):
            layout_vals = QHBoxLayout()
            for item in self.values:
                lineEdit_val = QLineEdit()
                lineEdit_val.setPlaceholderText(item)
                layout_vals.addWidget(lineEdit_val)
            
            self.layoutSet_values.append(layout_vals)
            self.layout_values.addLayout(layout_vals)
        
        self.layout_inputting.addLayout(self.layout_properties)
        self.layout_inputting.addLayout(self.layout_values)
        self.layout_main.addLayout(self.layout_inputting)
        
        # Add a button for adding a row
        self.btn_addRow = QPushButton("Add Row")
        self.btn_addRow.clicked.connect(self.addRow)
        
        # Add a button for removing a row
        self.btn_removeRow = QPushButton("Remove Row")
        self.btn_removeRow.clicked.connect(self.removeRow)
        
        # Add a button for adding a column
        self.btn_addCol = QPushButton("Add Column")
        self.btn_addCol.clicked.connect(self.addCol)
        
        # Add a button for removing a column
        self.btn_removeCol = QPushButton("Remove Column")
        self.btn_removeCol.clicked.connect(self.removeCol)
        
        # Add a OK button
        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.ok)
        
        # Add a Cancel button
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.cancel)
        
        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.addWidget(self.btn_addRow)
        self.layout_buttons.addWidget(self.btn_removeRow)
        self.layout_buttons.addWidget(self.btn_addCol)
        self.layout_buttons.addWidget(self.btn_removeCol)
        self.layout_buttons.addWidget(self.btn_ok)
        self.layout_buttons.addWidget(self.btn_cancel)
        self.layout_main.addLayout(self.layout_buttons)
        
        self.setUI()
        self.setLayout(self.layout_main)
        
    def addRow(self):
        # Add the property of a new row
        lineEdit_prop = QLineEdit()
        rowNum = len(self.properties)
        newRowName = f"Property {rowNum:02d}"
        self.properties.append(newRowName)            
        lineEdit_prop.setPlaceholderText(newRowName)
        self.lineEdit_properties.append(lineEdit_prop)
        self.layout_properties.addWidget(lineEdit_prop)
        
        # Add a set of values of a new row
        layout_vals = QHBoxLayout()
        for idx, item in enumerate(self.values):
            lineEdit_val = QLineEdit()
            lineEdit_val.setPlaceholderText(item)
            layout_vals.addWidget(lineEdit_val)
        self.layoutSet_values.append(layout_vals)
        self.layout_values.addLayout(layout_vals)
    
    def removeRow(self):
        if len(self.properties) > 1:
            # Remove the last property QLineEdit widget
            self.properties.pop()
            self.layout_properties.removeWidget(self.lineEdit_properties[-1])
            self.lineEdit_properties[-1].deleteLater()
            self.lineEdit_properties.pop()
            
            # Remove the last set of value QLineEdit widgets
            last_valueSet = self.layoutSet_values.pop()
            while last_valueSet.count():
                item = last_valueSet.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            self.layout_values.removeItem(last_valueSet)
            
            self.adjustSize()
    
    def addCol(self):
        # Add a new value column
        colNum = len(self.values)
        newColName = f"Value {colNum:02d}"
        self.values.append(newColName)
        
        for set in self.layoutSet_values:
            lineEdit_val = QLineEdit()
            lineEdit_val.setPlaceholderText(newColName)
            set.addWidget(lineEdit_val)
        
        self.adjustSize()
            
    def removeCol(self):
        if len(self.values) > 1:
            # Remove the last value column
            self.values.pop()
            for layout_value_set in self.layoutSet_values:
                layout_value_set.itemAt(layout_value_set.count()-1).widget().deleteLater()
    
    def ok(self):
        # Get the inputted data
        self.addProperties = []
        self.addValueSets = []
        for idx, lineEdit in enumerate(self.lineEdit_properties):
            if lineEdit.text() != "":
                self.addProperties.append(lineEdit.text())
                self.addValueSets.append([self.layoutSet_values[idx].itemAt(i).widget().text() for i in range(self.layoutSet_values[idx].count())])
        
        columnNames = [f"Value_{i}" for i in range(len(self.values))]
        self.addData = pd.DataFrame(self.addValueSets, columns=columnNames, index=self.addProperties)
        
        self.accept()
    
    def cancel(self):
        self.reject()
        
    def setUI(self):
        min_width = 800
        max_width = 1500
    
        width_01 = self.size().width()
        height_01 = 50
        
        size_01 = QSize(int(width_01/2), height_01)
        self.setMinimumWidth(min_width)
        self.setMaximumWidth(max_width)
            
        self.label_properties.setMaximumSize(size_01)
        self.label_values.setMaximumSize(size_01)
        
        self.label_properties.setStyleSheet("font-weight: bold;")
        self.label_values.setStyleSheet("font-weight: bold;")

