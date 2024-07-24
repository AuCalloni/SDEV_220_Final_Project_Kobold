from Models.associate import Associate
from Models.database import Database


# Associate controller to call our Associate model methods.
class AssociateController:
    def __init__(self, db_path):
        self.db = Database(db_path)
        self.model = Associate(self.db)

    # Call our add_associate method from the model.
    def add_associate(self, badge_num, name, department):
        self.model.add_associate(badge_num, name, department)

    # Call our get_all_associates method from the model.
    def get_associates(self):
        return self.model.get_all_associates()

    # Call our remove_associate method from the model.
    def remove_associate(self, badge_num):
        self.model.remove_associate(badge_num)

    # Call our model's get_badge_num_by_name
    def get_badge_num_by_name(self, name):
        return self.model.get_badge_num_by_name(name)

    def get_name_by_badge_num(self, badge_num):
        return self.model.get_name_by_badge_num(badge_num)
