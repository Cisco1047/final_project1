from gui import *
from logicCustomer import *
from logicTransaction import *
from PyQt6 import QtWidgets
import csv


class Logic(QMainWindow, Ui_mainWindow):
    """Main logic class that integrates the UI with backend operations for managing transactions and customer
    interactions."""

    def __init__(self):
        """Initializes the main window and its components, connects buttons to their functionalities."""
        super().__init__()

        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)

        self.ui.pinTextBox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        # Connect button to show the secondary windows
        self.ui.newCustomerButton.clicked.connect(self.show_new_customer_window)
        self.ui.enterButton.clicked.connect(self.show_transaction_window)

        # Initialize Transaction windows
        self.transaction_window = LogicTransaction()

        # Initialize New Customer Window
        self.newcustomer_window = LogicCustomer()
        self.newcustomer_window.exitButton.clicked.connect(self.show_main_window)

    def show_new_customer_window(self) -> None:
        """Hides the main window and displays the new customer window."""
        self.hide()
        self.newcustomer_window.show()

    def show_main_window(self) -> None:
        """Hides the new customer window and shows the main window."""
        self.newcustomer_window.hide()
        self.show()

    def show_transaction_window(self) -> None:
        """Validates user credentials and shows the transaction window if credentials are valid."""
        try:
            firstName = self.ui.firstNameTextBox.text()
            lastName = self.ui.lastNameTextBox.text()
            pin = int(self.ui.pinTextBox.text())
        except ValueError:
            self.ui.messageAccountLabel.setText('Please enter your name and pin.')
            return

        if not firstName:
            self.ui.messageAccountLabel.setText('Please enter your first name.')
        elif not lastName:
            self.ui.messageAccountLabel.setText('Please enter your last name.')
        elif pin < 1000 or pin > 9999:
            self.ui.messageAccountLabel.setText('Please enter your pin. It will be a four digit number.')
        else:
            credentials_valid = False
            try:
                with open('accounts.csv', newline='', mode='r') as csvfile:
                    reader = csv.reader(csvfile)
                    for row in reader:
                        if len(row) != 4:
                            continue
                        csv_firstName, csv_lastName, csv_pin, _ = row
                        if (csv_firstName.lower() == firstName.lower() and
                                csv_lastName.lower() == lastName.lower() and
                                csv_pin == str(pin)):
                            credentials_valid = True
                            break
            except FileNotFoundError:
                self.ui.messageAccountLabel.setText('Accounts file not found.')
                return

            if credentials_valid:
                self.transaction_window.load_user_balance(firstName, lastName, str(pin))
                self.hide()
                self.transaction_window.show()
            else:
                self.ui.messageAccountLabel.setText('Invalid credentials. Please try again.')
