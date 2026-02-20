class Person:
    species = "Human"

    def __init__(self, name):
        self.name = name

    def say_hi(self):
        print(f"Hi, I'm {self.name}.")

    @classmethod
    def change_species(cls, new_species):
        cls.species = new_species

    @staticmethod
    def is_adult(age):
        return age >= 18

if __name__ == "__main__":
    p = Person("Andrey")
    p.say_hi()
    print(Person.species)
    Person.change_species("Homo sapiens")
    print(Person.species)
    print(Person.is_adult(17))
    print(Person.is_adult(19))