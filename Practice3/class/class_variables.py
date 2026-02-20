class Car:
    wheels = 4

    def __init__(self, brand, color):
        self.brand = brand
        self.color = color

if __name__ == "__main__":
    c1 = Car("Toyota", "white")
    c2 = Car("BMW", "black")

    print(c1.brand, c1.color)
    print(c2.brand, c2.color)

    print(c1.wheels)
    print(c2.wheels)

    Car.wheels = 6
    print(c1.wheels, c2.wheels)

    c1.wheels = 3
    print(c1.wheels, c2.wheels, Car.wheels)