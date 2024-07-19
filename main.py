from Controllers.dummy_data_controller import DummyDataController
from AppLauncher import *
import sys


def main():
    db_path = 'TimesRecord.db'
    # Initialize DummyDataController and create tables and populate data
    dummy_data_controller = DummyDataController(db_path)
    dummy_data_controller.populate_dummy_data()
    # Remove the comment lines if you wish to delete the entries
    # dummy_data_controller.clear_all_associates()
    # dummy_data_controller.clear_all_previous_entries()


if __name__ == "__main__":
    main()
