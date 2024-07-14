from Models.current_week_sign_in_sign_out import CurrentWeekSignInSignOut
from Models.database import Database


class CurrentWeekController:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.model = CurrentWeekSignInSignOut(self.db)

    def add_entry(self, badge_num, date, sign_in_time, sign_out_time, additional_notes):
        self.model.add_entry(badge_num, date, sign_in_time, sign_out_time, additional_notes)

    def update_entry(self, record_id, sign_in_time, sign_out_time, additional_notes):
        self.model.update_entry(record_id, sign_in_time, sign_out_time, additional_notes)
        # Logic to check if our entry successfully updated.
        updated_entry = self.model.get_entry_by_id(record_id)

        # Return true if all 3 updated entries match with what is currently in the table.
        return updated_entry[3] == sign_in_time and updated_entry[4] == sign_out_time and updated_entry[
            5] == additional_notes

    def get_entries_for_date(self, date):
        self.model.get_entries_for_date(date)

    def get_all_entries(self):
        return self.model.get_all_entries()

    def clear_entries(self):
        self.model.clear_entries()

    # Separate method to call the get entry by id manually if the front end needs it.
    def get_entry_by_id(self, record_id):
        return self.model.get_entry_by_id(record_id)
