import sqlite3
import random
from datetime import datetime, timedelta


# This method is for assigning random sign-in / sign-out times to the data table.
def generate_sign_in_out_times(base_date):
    # Generate random sign-in hour between 12:00 AM and 11:00 PM. This is just a 24 hour time-period.
    sign_in_hour = random.randint(0, 23)
    # My workplace for some reason ONLY lets people sign-in and sign-out in multiples of 6. No clue why, it just
    # is that way.
    sign_in_minute = random.choice(range(0, 60, 6))
    # We pass in a date object to this method. We'll replace the base_date that is passed and update it
    # according to the sign-in time generated randomly.
    sign_in_time = base_date.replace(hour=sign_in_hour, minute=sign_in_minute, second=0)

    # Sometimes people gotta leave work early. I pose the only stipulation is that the sign-out time MUST be
    # greater than the sign-in time. This means the minimum amount of time you can work is 6 minutes.
    min_duration_minutes = 6

    # Get total minutes in a day (1440 minutes)
    max_duration_minutes = 24 * 60

    # Generate random duration ensuring it is a multiple of 6 minutes. We add 1 to max_duration_minutes because the
    # random choice function stops at 1 before the end of the range. We want to include the end of the range in this
    # instance.
    duration_minutes = random.choice(range(min_duration_minutes, max_duration_minutes + 1, 6))

    # Sign out time is just the amount of hours worked added on to our sign in time.
    sign_out_time = sign_in_time + timedelta(minutes=duration_minutes)

    # Return our tuple of both sign in and sign out times.
    return sign_in_time, sign_out_time


# This dummy controller class solely exists for us to populate dummy data into the data table for testing purposes.
# I do however see some reusability of the code I have created here for our actual controller.
class DummyDataController:
    def __init__(self, db_path):
        self.db_path = db_path

    # I already created the tables using DataGrip. It has an interactive GUI. To populate the data, I will be
    # creating methods here, so we are free to enter / remove data for testing purposes.
    def populate_dummy_data(self):
        # Create an instance of the sqlite3 object.
        connect_obj = sqlite3.connect(self.db_path)
        # Create cursor object
        cursor = connect_obj.cursor()

        associates = [
            (23462, "Austin Calloni", "Pokey"),
            (1111, "Brant Badger", "Developer"),
            (2222, "Ethan Wheeler", "Developer"),
            (3333, "Michael Balcazar", "Developer"),
            (4444, "Taylar Orndorff", "Developer")

        ]
        # Populate our associates table with the list of tuples above.
        cursor.executemany('''INSERT INTO Associates (BadgeNum, Name, Department) VALUES (?, ?, ?)''', associates)

        # A "Current Week" is at 0:00 on Monday. To determine the start of the week we will get the current day, and
        # subtract the day as a timedelta object. This will effectively return the monday of the current week.
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())

        # Dummy previous week sign-ins and sign-outs for 2 months
        # There's currently 5 associates as per the dummy associates list.
        for i in range(5):
            # 60 days in 2 months.
            for j in range(60):
                # We take our start of week and subtract the loop variable + 7. This ensures we do NOT overlap with
                # the current week. This will however leave a 1-week gap in between the current week and last week.
                # I will leave this week open for us to manually edit and generate data as we please.
                date = start_of_week - timedelta(days=(j + 7))

                # Call our random sign in and sign out generator method.
                sign_in_time, sign_out_time = generate_sign_in_out_times(date)

                # Execute our cursor object and populate the data table. As for the odd strftime method,
                # SQLite expects a formatted string for TIME columns so we must explicitly state our times in the
                # format it expects.
                cursor.execute('''INSERT INTO PreviousWeeksSignInSignOut (BadgeNum, Date, SignInTime, SignOutTime, AdditionalNotes)
                                                  VALUES (?, ?, ?, ?, ?)''',
                               (associates[i][0], date.date(), sign_in_time.strftime('%H:%M:%S'),
                                sign_out_time.strftime('%H:%M:%S'), "Test" + str(i)))

        connect_obj.commit()
        connect_obj.close()

    # Method to clear all the associates out from the table
    def clear_all_associates(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Associates')
        conn.commit()
        conn.close()

    # Method to clear out all the previous entries
    def clear_all_previous_entries(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM PreviousWeeksSignInSignOut')
        conn.commit()
        conn.close()
