from PyQt6.QtWidgets import *
from newCustomerGUI import *
import csv


class LogicCustomer(QMainWindow, Ui_newCustomerWindow):
    """Logic class for managing new customer registration in the system."""

    def __init__(self):
        """Initializes the customer window and its components, and connects the button to create new customers."""
        super().__init__()
        self.setupUi(self)

        self.pinNewCustomerTextBox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.confirmPinTextBox.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.enterCustomerButton.clicked.connect(lambda: self.new_customer())

    def new_customer(self) -> None:
        """Creates a new customer after validating the input fields and checking if the customer already exists."""
        try:
            firstName = self.firstNameNewCustomerTextBox.text()
            lastName = self.lastNameconfirmPinTextBoxTextBox.text()
            pin = int(self.pinNewCustomerTextBox.text())
            confirm_pin = int(self.confirmPinTextBox.text())
        except ValueError:
            self.messageNewCustomerLabel.setText('Please enter your name and new pin.')
            return

        if not firstName:
            self.messageNewCustomerLabel.setText('Please enter your first name.')
        elif not lastName:
            self.messageNewCustomerLabel.setText('Please enter your last name.')
        elif pin < 1000 or pin > 9999:
            self.messageNewCustomerLabel.setText('Please enter your pin. It must be a four-digit number.')
        elif confirm_pin < 1000 or confirm_pin > 9999:
            self.messageNewCustomerLabel.setText('Please confirm your pin. It must be a four-digit number.')
        elif pin != confirm_pin:
            self.messageNewCustomerLabel.setText('Pins do not match. Please try again.')
        else:
            # Verify that the customer does not already exist
            customer_exists = self.check_existing_customer(firstName, lastName, pin)
            if customer_exists:
                self.messageNewCustomerLabel.setText('An account with this information already exists.')
            else:
                # Write the new customer information to the accounts.csv file
                self.add_customer_to_csv(firstName, lastName, pin)
                self.messageNewCustomerLabel.setText('New account successfully created!')

    def check_existing_customer(self, firstname: str, lastname: str, pin: int) -> bool:
        """Checks if a customer with the given details already exists in the accounts.csv file."""
        try:
            with open('accounts.csv', newline='', mode='r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) == 3:
                        csv_firstName, csv_lastName, csv_pin = row
                        if (csv_firstName.lower() == firstname.lower() and
                                csv_lastName.lower() == lastname.lower() and
                                csv_pin == str(pin)):
                            return True
        except FileNotFoundError:
            self.messageNewCustomerLabel.setText('Accounts file not found.')
        return False

    def add_customer_to_csv(self, firstname: str, lastname: str, pin: int) -> None:
        """Adds a new customer to the accounts.csv file."""
        try:
            with open('accounts.csv', mode='a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([firstname, lastname, pin, 0.00])

        except IOError as e:
            self.messageNewCustomerLabel.setText(f'Failed to write to accounts.csv: {e}')
