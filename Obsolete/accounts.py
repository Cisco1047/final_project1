
class Account:

    def __init__(self, name, balance=0.00):

        self.__account_balance = balance
        self.__account_name = name
        self.set_balance(balance)

    def __str__(self):
        return f'Account name = {self.get_name()}, Account balance = {self.get_balance():.2f}'

    def deposit(self, amount):
        if amount > 0:
            self.__account_balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.get_balance():
            self.__account_balance -= amount
            return True
        return False

    def get_balance(self):
        return self.__account_balance

    def get_name(self):
        return self.__account_name

    def set_balance(self, value):
        self.__account_balance = max(0, value)

    def set_name(self, value):
        self.__account_name = value


class SavingAccount(Account):
    MINIMUM = 100
    RATE = 0.02

    def __init__(self, name):
        super().__init__(name)
        self.__deposit_count = 0
        self.set_balance(SavingAccount.MINIMUM)

    def __str__(self):
        return f'SAVING ACCOUNT: {super().__str__()}'

    def apply_interest(self):
        if self.__deposit_count % 5 == 0:
            self.set_balance(self.get_balance() * (1 + SavingAccount.RATE))

    def deposit(self, amount):
        if amount > 0:
            super().deposit(amount)
            self.__deposit_count += 1
            self.apply_interest()
            return True
        return False

    def withdraw(self, amount):
        if amount <= 0 or amount > self.get_balance() - SavingAccount.MINIMUM:
            return False
        else:
            return super().withdraw(amount)

    def set_balance(self, value):
        if value < SavingAccount.MINIMUM:
            super().set_balance(SavingAccount.MINIMUM)
        else:
            super().set_balance(value)

    def get_deposit_count(self):
        return self.__deposit_count