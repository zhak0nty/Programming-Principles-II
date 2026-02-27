def squares_up_to_n(n: int):   
    for i in range(1, n + 1):
        yield i * i


def even_numbers_0_to_n(n: int):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield i


def divisible_by_3_and_4(n: int):
    for i in range(0, n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


def squares(a: int, b: int):
    step = 1 if a <= b else -1
    x = a
    while True:
        yield x * x
        if x == b:
            break
        x += step


def countdown(n: int):
    for i in range(n, -1, -1):
        yield i


if __name__ == "__main__":
    # 1
    n = int(input().strip())
    print(*squares_up_to_n(n), sep=" ")

    # 2
    n = int(input().strip())
    print(",".join(map(str, even_numbers_0_to_n(n))))

    # 3
    n = int(input().strip())
    print(*divisible_by_3_and_4(n), sep=" ")

    # 4
    a = int(input().strip())
    b = int(input().strip())
    for val in squares(a, b):
        print(val)

    # 5
    n = int(input().strip())
    for val in countdown(n):
        print(val)