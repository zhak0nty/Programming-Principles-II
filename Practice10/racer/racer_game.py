import random
from dataclasses import dataclass

import pygame


@dataclass
class LaneObject:
    x: int
    y: float
    speed: float


@dataclass
class RacerConfig:
    width: int = 480
    height: int = 720
    road_left: int = 90
    road_right: int = 390
    lane_count: int = 3
    player_w: int = 58
    player_h: int = 98
    enemy_w: int = 58
    enemy_h: int = 98
    coin_size: int = 30


def lane_width(config: RacerConfig) -> int:
    return (config.road_right - config.road_left) // config.lane_count


def lane_center(config: RacerConfig, lane_idx: int) -> int:
    return config.road_left + lane_idx * lane_width(config) + lane_width(config) // 2


def spawn_enemy(config: RacerConfig, speed: float) -> LaneObject:
    lane = random.randint(0, config.lane_count - 1)
    return LaneObject(lane_center(config, lane), -config.enemy_h, speed)


def spawn_coin(config: RacerConfig, speed: float) -> LaneObject:
    lane = random.randint(0, config.lane_count - 1)
    return LaneObject(lane_center(config, lane), -config.coin_size, speed)


def car_rect(center_x: int, y: float, w: int, h: int) -> pygame.Rect:
    return pygame.Rect(int(center_x - w // 2), int(y), w, h)


def draw_road(screen: pygame.Surface, config: RacerConfig, bg_offset: int) -> None:
    screen.fill((24, 140, 55))
    pygame.draw.rect(
        screen,
        (60, 60, 60),
        (config.road_left, 0, config.road_right - config.road_left, config.height),
    )

    for lane in range(1, config.lane_count):
        x = config.road_left + lane * lane_width(config)
        pygame.draw.line(screen, (235, 235, 0), (x, 0), (x, config.height), 3)

    center_x = (config.road_left + config.road_right) // 2
    for y in range(-80, config.height + 80, 80):
        yy = y + bg_offset
        pygame.draw.rect(screen, (250, 250, 250), (center_x - 4, yy, 8, 44))


def draw_car(screen: pygame.Surface, rect: pygame.Rect, body_color: tuple[int, int, int]) -> None:
    pygame.draw.rect(screen, body_color, rect, border_radius=12)
    windshield = pygame.Rect(rect.x + 10, rect.y + 12, rect.width - 20, 24)
    pygame.draw.rect(screen, (175, 220, 255), windshield, border_radius=8)

    wheels = [
        pygame.Rect(rect.x - 2, rect.y + 10, 8, 18),
        pygame.Rect(rect.right - 6, rect.y + 10, 8, 18),
        pygame.Rect(rect.x - 2, rect.bottom - 30, 8, 18),
        pygame.Rect(rect.right - 6, rect.bottom - 30, 8, 18),
    ]
    for wheel in wheels:
        pygame.draw.rect(screen, (20, 20, 20), wheel, border_radius=3)
