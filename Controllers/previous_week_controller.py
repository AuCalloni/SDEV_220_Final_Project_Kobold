from Models.database import Database
from Models.previous_weeks_sign_in_sign_out import PreviousWeeksSignInSignOut


class PreviousWeekController:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.model = PreviousWeeksSignInSignOut(self.db)

    def add_entry(self, badge_num, date, sign_in_time, sign_out_time, additional_notes):
        self.model.add_entry(badge_num, date, sign_in_time, sign_out_time, additional_notes)

    def update_entry(self, record_id, sign_in_time, sign_out_time, additional_notes):
        self.model.update_entry(record_id, sign_in_time, sign_out_time, additional_notes)

        # Same logic to handle validating if our update method worked correctly.
        updated_entry = self.model.get_entry_by_id(record_id)
        return updated_entry[3] == sign_in_time and updated_entry[4] == sign_out_time and updated_entry[
            5] == additional_notes

    def get_entries_for_week(self, start_date, end_date):
        return self.model.get_entries_for_week(start_date, end_date)

    def get_paginated_weekly_entries(self, page_number, page_size=1):
        return self.model.get_paginated_weekly_entries(page_number, page_size)

    def clear_entries(self):
        self.model.clear_entries()

    # Separate method to handle getting a single record. Same logic as our current week model.
    def get_entry_by_id(self, record_id):
        return self.model.get_entry_by_id(record_id)
