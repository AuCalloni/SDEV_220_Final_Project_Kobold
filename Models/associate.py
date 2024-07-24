# Associate model class. This class holds the associate information such as Department, Badge, and full name.
class Associate:
    # Pass in our database.
    def __init__(self, db):
        self.db = db

    # Query to add associate to the table.
    def add_associate(self, badge_num, name, department):
        query = '''INSERT INTO Associates (BadgeNum, Name, Department) VALUES (?, ?, ?)'''
        self._execute_query(query, (badge_num, name, department))

    # Query to remove the passed in associate from the table.
    def remove_associate(self, badge_num):
        query = 'DELETE FROM Associates WHERE BadgeNum = ?'
        self._execute_query(query, (badge_num,))

    # Get all associates from the table. This will return the badge number, name and department. In that order.
    def get_all_associates(self):
        query = 'SELECT * FROM Associates'
        return self._fetch_all(query)

    # Retrieves the associate's badge number by passing in the name.
    def get_badge_num_by_name(self, name):
        query = 'SELECT BadgeNum FROM Associates WHERE Name = ?'
        result = self._fetch_one(query, (name,))
        return result

    def get_name_by_badge_num(self, badge_num):
        query = 'SELECT Name FROM Associates WHERE BadgeNum = ?'
        result = self._fetch_one(query, (badge_num,))
        return result

    # While refactoring this code, I found it to be pretty redundant to constantly call the sqlite database connection,
    # create a cursor, and then run the query. To clean things up, I think this is a happy median.
    # We create a private method to handle queries that are executions such as an update or delete.
    # One method will handle the boilerplate of connecting to the database, and all we do is pass in a query as a
    # parameter.
    def _execute_query(self, query, params=()):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()

    # Same deal for fetchall code. All we do is pass in a query, and it handles all the SQLite connections.
    def _fetch_all(self, query):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            # This returns a list of tuples.
            return cursor.fetchall()

    # Logic to retrieve a single entry
    def _fetch_one(self, query, params=()):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchone()
