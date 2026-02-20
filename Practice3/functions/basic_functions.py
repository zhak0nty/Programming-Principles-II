def greet(name: str) -> None:
    print(f"Hello, {name}!")

def add(a: int, b: int) -> int:
    return a + b

def is_even(n: int) -> bool:
    return n % 2 == 0

def reverse_text(text: str) -> str:
    return text[::-1]

if __name__ == "__main__":
    greet("Andrey")
    print(add(10, 25))
    print(is_even(42))
    print(is_even(19))
    print(reverse_text("python"))