from Models.current_week_sign_in_sign_out import CurrentWeekSignInSignOut
from Models.database import Database


# Current week controller that interacts and calls our CurrentWeekModel methods.
class CurrentWeekController:
    def __init__(self, db_path):
        # Connect the database.
        self.db = Database(db_path)
        # Assign the model.
        self.model = CurrentWeekSignInSignOut(self.db)

    # Call our model's add_entry method.
    def add_entry(self, badge_num, date, sign_in_time, sign_out_time, additional_notes):
        self.model.add_entry(badge_num, date, sign_in_time, sign_out_time, additional_notes)

    # Call our model's remove_entry method.
    def remove_entry(self, record_id):
        self.model.remove_entry(record_id)

    # Call our model's update_entry method.
    def update_entry(self, record_id, sign_in_time, sign_out_time, additional_notes):
        self.model.update_entry(record_id, sign_in_time, sign_out_time, additional_notes)
        # Logic to check if our entry successfully updated.
        updated_entry = self.model.get_entry_by_id(record_id)

        # Return true if all 3 updated entries match with what is currently in the table.
        return updated_entry[3] == sign_in_time and updated_entry[4] == sign_out_time and updated_entry[
            5] == additional_notes

    # Call our model's get_all_entries method.
    def get_all_entries(self):
        return self.model.get_all_entries()

    # Call our model's clear_entries method.
    def clear_entries(self):
        self.model.clear_entries()

    # Call our model's get_entry_by_id method.
    def get_entry_by_id(self, record_id):
        return self.model.get_entry_by_id(record_id)

    def get_entry_for_badge_and_date(self, badge_num, date):
        return self.model.get_entry_for_badge_and_date(badge_num, date)

    # Call our model's get_record_id_for_date
    def get_record_id_for_date(self, badge_num, date):
        return self.model.get_record_id_for_date(badge_num, date)

    # Call our model's generate_blank_weekly_entries method
    def generate_blank_weekly_entries(self, badge_num):
        self.model.generate_blank_weekly_entries(badge_num)
