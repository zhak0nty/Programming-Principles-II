from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass

import pygame


@dataclass
class SnakeConfig:
    cell_size: int = 24
    cols: int = 30
    rows: int = 26
    level_step: int = 5


@dataclass
class Food:
    pos: tuple[int, int]
    value: int
    ttl_ms: int
    color: tuple[int, int, int]
    kind: str = "normal"


@dataclass
class PowerUp:
    pos: tuple[int, int]
    kind: str
    spawned_at: int
    ttl_ms: int = 8000


def speed_for_level(level: int) -> int:
    return min(8 + (level - 1) * 2, 24)


def base_walls(cfg: SnakeConfig) -> set[tuple[int, int]]:
    walls = set()
    for x in range(cfg.cols):
        walls.add((x, 0))
        walls.add((x, cfg.rows - 1))
    for y in range(cfg.rows):
        walls.add((0, y))
        walls.add((cfg.cols - 1, y))
    return walls


def rand_free_cell(cfg: SnakeConfig, snake: deque[tuple[int, int]], walls: set[tuple[int, int]], blocked: set[tuple[int, int]]):
    snake_set = set(snake)
    for _ in range(500):
        pos = (random.randint(1, cfg.cols - 2), random.randint(1, cfg.rows - 2))
        if pos in walls or pos in blocked or pos in snake_set:
            continue
        return pos
    return (cfg.cols // 2 + 1, cfg.rows // 2)


def spawn_food(cfg: SnakeConfig, snake, walls, blocked) -> Food:
    pos = rand_free_cell(cfg, snake, walls, blocked)
    v = random.choices([1, 2, 4], weights=[60, 30, 10], k=1)[0]
    style = {1: (7000, (235, 90, 75)), 2: (5500, (110, 170, 255)), 4: (4000, (210, 145, 255))}
    ttl, color = style[v]
    return Food(pos, v, ttl, color, "normal")


def spawn_poison(cfg: SnakeConfig, snake, walls, blocked) -> Food:
    pos = rand_free_cell(cfg, snake, walls, blocked)
    return Food(pos, -2, 6500, (130, 20, 20), "poison")


def spawn_powerup(cfg: SnakeConfig, snake, walls, blocked, now_ms: int) -> PowerUp:
    kind = random.choice(["speed", "slow", "shield"])
    return PowerUp(rand_free_cell(cfg, snake, walls, blocked), kind, now_ms)


def build_obstacles(cfg: SnakeConfig, snake, walls, level: int) -> set[tuple[int, int]]:
    if level < 3:
        return set()
    obstacles = set()
    head = snake[0]
    safe_zone = {head, (head[0] + 1, head[1]), (head[0] - 1, head[1]), (head[0], head[1] + 1), (head[0], head[1] - 1)}
    count = min(6 + (level - 3) * 2, 24)
    for _ in range(500):
        if len(obstacles) >= count:
            break
        p = (random.randint(2, cfg.cols - 3), random.randint(2, cfg.rows - 3))
        if p in walls or p in safe_zone or p in set(snake):
            continue
        obstacles.add(p)
    return obstacles


def new_game_state(username: str, snake_color: tuple[int, int, int]):
    cfg = SnakeConfig()
    cx, cy = cfg.cols // 2, cfg.rows // 2
    snake = deque([(cx, cy), (cx - 1, cy), (cx - 2, cy)])
    walls = base_walls(cfg)
    obstacles = set()
    food = spawn_food(cfg, snake, walls, obstacles)
    return {
        "cfg": cfg,
        "username": username,
        "snake": snake,
        "dir": (1, 0),
        "next_dir": (1, 0),
        "score": 0,
        "level": 1,
        "alive": True,
        "food": food,
        "food_age": 0,
        "poison": None,
        "poison_age": 0,
        "powerup": None,
        "active_power": None,
        "active_until": 0,
        "shield": False,
        "walls": walls,
        "obstacles": obstacles,
        "snake_color": snake_color,
    }


def update_logic(state: dict, dt_ms: int, now_ms: int):
    if not state["alive"]:
        return
    cfg = state["cfg"]
    state["food_age"] += dt_ms
    if state["food_age"] >= state["food"].ttl_ms:
        state["food"] = spawn_food(cfg, state["snake"], state["walls"], state["obstacles"])
        state["food_age"] = 0

    if state["poison"] is None and random.random() < 0.01:
        state["poison"] = spawn_poison(cfg, state["snake"], state["walls"], state["obstacles"])
        state["poison_age"] = 0
    if state["poison"] is not None:
        state["poison_age"] += dt_ms
        if state["poison_age"] >= state["poison"].ttl_ms:
            state["poison"] = None

    if state["powerup"] is None and random.random() < 0.008:
        state["powerup"] = spawn_powerup(cfg, state["snake"], state["walls"], state["obstacles"], now_ms)
    if state["powerup"] is not None and now_ms - state["powerup"].spawned_at >= state["powerup"].ttl_ms:
        state["powerup"] = None

    if state["active_power"] in {"speed", "slow"} and now_ms >= state["active_until"]:
        state["active_power"] = None

    state["dir"] = state["next_dir"]
    dx, dy = state["dir"]
    hx, hy = state["snake"][0]
    new_head = (hx + dx, hy + dy)

    hits_wall = (
        new_head[0] < 0
        or new_head[1] < 0
        or new_head[0] >= cfg.cols
        or new_head[1] >= cfg.rows
        or new_head in state["walls"]
        or new_head in state["obstacles"]
        or new_head in state["snake"]
    )
    if hits_wall:
        if state["shield"]:
            state["shield"] = False
            return
        state["alive"] = False
        return

    state["snake"].appendleft(new_head)

    if new_head == state["food"].pos:
        state["score"] += state["food"].value
        state["food"] = spawn_food(cfg, state["snake"], state["walls"], state["obstacles"])
        state["food_age"] = 0
    elif state["poison"] is not None and new_head == state["poison"].pos:
        state["poison"] = None
        if len(state["snake"]) <= 3:
            state["alive"] = False
            return
        state["snake"].pop()
        state["snake"].pop()
    elif state["powerup"] is not None and new_head == state["powerup"].pos:
        pu = state["powerup"]
        state["powerup"] = None
        if pu.kind == "shield":
            state["shield"] = True
            state["active_power"] = "shield"
            state["active_until"] = 0
        else:
            state["active_power"] = pu.kind
            state["active_until"] = now_ms + 5000
    else:
        state["snake"].pop()

    state["level"] = 1 + state["score"] // cfg.level_step
    state["obstacles"] = build_obstacles(cfg, state["snake"], state["walls"], state["level"])


def draw_game(screen: pygame.Surface, fonts: dict, state: dict, show_grid: bool, personal_best: int):
    cfg = state["cfg"]
    cs = cfg.cell_size
    screen.fill((20, 20, 26))
    if show_grid:
        for x in range(cfg.cols):
            for y in range(cfg.rows):
                pygame.draw.rect(screen, (38, 38, 44), (x * cs, y * cs, cs, cs), 1)

    for wx, wy in state["walls"]:
        pygame.draw.rect(screen, (95, 95, 105), (wx * cs, wy * cs, cs, cs))
    for ox, oy in state["obstacles"]:
        pygame.draw.rect(screen, (125, 85, 60), (ox * cs, oy * cs, cs, cs))

    fx, fy = state["food"].pos
    pygame.draw.rect(screen, state["food"].color, (fx * cs + 4, fy * cs + 4, cs - 8, cs - 8), border_radius=7)
    screen.blit(fonts["small"].render(str(state["food"].value), True, (20, 20, 20)), (fx * cs + 8, fy * cs + 4))

    if state["poison"] is not None:
        px, py = state["poison"].pos
        pygame.draw.rect(screen, state["poison"].color, (px * cs + 4, py * cs + 4, cs - 8, cs - 8), border_radius=7)

    if state["powerup"] is not None:
        ux, uy = state["powerup"].pos
        col = {"speed": (255, 200, 70), "slow": (90, 160, 255), "shield": (130, 255, 170)}[state["powerup"].kind]
        pygame.draw.circle(screen, col, (ux * cs + cs // 2, uy * cs + cs // 2), cs // 2 - 3)

    for i, (sx, sy) in enumerate(state["snake"]):
        c = state["snake_color"] if i == 0 else (max(0, state["snake_color"][0] - 20), max(0, state["snake_color"][1] - 20), max(0, state["snake_color"][2] - 20))
        pygame.draw.rect(screen, c, (sx * cs, sy * cs, cs, cs), border_radius=5)

    hud = f"User: {state['username']}  Score: {state['score']}  Level: {state['level']}  Best: {personal_best}"
    screen.blit(fonts["hud"].render(hud, True, (235, 235, 235)), (10, 8))
    power = "none"
    if state["shield"]:
        power = "shield"
    elif state["active_power"] in {"speed", "slow"}:
        power = state["active_power"]
    screen.blit(fonts["small"].render(f"Power: {power}", True, (210, 210, 220)), (10, 36))
