import pygame


def tool_buttons() -> list[tuple[str, pygame.Rect]]:
    buttons = []
    x = 18
    for tool in ("brush", "rectangle", "circle", "eraser"):
        rect = pygame.Rect(x, 14, 128, 34)
        buttons.append((tool, rect))
        x += 140
    return buttons


def color_buttons() -> list[tuple[tuple[int, int, int], pygame.Rect]]:
    palette = [
        (0, 0, 0),
        (230, 50, 50),
        (40, 130, 255),
        (30, 170, 75),
        (252, 180, 40),
        (160, 80, 220),
        (255, 255, 255),
    ]

    buttons = []
    x = 18
    y = 56
    for color in palette:
        rect = pygame.Rect(x, y, 36, 30)
        buttons.append((color, rect))
        x += 48
    return buttons


def canvas_pos(pos: tuple[int, int], toolbar_h: int) -> tuple[int, int]:
    x, y = pos
    return x, y - toolbar_h


def in_canvas(pos: tuple[int, int], width: int, height: int, toolbar_h: int) -> bool:
    x, y = pos
    return 0 <= x < width and toolbar_h <= y < height
