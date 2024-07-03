from datetime import datetime, timedelta

from Models.associate import Associate
from Models.current_week_sign_in_sign_out import CurrentWeekSignInSignOut
from Models.previous_weeks_sign_in_sign_out import PreviousWeeksSignInSignOut
from Models.database import Database

# The intention is for the program to automatically dump the current week data into the previous week table
# at the end of the week. This class does exactly that.
class DataTransferController:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.current_week_model = CurrentWeekSignInSignOut(self.db)
        self.previous_week_model = PreviousWeeksSignInSignOut(self.db)
        self.associate_model = Associate(self.db)

    # For each entry in our current week, dump it into the previous week.
    def transfer_current_to_previous(self):
        entries = self.current_week_model.get_all_entries()
        for entry in entries:
            self.previous_week_model.add_entry(entry[1], entry[2], entry[3], entry[4], entry[5])
        # Clear the table once this is done.
        self.current_week_model.clear_entries()

    # Initialize a new week. This is to be used after a transfer.
    def initialize_new_week(self):
        # Clear out the current week's entries
        self.current_week_model.clear_entries()

        # Get the list of all associates
        associates = self.associate_model.get_all_associates()

        # Get the Monday of the current week
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())

        # Insert new entries for each associate for each day of the current week
        for associate in associates:
            badge_num = associate[0]
            # Loop over all 7 days of the week.
            for i in range(7):
                date = start_of_week + timedelta(days=i)
                self.current_week_model.add_entry(badge_num, date, None, None, "")

    # Check if it's a new week.
    def check_and_update_week(self):
        today = datetime.now().date()

        # Get every entry of current week
        current_week_entries = self.current_week_model.get_all_entries()

        # Check if it's already empty
        if not current_week_entries:
            # If the table is empty, initialize the new week
            self.initialize_new_week()
            return

        # Find the end date (Sunday) of the current week from the current week entries
        last_entry_date = max(datetime.strptime(entry[2], '%Y-%m-%d').date() for entry in current_week_entries)

        # Check if today is greater than the end of the current week
        if today > last_entry_date:
            self.transfer_current_to_previous()
            self.initialize_new_week()
        else:
            # Do nothing because the week is not over.
            return
