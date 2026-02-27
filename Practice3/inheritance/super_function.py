class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def info(self):
        return f"Brand: {self.brand}"

class Car(Vehicle):
    def __init__(self, brand, doors):
        super().__init__(brand)
        self.doors = doors

    def info(self):
        return f"{super().info()}, Doors: {self.doors}"

if __name__ == "__main__":
    v = Vehicle("Generic")
    print(v.info())

    c = Car("Toyota", 4)
    print(c.info())
    #это способ обратиться к родительскому классу