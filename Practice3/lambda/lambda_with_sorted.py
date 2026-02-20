if __name__ == "__main__":
    nums = [3, -10, 5, -2, 0, 7]
    print(sorted(nums, key=lambda x: abs(x)))

    words = ["game", "code", "python", "java"]
    print(sorted(words, key=lambda w: w[-1]))

    people = [
        {"name": "Andrey", "age": 19},
        {"name": "Ayan", "age": 20},
        {"name": "Dana", "age": 18},
    ]
    print(sorted(people, key=lambda p: p["age"]))

    students = [("Ayan", 90), ("Andrey", 85), ("Dana", 95)]
    print(sorted(students, key=lambda t: t[1], reverse=True))