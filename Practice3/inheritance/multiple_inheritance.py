class Flyable:
    def move(self):
        return "I can fly"

class Swimmable:
    def move(self):
        return "I can swim"

class Duck(Flyable, Swimmable):
    def sound(self):
        return "Quack"

class Duck2(Swimmable, Flyable):
    def sound(self):
        return "Quack"

if __name__ == "__main__":
    d1 = Duck()
    d2 = Duck2()

    print(d1.move(), d1.sound())
    print(d2.move(), d2.sound())

    print([cls.__name__ for cls in Duck.mro()])
    print([cls.__name__ for cls in Duck2.mro()])