import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QTimeEdit, QTableView, QPushButton
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from datetime import datetime


class AppGUIWindow(QMainWindow):
    def __init__(self, associate_controller, current_week_controller):
        super(QMainWindow, self).__init__()
        # Load our UI file.
        uic.loadUi('Views/AppGUI.ui', self)
        # Load our controllers
        self.associate_controller = associate_controller
        self.current_week_controller = current_week_controller
        # Find our widgets and assign them to a field
        self.employee_combo = self.findChild(QComboBox, 'employee_combo')
        self.time_in_edit = self.findChild(QTimeEdit, 'time_in_edit')
        self.time_out_edit = self.findChild(QTimeEdit, 'time_out_edit')
        self.record_button = self.findChild(QPushButton, 'record_button')
        self.times_table = self.findChild(QTableView, 'times_table')
        # Populate the combo box
        self.populate_employee_combo()
        # Populate the QTableView
        self.populate_times_table()
        # Wire up the record's click event
        self.record_button.clicked.connect(self.record_time_entry)

    # Update method that utilzies the QTimeEdit boxes.
    def record_time_entry(self):
        # Get selected associate name from combo box
        associate_name = self.employee_combo.currentText()
        # Get the respective badge number from the database
        badge_num = self.associate_controller.get_badge_num_by_name(associate_name)[0]

        # Get the time in and time out values from the QTimeEdit widgets
        time_in = self.time_in_edit.time().toString('HH:mm:ss')
        time_out = self.time_out_edit.time().toString('HH:mm:ss')

        # Get current date in 'YYYY-MM-DD' format
        current_date = datetime.now().date().strftime('%Y-%m-%d')

        # Find the record_id for the associate and today's date. This is needed for the update_entry method.
        record_id = self.current_week_controller.get_record_id_for_date(badge_num, current_date)

        if record_id:
            # Call the CurrentWeekController's update_entry method to update the in and out times
            self.current_week_controller.update_entry(record_id, time_in, time_out, "")

        # Refresh the table after updating
        self.populate_times_table()

    def populate_times_table(self):
        # Get all entries from our current week controller
        entries = self.current_week_controller.get_all_entries()
        # Set our model as a typical QStandardItemModel. The row count is the amount of entries, and for now there's
        # only 5 columns.
        model = QStandardItemModel(len(entries), 5)
        # Set the column names
        model.setHorizontalHeaderLabels(['BadgeNum', 'Date', 'SignInTime', 'SignOutTime', 'AdditionalNotes'])

        # Loop to assign data to each row
        for row, entry in enumerate(entries):
            # For each column in our entry's row. Our entry has 5 total values, so we use a slice here.
            for column, value in enumerate(entry[1:6]):
                # Convert our value to a QStandardItem, so it can be viewed.
                item = QStandardItem(str(value))
                # Set the item after conversion.
                model.setItem(row, column, item)

        self.times_table.setModel(model)

    # Populate the combo box
    def populate_employee_combo(self):
        # Get all associates
        associate_names = self.associate_controller.get_associates()
        # List comprehension to filter out everything that isn't a name
        associate_names = [associate[1] for associate in associate_names]
        # Clear the box of any data
        self.employee_combo.clear()
        for name in associate_names:
            # Add item to the box
            self.employee_combo.addItem(name)
