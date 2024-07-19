from PyQt6.QtWidgets import QApplication
from Views.AppGUI_logic import AppGUIWindow
from Controllers.associate_controller import AssociateController
from Controllers.previous_week_controller import PreviousWeekController
from Controllers.current_week_controller import CurrentWeekController
from Controllers.date_transfer_controller import DataTransferController
import sys


def launch_app():
    # Declare our application
    app = QApplication(sys.argv)
    # Set up our controllers
    db_path = 'TimesRecord.db'
    date_transfer_controller = DataTransferController(db_path)
    date_transfer_controller.check_and_update_week()
    associate_controller = AssociateController(db_path)
    current_week_controller = CurrentWeekController(db_path)
    previous_week_controller = PreviousWeekController(db_path)

    # Assign our window variable the APPGuiWindow class. That class handles calling the UI logic.
    window = AppGUIWindow(associate_controller, current_week_controller)
    # Show the window.
    window.show()
    # Do NOT exit unless the window is closed.
    sys.exit(app.exec())


if __name__ == '__main__':
    launch_app()
