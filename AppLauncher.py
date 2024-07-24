from PyQt6.QtWidgets import QApplication

from Controllers.associate_controller import AssociateController
from Controllers.previous_week_controller import PreviousWeekController
from Controllers.current_week_controller import CurrentWeekController
from Controllers.date_transfer_controller import DataTransferController
from Views.PreviousWeekGUI_logic import PreviousWeekGUI
from Views.AppGUI_logic import AppGUIWindow
import sys


def switch_to_previous_week_view(associate_controller, current_week_controller, date_transfer_controller,
                                 previous_week_controller):
    global previous_week_view
    previous_week_view = PreviousWeekGUI(associate_controller, current_week_controller, date_transfer_controller,
                                         previous_week_controller, switch_to_main_view)
    previous_week_view.show()


def switch_to_main_view(associate_controller, current_week_controller, date_transfer_controller,
                        previous_week_controller):
    global main_view
    main_view = AppGUIWindow(associate_controller, current_week_controller, date_transfer_controller,
                             previous_week_controller, switch_to_previous_week_view)
    main_view.show()


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
    switch_to_main_view(associate_controller, current_week_controller, date_transfer_controller,
                        previous_week_controller)

    # Do NOT exit unless the window is closed.
    sys.exit(app.exec())


if __name__ == '__main__':
    launch_app()
