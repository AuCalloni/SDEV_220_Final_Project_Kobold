class Associate:
    def __init__(self, db):
        self.db = db

    #Add associate method
    def add_associate(self, badge_num, name, department):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Associates (BadgeNum, Name, Department) VALUES (?, ?, ?)''',
                           (badge_num, name, department))
            conn.commit()
    # Remove associate method
    def remove_associate(self, badge_num):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM Associates WHERE BadgeNum = ?', (badge_num,))
            conn.commit()
    # Get all associates in the table.
    def get_all_associates(self):
        with self.db.connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Associates')
            return cursor.fetchall()