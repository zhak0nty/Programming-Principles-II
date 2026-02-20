def min_max(numbers: list[int]) -> tuple[int, int]:
    return min(numbers), max(numbers)

def safe_divide(a: float, b: float):
    if b == 0:
        return None
    return a / b

def count_vowels(text: str) -> int:
    vowels = set("aeiouAEIOU")
    return sum(1 for ch in text if ch in vowels)

def average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)

if __name__ == "__main__":
    nums = [10, 3, 99, 25, -4]
    print(min_max(nums))
    print(safe_divide(10, 2))
    print(safe_divide(10, 0))
    print(count_vowels("Programming"))
    scores = [80.0, 90.0, 75.0, 95.0]
    print(average(scores))