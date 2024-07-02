from Models.associate import Associate
from Models.database import Database


class AssociateController:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.model = Associate(self.db)

    def add_associate(self, badge_num, name, department):
        self.model.add_associate(badge_num, name, department)

    def get_associates(self):
        return self.model.get_all_associates()

    def remove_associate(self, badge_num):
        self.model.remove_associate(badge_num)
