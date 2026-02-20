def rectangle_area(width: float, height: float) -> float:
    return width * height

def power(base: float, exponent: int = 2) -> float:
    return base ** exponent

def format_full_name(first_name: str, last_name: str, middle_name: str = "") -> str:
    middle = f" {middle_name}" if middle_name else ""
    return f"{last_name} {first_name}{middle}"

def make_email(username: str, domain: str = "gmail.com") -> str:
    return f"{username}@{domain}"

if __name__ == "__main__":
    print(rectangle_area(5, 3))
    print(rectangle_area(height=2, width=7))
    print(power(4))
    print(power(4, 3))
    print(format_full_name("Andrey", "Kudryakov"))
    print(format_full_name("Andrey", "Kudryakov", middle_name="Vasilievich"))
    print(make_email("zhak0nty"))
    print(make_email("zhak0nty", domain="kbtu.kz"))