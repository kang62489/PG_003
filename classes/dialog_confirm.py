## Author: Kang
## Last Update: 2025-Jan-20
## Usage: A class for build a dialog for confimation

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QLineEdit, QVBoxLayout


class Confirm(QDialog):
    def __init__(self, title="Dialog", msg="Question"):
        super().__init__()
        self.setWindowTitle(title)

        self.message = QLabel(msg)

        self.buttons = QDialogButtonBox.Yes | QDialogButtonBox.No
        self.buttonBox = QDialogButtonBox(self.buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.buttonBox, 0, Qt.AlignCenter)
        self.setLayout(self.layout)


class ConfirmWithPasscode(QDialog):
    def __init__(self, title="Dialog", msg="Question", passcode="kang"):
        super().__init__()
        self.setWindowTitle(title)
        self.correct_passcode = passcode

        self.message = QLabel(msg)
        self.passcode_label = QLabel("Enter passcode to confirm:")
        self.passcode_input = QLineEdit()
        self.passcode_input.setEchoMode(QLineEdit.Password)

        self.buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(self.buttons)
        self.buttonBox.accepted.connect(self.check_passcode)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.message)
        self.layout.addWidget(self.passcode_label)
        self.layout.addWidget(self.passcode_input)
        self.layout.addWidget(self.buttonBox, 0, Qt.AlignCenter)
        self.setLayout(self.layout)

    def check_passcode(self):
        if self.passcode_input.text() == self.correct_passcode:
            self.accept()
        else:
            self.passcode_label.setText("❌ Wrong passcode! Try again:")
            self.passcode_input.clear()
