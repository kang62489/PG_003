import os
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QLineEdit
from .dialog_confirm import DialogConfirm
from rich import print

class DialogSaveTemplate(QDialog):
    """A class for build a dialog for saving template"""
    def __init__(self, caption="Saving..."):
        super().__init__()
        self.setWindowTitle(caption)
        self.buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(self.buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        self.lbl_message = QLabel("Please input the filename: ")
        
        self.lineEdit_filename = QLineEdit()
        self.lineEdit_filename.setMaxLength(30)
        self.lineEdit_filename.setPlaceholderText('Enter your filename here.')
        self.lineEdit_filename.returnPressed.connect(self.accept)
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_message)
        self.layout.addWidget(self.lineEdit_filename)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        
        # Set input validator
        regex = QRegularExpression(r"patch_default|puff_default")
        self.validator  = QRegularExpressionValidator(regex)
        self.lineEdit_filename.textChanged.connect(self.validate_input)
                
    def validate_input(self, text):
        self.lineEdit_filename.setValidator(self.validator)
        if self.lineEdit_filename.hasAcceptableInput():
            print("[bold red]Input filename is not acceptable[/bold red]")
            self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            self.lineEdit_filename.setValidator(None)
            return
        
        self.lineEdit_filename.setValidator(None)
        self.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)

    def savefile(self, path, currentTemplate):
        filePath = os.path.join(path, 'template_' + self.lineEdit_filename.text() +'.json')
        if not os.path.isfile(filePath):
            currentTemplate.to_json(filePath, orient='columns', indent=4)
            print("[bold green]Template Saved!![/bold green]")
            return
            
        self.dlg_overwriteCheck = DialogConfirm(title="Warning", msg="Warning! Template name is exist, continue overwritting?")
        proceedOverwriteWithSameName = self.dlg_overwriteCheck.exec()
        if proceedOverwriteWithSameName:
            currentTemplate.to_json(filePath, orient='columns', indent=4)
            print("[bold green]Original file overwritten![/bold green]")
            return
        
        proceedOverwriteWithNameChanged = self.exec()
        if not proceedOverwriteWithNameChanged:
            print("[yellow]File saving cancelled![/yellow]")
            return
        
        return self.savefile(path, currentTemplate)