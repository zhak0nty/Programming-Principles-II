if __name__ == "__main__":
    numbers = [1,2,3,4,5,6,7,8,9,10]
    print(list(filter(lambda x: x % 2 == 0, numbers)))
    print(list(filter(lambda x: x > 5, numbers)))

    words = ["apple", "banana", "apricot", "kiwi", "avocado"]
    print(list(filter(lambda w: w.startswith("a"), words)))

    products = [("Phone", 500), ("Laptop", 1200), ("Mouse", 25)]
    print(list(filter(lambda p: p[1] >= 500, products)))
    #отфильтровать тру го фалс нет