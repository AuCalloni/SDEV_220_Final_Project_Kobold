from Models.database import Database
from Models.previous_weeks_sign_in_sign_out import PreviousWeeksSignInSignOut


# Previous week controller to interact withour Previous week model.
class PreviousWeekController:
    def __init__(self, db_path):
        # Connect our database.
        self.db = Database(db_path)
        # Connect to our model.
        self.model = PreviousWeeksSignInSignOut(self.db)

    # Call the model's add entry method
    def add_entry(self, badge_num, date, sign_in_time, sign_out_time, additional_notes):
        self.model.add_entry(badge_num, date, sign_in_time, sign_out_time, additional_notes)

    # Call the model's update_entry method.
    def update_entry(self, record_id, sign_in_time, sign_out_time, additional_notes):
        self.model.update_entry(record_id, sign_in_time, sign_out_time, additional_notes)

        # Same logic to handle validating if our update method worked correctly.
        updated_entry = self.model.get_entry_by_id(record_id)
        return updated_entry[3] == sign_in_time and updated_entry[4] == sign_out_time and updated_entry[
            5] == additional_notes

    # Call the model's get entries_for_week method.
    def get_entries_for_week(self, start_date, end_date):
        return self.model.get_entries_for_week(start_date, end_date)

    # Call the model's get_paginated_weekly_entries method.
    def get_paginated_weekly_entries(self, page_number, page_size=1):
        return self.model.get_paginated_weekly_entries(page_number, page_size)

    # Call the model's clear_entries method (PROBABLY DON'T EVER DO THIS OUTSIDE TESTING!)
    def get_entry_by_id(self, record_id):
        return self.model.get_entry_by_id(record_id)
