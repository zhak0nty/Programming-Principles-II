def sum_all(*args: float) -> float:
    return sum(args)

def print_info(**kwargs):
    for key, value in kwargs.items():
        print(key, value)

def order_total(price: float, *discounts: float, **extras: float) -> float:
    total = price
    for d in discounts:
        total *= (1 - d)
    total += sum(extras.values())
    return total

def merge_lists(*lists: list[int]) -> list[int]:
    result = []
    for lst in lists:
        result.extend(lst)
    return result

if __name__ == "__main__":
    print(sum_all(1, 2, 3))
    print(sum_all(10, 0.5, 2.5))
    print_info(name="Andrey", city="Almaty", major="Information Systems")
    print(order_total(10000, 0.10, 0.05, delivery=500, tip=200))
    print(merge_lists([1, 2], [10, 20, 30], [-1]))