class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return "Meow"

class Dog(Animal):
    def speak(self):
        return "Woof"

if __name__ == "__main__":
    a = Animal("Unknown")
    c = Cat("Murka")
    d = Dog("Rex")

    for x in [a, c, d]:
        print(x.name, x.speak())
        #один класс может получать свойства и методы другого класса