class Dog:
    def bark(self):
        print("Woof!")

class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

class Counter:
    def __init__(self):
        self.value = 0
#метод функ в классе
    def inc(self):
        self.value += 1

    def dec(self):
        self.value -= 1
#селф ссылка на обьект типо передали значение и сохранили где
if __name__ == "__main__":
    dog = Dog()
    dog.bark()

    calc = Calculator()
    print(calc.add(2, 3))
    print(calc.multiply(4, 5))
#template for creating objects
    c = Counter()
    c.inc()
    c.inc()
    c.dec()
    print(c.value)

    c.owner = "Andrey"
    print(c.owner)