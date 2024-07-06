from PyQt5.QtWidgets import *

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OneNote Sign-In")

        self.label = QLabel("Sign In")
        self.button = QPushButton("Next")
        self.button.clicked.connect(self.the_button_was_clicked)
        self.input = QLineEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    #Button method, WIP    
    def the_button_was_clicked(self):
        print("Clicked.")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()