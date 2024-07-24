import sys

from Controllers import previous_week_controller
from Views.AddAssociateGUI_logic import *
from Views.PreviousWeekGUI_logic import *
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QTimeEdit, QTableView, QPushButton, QAbstractItemView
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt
from datetime import datetime, time, timedelta


# This is our main window. It has means to record data. It also has a way to navigate to the "previous weeks" view,
# and it also has capabilities to add and remove associates.
class AppGUIWindow(QMainWindow):
    def __init__(self, associate_controller, current_week_controller, date_transfer_controller,
                 previous_week_controller,
                 previous_callback):
        super(QMainWindow, self).__init__()
        # Load our UI file.
        uic.loadUi('Views/AppGUI.ui', self)
        # Load our controllers
        self.associate_controller = associate_controller
        self.current_week_controller = current_week_controller
        self.date_transfer_controller = date_transfer_controller
        self.previous_week_controller = previous_week_controller
        self.previous_callback = previous_callback
        # Find our widgets and assign them to a field
        self.employee_combo = self.findChild(QComboBox, 'employee_combo')
        self.time_in_edit = self.findChild(QTimeEdit, 'time_in_edit')
        self.time_out_edit = self.findChild(QTimeEdit, 'time_out_edit')
        self.record_button = self.findChild(QPushButton, 'record_button')
        self.add_associate = self.findChild(QPushButton, 'add_associate')
        self.times_table = self.findChild(QTableView, 'times_table')
        self.previous_weeks_button = self.findChild(QPushButton, 'previous_weeks_button')
        self.remove_associate = self.findChild(QPushButton, 'remove_associate')
        # Populate the combo box
        self.populate_employee_combo()
        # Populate the QTableView
        self.populate_times_table()
        # Wire up click events
        self.record_button.clicked.connect(self.record_time_entry)
        self.remove_associate.clicked.connect(self.remove_selected_associate)
        self.add_associate.clicked.connect(self.open_add_dialog)
        self.previous_weeks_button.clicked.connect(self.open_previous_weeks_view)

    # Update method that utilizes the QTimeEdit boxes.
    def record_time_entry(self):
        # Get selected associate name from combo box
        associate_name = self.employee_combo.currentText()
        # Get the respective badge number from the database
        badge_num = self.associate_controller.get_badge_num_by_name(associate_name)[0]

        # Get the time in and time out values from the QTimeEdit widgets
        time_in = self.time_in_edit.time().toString('HH:mm:ss')
        time_out = self.time_out_edit.time().toString('HH:mm:ss')

        # Get current date in 'YYYY-MM-DD' format
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        # Times are typically not recorded unless it's the end of the day. 2nd shift associates end anywhere between
        # 1:00-3:00 AM. So you need to record your time technically for the "previous" day. The logic below will
        # roll back what day the time is recorded for if it's between 1-4. Sometimes we stay later than 3, so it's best
        # to allow extra time.
        day_roll_back_start = time(0, 0, 0)
        day_roll_back_end = time(4, 0, 0)
        if day_roll_back_start <= current_time <= day_roll_back_end:
            # If our time is between these hours, roll back the day
            current_date -= timedelta(days=1)
        # Format our time for recording.
        current_date = current_date.strftime('%Y-%m-%d')
        # Find the record_id for the associate and today's date. This is needed for the update_entry method.
        record_id = self.current_week_controller.get_record_id_for_date(badge_num, current_date)
        # If a record id is found
        if record_id:
            # Call the CurrentWeekController's update_entry method to update the in and out times
            self.current_week_controller.update_entry(record_id, time_in, time_out, "")
            # Show a success message box
            QMessageBox.information(self, "Entry Updated",
                                    f"Time entry for {associate_name} has been updated successfully.")

        # Refresh the table after updating
        self.populate_times_table()

    # Method to populate our table with data.
    def populate_times_table(self):
        # Get all entries from our current week controller
        entries = self.current_week_controller.get_all_entries()
        # Set our model as a typical QStandardItemModel. The row count is the amount of entries, and for now there's
        # only 6 columns.
        model = QStandardItemModel(len(entries), 6)
        # Set the column names
        model.setHorizontalHeaderLabels(['BadgeNum', 'Name', 'Date', 'SignInTime', 'SignOutTime', 'AdditionalNotes'])

        # Loop to assign data to each row
        for row, entry in enumerate(entries):
            # Set our badge num
            badge_num = entry[1]
            # Set our record number
            record_num = entry[0]
            # get_name_by_badge_num returns a list of tuples, but our QStandardItem is expecting a string.
            associate_name_tuple = self.associate_controller.get_name_by_badge_num(badge_num)
            # Get just the first item from the list/tuple.
            associate_name = associate_name_tuple[0] if associate_name_tuple else "Unknown"
            # Set the badge number item and sets the record_number as background data for this specific StandardItem.
            # UserRole is useful for setting background information that we don't want to be displayed to the user.
            badge_item = QStandardItem(str(badge_num))
            badge_item.setData(record_num, Qt.ItemDataRole.UserRole)
            # Set our item at this column to be the badge_number item.
            model.setItem(row, 0, badge_item)

            # Set the name item. The current week controller's "get_all_entries" method does not return names.
            # Thus, we have to hardcode a name column in its place.
            name_item = QStandardItem(associate_name)
            model.setItem(row, 1, name_item)

            # Set the other items (Date, SignInTime, SignOutTime, AdditionalNotes). This is from 2:6 because 0 is our
            # badge number, and 1 is our name.
            for column, value in enumerate(entry[2:6]):
                item = QStandardItem(str(value))
                # Add two to the column to offset it since we are slicing 2:6
                model.setItem(row, column + 2, item)
        # Set the table's model.
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

    # Method to open our add new associate dialog.
    def open_add_dialog(self):
        # Construct our dialog class.
        dialog = AddAssociateDialog(self)
        # .exec() is used to prevent the dialog from closing until data is fully processed I.E. hitting OK or Cancel.
        # It also prevents the user from interacting with the main window until the dialog is closed.
        # Qt's documentation recommends using .open() for asynchronous operations, but this would cause the
        # if block to execute immediately with empty data.
        if dialog.exec():
            # Get the data from the 3 QLineEdit widgets
            department, name, badge_num = dialog.get_data()
            # If all 3 entries have a value we add it to the associate table.
            if department and name and badge_num:
                self.associate_controller.add_associate(badge_num, name, department)
                # Generate a week's worth of blank entries for the newly added associate
                self.current_week_controller.generate_blank_weekly_entries(badge_num)
                # Refresh our table
                self.populate_times_table()

    # Method to remove the selected associate from the current week table.
    def remove_selected_associate(self):
        # Get the indices of our selected rows. It's set to single selection, so it'll only be one.
        selected_indexes = self.times_table.selectionModel().selectedRows()
        # If we have a selected row
        if selected_indexes:
            # First column is our badge number.
            selected_index = selected_indexes[0]
            # This specifically calls for the badge number column of our selected row. .sibling(row,column) will
            # target whatever the row/column index is. In this instance it's our badge number column.
            # We also stored our record_number in this column as a UserRole if we ever need it. Leaving .data() empty
            # will default to the Qt.DisplayRole rather than the UserRole. If we ever need to retrieve the record_num
            # we can simply pass in Qt.ItemDataRole.UserRole into the .data() method.
            badge_number = selected_index.sibling(selected_index.row(), 0).data()
            # Confirm removal
            reply = QMessageBox.question(self, "Remove Associate",
                                         "Are you sure you want to remove this associate?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)

            # If yes, remove the associate
            if reply == QMessageBox.StandardButton.Yes:
                self.associate_controller.remove_associate(badge_number)
                # Transfer all current weekly entries of the associate to the past view.
                self.date_transfer_controller.transfer_removed_associate_data(badge_number)
                # Refresh our table.
                self.populate_times_table()

                # Show a success message box
                QMessageBox.information(self, "Associate Removed",
                                        f"Associate with badge number {badge_number} has been removed successfully.")

    # Callback to open our previous weeks view.
    def open_previous_weeks_view(self):
        self.previous_callback(self.associate_controller, self.current_week_controller, self.date_transfer_controller,
                               self.previous_week_controller)
        self.close()
