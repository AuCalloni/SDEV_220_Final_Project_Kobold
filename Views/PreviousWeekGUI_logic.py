from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QPushButton, QLabel, QVBoxLayout, QAbstractItemView, \
    QMessageBox
from PyQt6 import uic, QtCore, QtGui
from PyQt6.QtCore import Qt


# Previous weeks view. All prior entries will be dumped in this view.
class PreviousWeekGUI(QMainWindow):
    def __init__(self, associate_controller, current_week_controller, date_transfer_controller,
                 previous_week_controller, main_callback):
        super().__init__()
        # Assign our controllers to private fields
        self.associate_controller = associate_controller
        self.current_week_controller = current_week_controller
        self.previous_week_controller = previous_week_controller
        self.date_transfer_controller = date_transfer_controller
        # Main callback function to transfer back to the main view.
        self.main_callback = main_callback
        # Set our default current page number to 1.
        self.current_page = 1
        # Default items per page is 1. 1 is equivalent to a week's worth of data.
        self.items_per_page = 1
        # Empty dictionary to keep track of what cells changed. Original data will be stored in this for a later
        # comparison.
        self.original_data = {}
        # Load our UI
        uic.loadUi('Views/PreviousWeekGUI.ui', self)
        # Find our widgets and assign them to private fields.
        self.back_button = self.findChild(QPushButton, 'back_button')
        self.table_view = self.findChild(QTableView, 'previous_weeks_table')
        self.page_label = self.findChild(QLabel, 'page_label')
        self.next_button = self.findChild(QPushButton, 'next_button')
        self.prev_button = self.findChild(QPushButton, 'prev_button')
        self.update_button = self.findChild(QPushButton, 'update_button')

        # Empty set to keep track of what rows have had changed made to them. This is used for the update method.
        self.modified_records = set()

        # Initialize the table model
        self.table_model = QtGui.QStandardItemModel()
        self.table_view.setModel(self.table_model)

        # Connect our click and DataChanged events.
        self.table_model.dataChanged.connect(self.on_data_changed)
        self.next_button.clicked.connect(self.next_page)
        self.prev_button.clicked.connect(self.previous_page)
        self.back_button.clicked.connect(self.return_to_main_view)
        self.update_button.clicked.connect(self.update_entries)
        # Update our page label.
        self.update_page_label()
        # Populate the table with previous weekly entries.
        self.populate_times_table()

    # Method to go to the next page.
    def next_page(self):
        # Get the total amount of weeks.
        total_weeks = self.previous_week_controller.get_total_weeks()
        # As long as our page number does not exceed the maximum amount of weeks, we can go to the next page.
        if self.current_page < total_weeks:
            self.current_page += 1
            self.populate_times_table()

    # Method to go back a page.
    def previous_page(self):
        # As long as we are not at page 1 or below, we can go back a page.
        if self.current_page > 1:
            self.current_page -= 1
            self.populate_times_table()

    # Update the page label. This is needed after changing pages.
    def update_page_label(self):
        self.page_label.setText(f"Page {self.current_page}")

    # Method to populate our previous weekly entries. This differs from our "current weekly entries" because it uses
    # pagination to separate the weekly entries. 1 page worth of data is a week's worth of data for each associate.

    def populate_times_table(self):
        # Get our paginated entries and total weeks.
        entries, total_weeks = self.previous_week_controller.get_paginated_weekly_entries(self.current_page,
                                                                                          self.items_per_page)

        # Set the standard item model for our table to bind to.
        model = QtGui.QStandardItemModel(len(entries), 6)

        # Set our headers.
        model.setHorizontalHeaderLabels(['BadgeNum', 'Name', 'Date', 'SignInTime', 'SignOutTime', 'AdditionalNotes'])

        # Clear previous data.
        self.original_data.clear()
        self.modified_records.clear()
        # Loop through each row.
        for row, entry in enumerate(entries):
            # Set our record number.
            record_num = entry[0]

            # Set our badge num.
            badge_num = entry[1]

            # get_name_by_badge_num returns a list of tuples, but our QStandardItem is expecting a string.
            associate_name_tuple = self.associate_controller.get_name_by_badge_num(badge_num)

            # Get just the first item from the list/tuple. There's only one item to retrieve anyway which is the name.
            associate_name = associate_name_tuple[0] if associate_name_tuple else "Unknown"

            # Store the record number as the key, and the rest of the data as a list as the value.
            self.original_data[record_num] = entry[1:]

            # Set the badge number item and set the record_number as background data.
            badge_item = QtGui.QStandardItem(str(badge_num))
            badge_item.setData(record_num, Qt.ItemDataRole.UserRole)
            # We do not want the badge field to be editable. The ~ operator is a bitwise NOT operator and the & is a
            # bitwise AND operator. We are essentially retrieving all the flags and just flipping the ItemIsEditable
            # flag to be non-edible.
            badge_item.setFlags(badge_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            model.setItem(row, 0, badge_item)

            # Set the name column since our paginated weekly entries does not return a name.
            name_item = QtGui.QStandardItem(associate_name)
            # Don't allow the name to be edited
            name_item.setFlags(name_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            model.setItem(row, 1, name_item)

            # Set the date column and make it not editable
            date_item = QtGui.QStandardItem(str(entry[2]))
            date_item.setFlags(date_item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the date item not editable
            model.setItem(row, 2, date_item)

            # Set the other items (SignInTime, SignOutTime, AdditionalNotes).
            for column, value in enumerate(entry[3:6]):
                item = QtGui.QStandardItem(str(value))
                # Add 2 to the column to offset it since we are slicing 2:6.
                model.setItem(row, column + 3, item)

        # Set the table's model.
        self.table_view.setModel(model)
        self.table_model = model
        # Ensure the signal is connected to the new model. This is NEEDED or the dataChanged event just doesn't work
        # even though we originally set it in the __init__.
        self.table_model.dataChanged.connect(self.on_data_changed)
        self.table_model = model
        # Update the page label and navigation buttons.
        self.update_page_label()
        self.update_navigation_buttons(total_weeks)

    # Logic to enable or disable the prev/next buttons.
    def update_navigation_buttons(self, total_weeks):
        self.next_button.setEnabled(self.current_page < total_weeks)
        self.prev_button.setEnabled(self.current_page > 1)

    # Calls the callback function to return to the main view.
    def return_to_main_view(self):
        self.main_callback(self.associate_controller, self.current_week_controller, self.date_transfer_controller,
                           self.previous_week_controller)
        self.close()

    # Logic for data changed event. We ONLY want to update entries that have changes to them so we store them using the
    # on_data_changed event.
    def on_data_changed(self, top_left, bottom_right, roles):
        # For each item that is of EditRole type. EditRole is applied by the QtFramework whenever a cell is changed.
        if QtCore.Qt.ItemDataRole.EditRole in roles:
            # We want to include the bottom right row, so since range stops at the last index, we add 1 to the end.
            for row in range(top_left.row(), bottom_right.row() + 1):
                # Set the record_id as a user role.
                record_id = self.table_model.item(row, 0).data(QtCore.Qt.ItemDataRole.UserRole)
                # Add the modified record to the set.
                self.modified_records.add(record_id)

    # Method to update our entries.
    def update_entries(self):
        # Declare an empty list for our entries
        updated_entries = []
        # Loop through all the modified records
        for record_id in self.modified_records:
            # Get the row number in the table
            row = self.get_row_by_record_id(record_id)
            # If the row is not found we return
            if row is None:
                continue
            # Our new sign in time
            new_sign_in_time = self.table_model.item(row, 3).text()
            # Our new sign out time
            new_sign_out_time = self.table_model.item(row, 4).text()
            # Our new additional notes
            new_additional_notes = self.table_model.item(row, 5).text()

            # Retrieve original data for comparison
            original_data = self.original_data.get(record_id)
            # If no data is found we skip and continue
            if not original_data:
                continue

            # Assign meaningful names from our retrieved original data
            original_sign_in_time, original_sign_out_time, original_additional_notes = original_data[2], original_data[
                3], original_data[4]

            # Check if any of the new values differ from the original values
            if (new_sign_in_time != original_sign_in_time or
                    new_sign_out_time != original_sign_out_time or
                    new_additional_notes != original_additional_notes):
                # Append the tuple to our list
                updated_entries.append((record_id, new_sign_in_time, new_sign_out_time, new_additional_notes))

        for entry in updated_entries:
            # Unpack the tuple
            record_id, new_sign_in_time, new_sign_out_time, new_additional_notes = entry
            # Call our update method.
            self.previous_week_controller.update_entry(record_id, new_sign_in_time, new_sign_out_time,
                                                       new_additional_notes)
        # State how many entries updated
        if updated_entries:
            QMessageBox.information(self, "Update Successful", f"Updated {len(updated_entries)} entry(ies).")
        # If no entries were updated, state no changes were made.
        else:
            QMessageBox.information(self, "No Changes", "No changes detected.")

        # Clear the modified records after updating
        self.modified_records.clear()

    # Method to retrieve the row number based off of the passed in record id.
    def get_row_by_record_id(self, record_id):
        # Get the amount of rows
        rows = self.table_model.rowCount()
        for row in range(rows):
            # If our user data record id at the row matches the passed in record id, return the row
            if self.table_model.item(row, 0).data(QtCore.Qt.ItemDataRole.UserRole) == record_id:
                return row
        # Otherwise return nothing.
        return None
