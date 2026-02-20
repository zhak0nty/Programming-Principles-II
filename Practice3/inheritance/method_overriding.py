class Payment:
    def pay(self, amount):
        return f"Paying {amount} by default method"

class CardPayment(Payment):
    def pay(self, amount):
        return f"Paying {amount} by card"

class CashPayment(Payment):
    def pay(self, amount):
        return f"Paying {amount} in cash"

class BonusPayment(Payment):
    def pay(self, amount):
        return super().pay(amount) + " (with bonus logic)"

if __name__ == "__main__":
    print(Payment().pay(1000))
    print(CardPayment().pay(1000))
    print(CashPayment().pay(1000))
    print(BonusPayment().pay(1000))