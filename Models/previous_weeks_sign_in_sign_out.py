from datetime import timedelta, datetime


class PreviousWeeksSignInSignOut:
    def __init__(self, db):
        self.db = db

    # These 3 methods are essentially the same as the get current entries.
    def add_entry(self, badge_num, date, sign_in_time, sign_out_time, additional_notes):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO PreviousWeeksSignInSignOut (BadgeNum, Date, SignInTime, SignOutTime, AdditionalNotes)
                              VALUES (?, ?, ?, ?, ?)''',
                           (badge_num, date, sign_in_time, sign_out_time, additional_notes))
            conn.commit()

    def update_entry(self, record_id, sign_in_time, sign_out_time, additional_notes):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''UPDATE PreviousWeeksSignInSignOut
                              SET SignInTime = ?, SignOutTime = ?, AdditionalNotes = ?
                              WHERE RecordID = ?''',
                           (sign_in_time, sign_out_time, additional_notes, record_id))
            conn.commit()

    def get_entries_for_week(self, start_date, end_date):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT * FROM PreviousWeeksSignInSignOut WHERE Date BETWEEN ? AND ?''',
                           (start_date, end_date))
            return cursor.fetchall()

    # This is where it differs. To handle pagination and the ability to NOT retrieve EVERY SINGLE entry from
    # weeks prior, there's quite a bit of logic needed to achieve this. First we have our get_total_weeks method
    # which calculates the total amount of weeks stored in the Previous Signout Table.
    def get_total_weeks(self):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            # SQL statement to retrieve the lowest date and the highest date.
            cursor.execute('''SELECT MIN(Date), MAX(Date) FROM PreviousWeeksSignInSignOut''')
            result = cursor.fetchone()
            # Return 0 weeks if there is nothing retrieved.
            if result[0] is None or result[1] is None:
                return 0
            # Convert our earliest date to Y-M-D format as a datetime object.
            start_date = datetime.strptime(result[0], '%Y-%m-%d').date()
            # Convert our latest date to Y-M-D format as a datetime object.
            end_date = datetime.strptime(result[1], '%Y-%m-%d').date()
            # Get the amount of days in between.
            total_days = (end_date - start_date).days
            # Divide by 7 for amount of weeks and add 1 if total_weeks is not divisible by 7
            # to account for any remaining days that are less than week, thus counting it as a full week.
            total_weeks = total_days // 7
            if total_days % 7 != 0:
                total_weeks += 1
            return total_weeks
    # This method is used to retrieve the date ranges per page.
    def get_week_date_range(self, page_number, page_size=1):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            # Retrieve distinct dates so we don't get duplicate entries.
            cursor.execute('''SELECT DISTINCT Date FROM PreviousWeeksSignInSignOut ORDER BY Date ASC''')

            # For each retrieved date, convert the date to a datetime object.
            all_dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in cursor.fetchall()]

        # Ugly logic starts here. Indices are typically 0-indexed so we subtract 1 and multiply by page size.
        start_index = (page_number - 1) * page_size

        # Our last index page is just our starting + our page size. This is only useful in the event we need
        # to pass in more than 1 page to the method.
        end_index = start_index + page_size

        # Empty weeks list, and current week is none.
        weeks = []
        current_week = None
        # Loop through using enumerate. It'll return the index and the date per loop.
        for i, date in enumerate(all_dates):
            # Current week starts out as none
            if current_week is None:
                # Take our current date in the loop and subtract the date as weekday to get the monday of the current
                # week.
                start_date = date - timedelta(days=date.weekday())
                # Add 6 to the monday to get sunday.
                end_date = start_date + timedelta(days=6)
                # Current week of our iteration assigned as a tuple.
                current_week = (start_date, end_date)
                # Append it to the list.
                weeks.append(current_week)
            # Check if our next date iteration is greater than end date of week prior.
            elif date > current_week[1]:
                # Get monday of week
                start_date = date - timedelta(days=date.weekday())
                # Get Sunday of week
                end_date = start_date + timedelta(days=6)
                # Assign current week tuple
                current_week = (start_date, end_date)
                # Append it
                weeks.append(current_week)
        # ONLY return a slice of the weeks that we need. There's no point in returning literally every date at once.
        # IT WILL LAG!!!!
        paginated_weeks = weeks[start_index:end_index]
        return paginated_weeks

    # Pagination function using our two methods created above.
    def get_paginated_weekly_entries(self, page_number, page_size=1):
        # Call our week date range method depending on page number passed.
        weeks = self.get_week_date_range(page_number, page_size)
        paginated_entries = []
        for start_date, end_date in weeks:
            # Return entries for the week after we get our date range.
            weekly_entries = self.get_entries_for_week(start_date, end_date)
            # Tack it on to the paginated list.
            paginated_entries.extend(weekly_entries)
        total_weeks = self.get_total_weeks()
        # Return our paginated list and the total of all weeks.
        return paginated_entries, total_weeks

    def clear_entries(self):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM PreviousWeeksSignInSignOut')
            conn.commit()
