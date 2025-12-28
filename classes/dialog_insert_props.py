import pandas as pd
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QDialog,
    QSizePolicy,
    QApplication
)

class DialogInsertProps(QDialog):
    """A class for creating an inputing window for QTableView"""
    def __init__(self, parent=None, propertyNum=1, valueNum=1):
        super().__init__(parent)
        self.layout_main = QVBoxLayout()
        self.layout_values = QVBoxLayout()
        self.layout_inputting = QHBoxLayout()
        self.layout_properties = QVBoxLayout()
        
        
        self.lbl_properties = QLabel("Property Names")
        self.layout_properties.addWidget(self.lbl_properties)
        self.lbl_values = QLabel("VALUE")
        self.layout_values.addWidget(self.lbl_values)
        
        self.lbl_properties.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.lbl_values.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        
        self.properties = [f"Property {i:02d}" for i in range(propertyNum)]
        self.values = [f"Value {i:02d}" for i in range(valueNum)]
                
        
        self.lineEdit_properties = []
        for item in self.properties:
            lineEdit_prop = QLineEdit()
            lineEdit_prop.setPlaceholderText(item)
            self.layout_properties.addWidget(lineEdit_prop)
            self.lineEdit_properties.append(lineEdit_prop)
        
        
        
        self.lineEdit_values = []
        for item in self.values:
            lineEdit_val = QLineEdit()
            lineEdit_val.setPlaceholderText(item)
            self.layout_values.addWidget(lineEdit_val)
            self.lineEdit_values.append(lineEdit_val)
        
        self.layout_inputting.addLayout(self.layout_properties)
        self.layout_inputting.addLayout(self.layout_values)
        self.layout_main.addLayout(self.layout_inputting)
        
        # Add a button for adding a row
        self.btn_add_row = QPushButton("Add Row")
        self.btn_add_row.clicked.connect(self.add_row)
        
        # Add a button for removing a row
        self.btn_rm_row = QPushButton("Remove Row")
        self.btn_rm_row.clicked.connect(self.rm_row)
        
        # Add a OK button
        self.btn_ok = QPushButton("OK")
        self.btn_ok.clicked.connect(self.ok)
        
        # Add a Cancel button
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.clicked.connect(self.cancel)
        
        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.addWidget(self.btn_add_row)
        self.layout_buttons.addWidget(self.btn_rm_row)
        self.layout_buttons.addWidget(self.btn_ok)
        self.layout_buttons.addWidget(self.btn_cancel)
        self.layout_main.addLayout(self.layout_buttons)
        
        self.setup_uis()
        self.setLayout(self.layout_main)
        
    def add_row(self):
        # Add a new row to the bottom
        lineEdit_prop = QLineEdit()
        current_row_number = len(self.properties)
        newRowName = f"Property {current_row_number:02d}"
        self.properties.append(newRowName)            
        lineEdit_prop.setPlaceholderText(newRowName)
        self.lineEdit_properties.append(lineEdit_prop)
        self.layout_properties.addWidget(lineEdit_prop)
        
        # Add a set of values of a new row
        lineEdit_val = QLineEdit()
        newValueName = f"Value {current_row_number:02d}"
        self.values.append(newValueName)
        lineEdit_val.setPlaceholderText(newValueName)
        self.lineEdit_values.append(lineEdit_val)
        self.layout_values.addWidget(lineEdit_val)
        self.adjustSize()
        self.btn_ok.setDefault(True)
        
    def rm_row(self):
        if len(self.properties) > 1:
            # Disable updates to prevent flickering
            self.setUpdatesEnabled(False)
            
            # Remove the last property QLineEdit widget
            self.properties.pop()
            self.layout_properties.removeWidget(self.lineEdit_properties[-1])
            self.lineEdit_properties[-1].deleteLater()
            self.lineEdit_properties.pop()
            
            # Remove the last set of value QLineEdit widgets
            self.values.pop()
            self.layout_values.removeWidget(self.lineEdit_values[-1])
            self.lineEdit_values[-1].deleteLater()
            self.lineEdit_values.pop()
            
            # Force layout update
            self.layout_properties.invalidate()
            self.layout_values.invalidate()
            
            # Process events to ensure widgets are properly removed
            QApplication.processEvents()
            
            # Now adjust the size
            self.adjustSize()
            
            # Re-enable updates
            self.setUpdatesEnabled(True)
            
            self.btn_ok.setDefault(True)
                    
    def ok(self):
        # Get the input data
        self.toBeAddProperties = []
        self.toBeAddValues = []
        texts_prop = [lineEdit.text() for lineEdit in self.lineEdit_properties]
        texts_val = [lineEdit.text() for lineEdit in self.lineEdit_values]
        for prop, val in zip(texts_prop, texts_val):
            if prop != "":
                self.toBeAddProperties.append(prop)
                self.toBeAddValues.append(val)
        
        columnNames = ["VALUE_0"]
        self.dataToBeAdded = pd.DataFrame(self.toBeAddValues, columns=columnNames, index=self.toBeAddProperties)
        
        self.accept()
    
    def cancel(self):
        self.reject()
        
    def setup_uis(self):
        min_width = 400
        max_width = 800
    
        width_01 = self.size().width()
        height_01 = 50
        
        size_01 = QSize(int(width_01/2), height_01)
        self.setMinimumWidth(min_width)
        self.setMaximumWidth(max_width)
            
        self.lbl_properties.setMaximumSize(size_01)
        self.lbl_values.setMaximumSize(size_01)
        
        self.lbl_properties.setStyleSheet("font-weight: bold;")
        self.lbl_values.setStyleSheet("font-weight: bold;")

        self.btn_ok.setDefault(True)
