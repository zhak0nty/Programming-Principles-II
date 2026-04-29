import math
from collections import deque
from datetime import datetime
from pathlib import Path

import pygame


def make_tool_buttons() -> list[tuple[str, pygame.Rect]]:
    tools = [
        "pencil",
        "line",
        "rectangle",
        "circle",
        "square",
        "right_triangle",
        "equilateral_triangle",
        "rhombus",
        "fill",
        "text",
        "eraser",
    ]
    buttons = []
    x, y = 12, 10
    for tool in tools:
        w = 116 if len(tool) < 10 else 165
        rect = pygame.Rect(x, y, w, 32)
        buttons.append((tool, rect))
        x += w + 8
        if x > 1180:
            x, y = 12, y + 38
    return buttons


def make_size_buttons() -> list[tuple[int, pygame.Rect]]:
    sizes = [2, 5, 10]
    buttons = []
    x = 12
    for size in sizes:
        buttons.append((size, pygame.Rect(x, 90, 64, 32)))
        x += 72
    return buttons


def make_color_buttons() -> list[tuple[tuple[int, int, int], pygame.Rect]]:
    palette = [
        (0, 0, 0),
        (230, 50, 50),
        (40, 130, 255),
        (30, 170, 75),
        (252, 180, 40),
        (160, 80, 220),
        (255, 140, 0),
        (255, 255, 255),
    ]
    buttons = []
    x = 320
    for color in palette:
        buttons.append((color, pygame.Rect(x, 90, 36, 32)))
        x += 44
    return buttons


def in_canvas(pos: tuple[int, int], width: int, height: int, toolbar_h: int) -> bool:
    return 0 <= pos[0] < width and toolbar_h <= pos[1] < height


def to_canvas(pos: tuple[int, int], toolbar_h: int) -> tuple[int, int]:
    return pos[0], pos[1] - toolbar_h


def square_rect(start: tuple[int, int], end: tuple[int, int]) -> pygame.Rect:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    side = min(abs(dx), abs(dy))
    sx = start[0] if dx >= 0 else start[0] - side
    sy = start[1] if dy >= 0 else start[1] - side
    return pygame.Rect(sx, sy, side, side)


def rectangle_rect(start: tuple[int, int], end: tuple[int, int]) -> pygame.Rect:
    return pygame.Rect(
        min(start[0], end[0]),
        min(start[1], end[1]),
        abs(end[0] - start[0]),
        abs(end[1] - start[1]),
    )


def circle_radius(start: tuple[int, int], end: tuple[int, int]) -> int:
    return int(math.hypot(end[0] - start[0], end[1] - start[1]))


def right_triangle_points(start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    return [start, (start[0], end[1]), end]


def equilateral_triangle_points(start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    side = max(1, abs(end[0] - start[0]))
    direction = 1 if end[1] >= start[1] else -1
    height = int((math.sqrt(3) / 2) * side)
    p1 = (start[0], start[1])
    p2 = (start[0] + side, start[1])
    p3 = (start[0] + side // 2, start[1] + direction * height)
    return [p1, p2, p3]


def rhombus_points(start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    cx = (start[0] + end[0]) // 2
    cy = (start[1] + end[1]) // 2
    dx = abs(end[0] - start[0]) // 2
    dy = abs(end[1] - start[1]) // 2
    return [(cx, cy - dy), (cx + dx, cy), (cx, cy + dy), (cx - dx, cy)]


def flood_fill(surface: pygame.Surface, start: tuple[int, int], new_color: tuple[int, int, int]) -> None:
    width, height = surface.get_size()
    x, y = start
    if not (0 <= x < width and 0 <= y < height):
        return

    target = surface.get_at((x, y))
    replacement = pygame.Color(*new_color)
    if target == replacement:
        return

    q = deque([(x, y)])
    while q:
        cx, cy = q.popleft()
        if cx < 0 or cy < 0 or cx >= width or cy >= height:
            continue
        if surface.get_at((cx, cy)) != target:
            continue
        surface.set_at((cx, cy), replacement)
        q.append((cx + 1, cy))
        q.append((cx - 1, cy))
        q.append((cx, cy + 1))
        q.append((cx, cy - 1))


def save_canvas_png(canvas: pygame.Surface, base_dir: Path) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = base_dir / f"canvas_{stamp}.png"
    pygame.image.save(canvas, path)
    return path
