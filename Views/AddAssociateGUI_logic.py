from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QDialogButtonBox, QLabel, QMessageBox
from PyQt6 import uic
from PyQt6.QtGui import QIntValidator
from PyQt6 import QtCore, QtGui, QtWidgets


# Dialog to add a new associate.
class AddAssociateDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set title of the window
        self.setWindowTitle("Add Associate")
        # Load our UI file.
        uic.loadUi("Views/AddAssociateGUI.ui", self)
        # Find our widgets
        self.department_edit = self.findChild(QLineEdit, "department_edit")
        self.name_edit = self.findChild(QLineEdit, "name_edit")
        self.badge_num_edit = self.findChild(QLineEdit, "badge_num_edit")
        self.button_box = self.findChild(QtWidgets.QDialogButtonBox, "buttonBox")
        # Set an integer validator for the badge_num_edit
        self.badge_num_edit.setValidator(QIntValidator(0, 999999999, self))

    # Custom accept logic to provide a message box to give confirmation that the associate was added.
    def accept(self):
        QMessageBox.information(self, "Associate Added", "The associate has been added successfully.")
        super().accept()

    # Custom rejection logic to provide an option to cancel.
    def reject(self):
        reply = QMessageBox.question(self, "Cancel", "Are you sure you want to cancel?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                     QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            super().reject()

    # Method to pass our QLineEdit data back to the Main window.
    def get_data(self):
        return self.department_edit.text(), self.name_edit.text(), self.badge_num_edit.text()
