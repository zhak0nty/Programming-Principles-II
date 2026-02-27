if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    print(list(map(lambda x: x * x, numbers)))

    texts = ["10", "20", "30"]
    print(list(map(lambda s: int(s), texts)))

    print(list(map(lambda x: x + 10, numbers)))

    students = [("Ayan", 90), ("Andrey", 85), ("Dana", 95)]
    print(list(map(lambda t: t[0], students)))
    #изменить данные