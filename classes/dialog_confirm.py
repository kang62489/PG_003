## Author: Kang
## Last Update: 2025-Jan-20
## Usage: A class for build a dialog for confimation

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QLineEdit, QVBoxLayout


class DialogConfirm(QDialog):
    def __init__(self, title="Dialog", msg="Question"):
        super().__init__()
        self.setWindowTitle(title)

        self.lbl_message = QLabel(msg)

        self.buttons = QDialogButtonBox.Yes | QDialogButtonBox.No
        self.buttonBox = QDialogButtonBox(self.buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_message)
        self.layout.addWidget(self.buttonBox, 0, Qt.AlignCenter)
        self.setLayout(self.layout)


class DialogConfirmPasscode(QDialog):
    def __init__(self, title="Dialog", msg="Question", passcode="kang"):
        super().__init__()
        self.setWindowTitle(title)
        self.correct_passcode = passcode

        self.lbl_message = QLabel(msg)
        self.lbl_passcode = QLabel("Enter passcode to confirm:")
        self.le_passcode = QLineEdit()
        self.le_passcode.setEchoMode(QLineEdit.Password)

        self.buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(self.buttons)
        self.buttonBox.accepted.connect(self.check_passcode)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.lbl_message)
        self.layout.addWidget(self.lbl_passcode)
        self.layout.addWidget(self.le_passcode)
        self.layout.addWidget(self.buttonBox, 0, Qt.AlignCenter)
        self.setLayout(self.layout)

    def check_passcode(self):
        if self.le_passcode.text() == self.correct_passcode:
            self.accept()
        else:
            self.lbl_passcode.setText("❌ Wrong passcode! Try again:")
            self.le_passcode.clear()
