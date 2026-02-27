class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def info(self):
        return f"{self.name}, age {self.age}"

class BankAccount:
    def __init__(self, owner, balance=0.0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

if __name__ == "__main__":
    s1 = Student("Andrey", 19)
    print(s1.info())

    acc = BankAccount("Andrey")
    acc.deposit(1500)
    print(acc.balance)
    print(acc.withdraw(700))
    print(acc.balance)
    print(acc.withdraw(99999))
    #начальные данные при создании.