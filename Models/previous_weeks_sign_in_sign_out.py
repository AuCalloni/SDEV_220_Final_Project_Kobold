from datetime import timedelta, datetime
from idlelib import query


# Model class to handle data interactions with the previous weekly entries table.
class PreviousWeeksSignInSignOut:
    def __init__(self, db):
        self.db = db

    # Method to add entry to the table. Mostly only used by our date_transfer_controller
    def add_entry(self, badge_num, date, sign_in_time, sign_out_time, additional_notes):
        query = '''INSERT INTO PreviousWeeksSignInSignOut (BadgeNum, Date, SignInTime, SignOutTime, AdditionalNotes)
                   VALUES (?, ?, ?, ?, ?)'''
        self._execute_query(query, (badge_num, date, sign_in_time, sign_out_time, additional_notes))

    # Method to update a single entry if needed.
    def update_entry(self, record_id, sign_in_time, sign_out_time, additional_notes):
        query = '''UPDATE PreviousWeeksSignInSignOut
                   SET SignInTime = ?, SignOutTime = ?, AdditionalNotes = ?
                   WHERE RecordID = ?'''
        self._execute_query(query, (sign_in_time, sign_out_time, additional_notes, record_id))

    # Return all entries using a provided date range.
    def get_entries_for_week(self, start_date, end_date):
        query = '''SELECT * FROM PreviousWeeksSignInSignOut WHERE Date BETWEEN ? AND ?'''
        return self._fetch_all(query, (start_date, end_date))

    # Get a single entry from the table via the provided record_id
    def get_entry_by_id(self, record_id):
        query = '''SELECT * FROM PreviousWeeksSignInSignOut WHERE RecordID = ?'''
        return self._fetch_one(query, (record_id,))

    # The logic for this just wasn't working out, so I had to take a different approach. Previously it only worked
    # as long as there were NO gaps in the previous weeks table's data. This way is much cleaner, shorter and ONLY
    # counts the total week range as long as there is populated data. Gaps in empty weeks will not affect it any longer.
    def get_total_weeks(self):
        # This query works in such a way that it only counts DISTINCT week pairs from the previous weeks data table.
        # the "strftime('%Y-%W, Date) will format each week of the year, retrieve only 1 distinct copy of it, and
        # it will be counted. This is overall a lot simpler and way better than the logic heavy method that used to
        # be here.
        query = '''SELECT COUNT(DISTINCT strftime('%Y-%W', Date)) FROM PreviousWeeksSignInSignOut'''
        result = self._fetch_one(query)
        return result[0] if result else 0

    # This method was doing far too much, so it's been refactored. The original looping logic has been placed in its
    # own method now.
    def get_week_date_range(self, page_number, page_size=1):
        # Select every distinct date from the table.
        query = '''SELECT DISTINCT Date FROM PreviousWeeksSignInSignOut ORDER BY Date ASC'''
        # For each retrieved date, convert the date to a datetime object.
        all_dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in self._fetch_all(query)]
        # Get every week as a grouping
        weeks = self._group_dates_into_weeks(all_dates)
        # Return a sliced list using our page number - 1 (since lists are 0 indexed) multiplied by the
        # page size depending on how big we want our "pages" to be. The end of the list is just the page_number
        # multiplied by the page_size.
        # Page_size is essentially just a scale factor for both the beginning and end of the list comprehension
        # depending on how big the pages will be.
        return weeks[(page_number - 1) * page_size: page_number * page_size]

    # Pagination function using our two methods created above.
    def get_paginated_weekly_entries(self, page_number, page_size=1):
        # Call our week date range method depending on page number passed.
        weeks = self.get_week_date_range(page_number, page_size)
        paginated_entries = []
        for start_date, end_date in weeks:
            # Return entries for the week after we get our date range, and tack it on to the paginated list.
            paginated_entries.extend(self.get_entries_for_week(start_date, end_date))
        total_weeks = self.get_total_weeks()
        # Return our paginated list and the total of all weeks.
        return paginated_entries, total_weeks

    # Segregated boilerplate code for queries that are a commit.
    def _execute_query(self, query, params=()):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    # Segregated boilerplate code for queries that return more than 1 entry.
    def _fetch_all(self, query, params=()):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()

    # Segregated boilerplate code for queries that return a single entry.
    def _fetch_one(self, query, params=()):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()

    # Originally used to be logic that was part of get_week_date_range. That method was doing far too much,
    # so I broke it up into two separate methods.
    def _group_dates_into_weeks(self, all_dates):
        # Declare our weeks list
        weeks = []
        # Set current week to none.
        current_week = None
        for date in all_dates:
            # current_week[1] will be the end date of each current_week item. Thus, we are checking if the date of our
            # current iteration is greater than the end date (sunday) of our current_week. If it is, then we're good
            # to add another group to the list.
            if current_week is None or date > current_week[1]:
                # Monday of the current date's week.
                start_date = date - timedelta(days=date.weekday())
                # Sunday of the corresponding date's week.
                end_date = start_date + timedelta(days=6)
                # Group them into a tuple
                current_week = (start_date, end_date)
                # Append them
                weeks.append(current_week)
        return weeks
