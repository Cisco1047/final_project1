from PyQt6.QtWidgets import *
from transactionGUI import *
import csv


class LogicTransaction(QMainWindow, Ui_transactionWindow):
    """Logic class for handling transactions, including deposits, withdrawals, and balance inquiries."""

    def __init__(self):
        """Initializes the transaction window and its components, connects buttons to their respective functions."""
        super().__init__()
        self.setupUi(self)

        # Initialize user balance and details
        self.balance = 0.0
        self.current_first_name = ""
        self.current_last_name = ""
        self.current_pin = ""

        # Connect button actions to methods
        self.depositPushButton.clicked.connect(lambda: self.deposit())
        self.withdrawButton.clicked.connect(lambda: self.withdraw())
        self.clearButton.clicked.connect(lambda: self.clear())

    def load_user_balance(self, first_name: str, last_name: str, pin: str) -> None:
        """
        Loads the user's balance from a CSV file based on provided credentials.
        """
        self.current_first_name = first_name
        self.current_last_name = last_name
        self.current_pin = pin

        # Read the CSV file to find the user's balance
        try:
            with open('accounts.csv', newline='', mode='r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) == 4:
                        csv_first_name, csv_last_name, csv_pin, csv_balance = row
                        if (csv_first_name.lower() == first_name.lower() and
                                csv_last_name.lower() == last_name.lower() and
                                csv_pin == pin):
                            self.balance = float(csv_balance)
                            break
                else:
                    # Default to 0.0 if the user doesn't exist in the file
                    self.balance = 0.0
        except FileNotFoundError:
            self.balance = 0.0

        self.update_balance_label()

    def update_balance_label(self) -> None:
        """Updates the displayed balance on the transaction window's UI."""
        self.activityOutputTransactionLabel.setText(f'Current Balance: ${self.balance:.2f}')

    def deposit(self) -> None:
        """Deposits a user-specified amount into their account and updates the CSV file."""
        try:
            action_amount = float(self.amountTextBox.text().strip('$'))
        except ValueError:
            self.activityOutputTransactionLabel.setText('Invalid input: Please enter a valid transaction amount.')
            return

        if action_amount <= 0:
            self.activityOutputTransactionLabel.setText('Invalid: Deposit amount must be positive.')
            return

        self.balance += action_amount
        self.update_balance_label()
        self.update_csv_balance()
        self.clear()

    def withdraw(self) -> None:
        """Withdraws a user-specified amount from their account if sufficient funds exist, and updates the CSV file."""
        try:
            action_amount = float(self.amountTextBox.text().strip('$'))
        except ValueError:
            self.activityOutputTransactionLabel.setText('Invalid input: Please enter a valid transaction amount.')
            return

        if action_amount <= 0:
            self.activityOutputTransactionLabel.setText('Invalid: Withdrawal amount must be positive.')
            return

        if action_amount > self.balance:
            self.activityOutputTransactionLabel.setText('Insufficient funds.')
            return

        self.balance -= action_amount
        self.update_balance_label()
        self.update_csv_balance()
        self.clear()

    def clear(self) -> None:
        """Clears the input text box and sets focus to it for the next input."""
        self.amountTextBox.setText('$')
        self.amountTextBox.setFocus()

    def update_csv_balance(self) -> None:
        """Updates the user's balance in the accounts CSV file after a transaction."""
        updated_rows = []
        user_found = False

        # Read and update the CSV file
        try:
            with open('accounts.csv', newline='', mode='r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if len(row) == 4:
                        csv_first_name, csv_last_name, csv_pin, csv_balance = row
                        if (csv_first_name.lower() == self.current_first_name.lower() and
                                csv_last_name.lower() == self.current_last_name.lower() and
                                csv_pin == self.current_pin):
                            updated_rows.append([csv_first_name, csv_last_name, csv_pin, f'{self.balance:.2f}'])
                            user_found = True
                        else:
                            updated_rows.append(row)
                    else:
                        updated_rows.append(row)
        except FileNotFoundError:
            pass

        # If the user was not found during reading, add them to the list
        if not user_found:
            updated_rows.append(
                [self.current_first_name, self.current_last_name, self.current_pin, f'{self.balance:.2f}'])

        # Write the updated rows back to the CSV file
        try:
            with open('accounts.csv', mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(updated_rows)
        except IOError as e:
            self.activityOutputTransactionLabel.setText(f'Error updating balance: {e}')
