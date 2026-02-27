if __name__ == "__main__":
    square = lambda x: x * x
    print(square(5))

    add = lambda a, b: a + b
    print(add(10, 7))

    def multiplier(k: int):
        return lambda x: x * k

    times3 = multiplier(3)
    print(times3(8))

    words = ["banana", "kiwi", "strawberry", "fig"]
    print(sorted(words, key=lambda w: len(w)))
    #функция в одну строку без имени