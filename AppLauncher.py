from PyQt6.QtWidgets import QApplication

from Controllers.associate_controller import AssociateController
from Controllers.previous_week_controller import PreviousWeekController
from Controllers.current_week_controller import CurrentWeekController
from Controllers.date_transfer_controller import DataTransferController
from Views.PreviousWeekGUI_logic import PreviousWeekGUI
from Views.AppGUI_logic import AppGUIWindow
import sys

# Define the global variables at the module level so my IDE will shut up.
previous_week_view = None
main_view = None


# To avoid circular dependency, we have two main call back methods with global variables that handle what view
# is to be shown. This one calls our previous week's view.
def switch_to_previous_week_view(associate_controller, current_week_controller, date_transfer_controller,
                                 previous_week_controller):
    global previous_week_view
    previous_week_view = PreviousWeekGUI(associate_controller, current_week_controller, date_transfer_controller,
                                         previous_week_controller, switch_to_main_view)
    previous_week_view.show()


# This method switches back to our main view.
def switch_to_main_view(associate_controller, current_week_controller, date_transfer_controller,
                        previous_week_controller):
    global main_view
    main_view = AppGUIWindow(associate_controller, current_week_controller, date_transfer_controller,
                             previous_week_controller, switch_to_previous_week_view)
    main_view.show()


# Our driving method to launch the application.
def launch_app():
    # Declare our application
    app = QApplication(sys.argv)
    # Set up our controllers
    db_path = 'TimesRecord.db'
    # Assign our controllers
    date_transfer_controller = DataTransferController(db_path)
    # Check if it's a new week, if so perform updates
    date_transfer_controller.check_and_update_week()
    associate_controller = AssociateController(db_path)
    current_week_controller = CurrentWeekController(db_path)
    previous_week_controller = PreviousWeekController(db_path)

    # Switch to the main view.
    switch_to_main_view(associate_controller, current_week_controller, date_transfer_controller,
                        previous_week_controller)

    # Do NOT exit unless the window is closed.
    sys.exit(app.exec())


if __name__ == '__main__':
    launch_app()
