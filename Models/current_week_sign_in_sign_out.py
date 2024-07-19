# This is our model for the Current Week table entries.
# I refactored this to also improve readability and efficiency. All the SQLite boilerplate is placed in its own
# method. The methods still perform the same logic, they are now MUCH cleaner without all the boilerplate in the way.
class CurrentWeekSignInSignOut:
    def __init__(self, db):
        self.db = db

    # Add in a new entry to the table. Our date_transfer_controller is typically the only thing that will use this
    # particular method, since it is in charge of initializing a new week.
    def add_entry(self, badge_num, date, sign_in_time, sign_out_time, additional_notes):
        query = '''INSERT INTO CurrentWeekSignInSignOut (BadgeNum, Date, SignInTime, SignOutTime, AdditionalNotes)
                   VALUES (?, ?, ?, ?, ?)'''
        self._execute_query(query, (badge_num, date, sign_in_time, sign_out_time, additional_notes))

    # Update an entry in the current week. This will probably be the most used method.
    def update_entry(self, record_id, sign_in_time, sign_out_time, additional_notes):
        query = '''UPDATE CurrentWeekSignInSignOut
                   SET SignInTime = ?, SignOutTime = ?, AdditionalNotes = ?
                   WHERE RecordID = ?'''
        self._execute_query(query, (sign_in_time, sign_out_time, additional_notes, record_id))

    # Get all entries from a passed in date.
    def get_entries_for_date(self, date):
        query = 'SELECT * FROM CurrentWeekSignInSignOut WHERE Date = ?'
        return self._fetch_all(query, (date,))

    # Get ALL entries from the table.
    def get_all_entries(self):
        query = 'SELECT * FROM CurrentWeekSignInSignOut'
        return self._fetch_all(query)

    # Clear all entries from the table. This is another method that is pretty much only used by our
    # date_transfer_controller
    def clear_entries(self):
        query = 'DELETE FROM CurrentWeekSignInSignOut'
        self._execute_query(query)

    # Get a specific entry by the record id.
    def get_entry_by_id(self, record_id):
        query = 'SELECT * FROM CurrentWeekSignInSignOut WHERE RecordID = ?'
        return self._fetch_one(query, (record_id,))

    # Get a specific entry using a badge and date
    def get_entry_for_badge_and_date(self, badge_num, date):
        query = '''SELECT * FROM CurrentWeekSignInSignOut WHERE BadgeNum = ? AND Date = ?'''
        return self._fetch_one(query, (badge_num, date))

    # Get a specific record_id by passing in both a badge number and date.
    def get_record_id_for_date(self, badge_num, date):
        entry = self.get_entry_for_badge_and_date(badge_num, date)
        return entry[0] if entry else None

    # Segregated boilerplate code for commits to the SQLite table. This is used by our add, update and clear methods.
    def _execute_query(self, query, params=()):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    # Segregated boilerplate to return multiple entries from the table. This is used by our get_entries_for_date and
    # get_all_entries methods.
    def _fetch_all(self, query, params=()):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    # Segregated boilerplate to return a single queried result. This is only used by our get_entry_by_id method.
    def _fetch_one(self, query, params=()):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
