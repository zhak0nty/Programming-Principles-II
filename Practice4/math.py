import math


def deg_to_rad(deg: float) -> float:
    return deg * math.pi / 180.0


def area_trapezoid(h: float, a: float, b: float) -> float:
    return (a + b) * h / 2.0


def area_regular_polygon(n: int, s: float) -> float:
    # area = (n * s^2) / (4 * tan(pi/n))
    return (n * (s ** 2)) / (4.0 * math.tan(math.pi / n))


def area_parallelogram(base: float, height: float) -> float:
    return base * height


if __name__ == "__main__":
    # 1
    deg = float(input().strip())
    print(deg_to_rad(deg))

    # 2
    h = float(input().strip())
    a = float(input().strip())
    b = float(input().strip())
    print(area_trapezoid(h, a, b))

    # 3
    n = int(input().strip())
    s = float(input().strip())
    print(area_regular_polygon(n, s))

    # 4
    base = float(input().strip())
    height = float(input().strip())
    print(area_parallelogram(base, height))