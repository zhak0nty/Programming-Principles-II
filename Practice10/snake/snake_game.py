import random
from collections import deque
from dataclasses import dataclass

import pygame


@dataclass
class SnakeConfig:
    cell_size: int = 24
    cols: int = 28
    rows: int = 24


@dataclass
class LevelInfo:
    level: int
    foods_to_next_level: int
    speed_fps: int


def build_walls(config: SnakeConfig) -> set[tuple[int, int]]:
    walls: set[tuple[int, int]] = set()
    for x in range(config.cols):
        walls.add((x, 0))
        walls.add((x, config.rows - 1))
    for y in range(config.rows):
        walls.add((0, y))
        walls.add((config.cols - 1, y))

    for y in range(4, config.rows - 4):
        if y not in (config.rows // 2 - 1, config.rows // 2, config.rows // 2 + 1):
            walls.add((config.cols // 3, y))
            walls.add((2 * config.cols // 3, y))
    return walls


def level_info(score: int) -> LevelInfo:
    level = 1 + score // 4
    speed = min(10 + (level - 1) * 2, 26)
    foods_to_next = 4 - (score % 4)
    return LevelInfo(level=level, foods_to_next_level=foods_to_next, speed_fps=speed)


def spawn_food(config: SnakeConfig, snake: deque[tuple[int, int]], walls: set[tuple[int, int]]) -> tuple[int, int]:
    snake_set = set(snake)
    while True:
        pos = (random.randint(1, config.cols - 2), random.randint(1, config.rows - 2))
        if pos in walls or pos in snake_set:
            continue
        return pos


def draw_grid(screen: pygame.Surface, config: SnakeConfig) -> None:
    screen.fill((20, 20, 26))
    for x in range(config.cols):
        for y in range(config.rows):
            rect = pygame.Rect(
                x * config.cell_size,
                y * config.cell_size,
                config.cell_size,
                config.cell_size,
            )
            pygame.draw.rect(screen, (38, 38, 44), rect, 1)
