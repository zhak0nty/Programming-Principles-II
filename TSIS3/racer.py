import random
from dataclasses import dataclass

import pygame


@dataclass
class Config:
    width: int = 520
    height: int = 760
    road_left: int = 90
    road_right: int = 430
    lane_count: int = 3
    player_w: int = 58
    player_h: int = 98
    traffic_w: int = 58
    traffic_h: int = 98
    finish_distance: int = 3000


CAR_COLORS = {
    "blue": (60, 130, 240),
    "green": (45, 180, 110),
    "orange": (245, 145, 50),
}
DIFFICULTY_FACTOR = {"easy": 0.85, "normal": 1.0, "hard": 1.2}


def lane_width(cfg: Config) -> int:
    return (cfg.road_right - cfg.road_left) // cfg.lane_count


def lane_center(cfg: Config, lane: int) -> int:
    return cfg.road_left + lane * lane_width(cfg) + lane_width(cfg) // 2


def car_rect(center_x: int, y: float, w: int, h: int) -> pygame.Rect:
    return pygame.Rect(int(center_x - w // 2), int(y), w, h)


def draw_car(screen: pygame.Surface, rect: pygame.Rect, body_color):
    pygame.draw.rect(screen, body_color, rect, border_radius=12)
    pygame.draw.rect(screen, (185, 225, 255), (rect.x + 10, rect.y + 12, rect.width - 20, 24), border_radius=8)
    for wheel in (
        pygame.Rect(rect.x - 2, rect.y + 10, 8, 18),
        pygame.Rect(rect.right - 6, rect.y + 10, 8, 18),
        pygame.Rect(rect.x - 2, rect.bottom - 30, 8, 18),
        pygame.Rect(rect.right - 6, rect.bottom - 30, 8, 18),
    ):
        pygame.draw.rect(screen, (20, 20, 20), wheel, border_radius=3)


def draw_road(screen: pygame.Surface, cfg: Config, offset: int):
    screen.fill((24, 140, 55))
    pygame.draw.rect(screen, (60, 60, 60), (cfg.road_left, 0, cfg.road_right - cfg.road_left, cfg.height))
    for lane in range(1, cfg.lane_count):
        x = cfg.road_left + lane * lane_width(cfg)
        pygame.draw.line(screen, (235, 235, 0), (x, 0), (x, cfg.height), 3)
    center_x = (cfg.road_left + cfg.road_right) // 2
    for y in range(-80, cfg.height + 80, 80):
        pygame.draw.rect(screen, (250, 250, 250), (center_x - 4, y + offset, 8, 44))


def make_game_state(settings: dict):
    return {
        "cfg": Config(),
        "lane": 1,
        "player_y": 760 - 98 - 30,
        "coins": 0,
        "distance": 0,
        "score": 0,
        "speed_level": 0,
        "alive": True,
        "road_offset": 0,
        "traffic": [],
        "hazards": [],
        "coins_obj": [],
        "powerups": [],
        "active_powerup": None,
        "powerup_left_ms": 0,
        "difficulty": settings["difficulty"],
        "car_color": settings["car_color"],
        "event_timer": 0,
        "event_type": "",
    }


def spawn_in_lane(cfg: Config, y: float, speed: float):
    lane = random.randint(0, cfg.lane_count - 1)
    return {"lane": lane, "x": lane_center(cfg, lane), "y": y, "speed": speed}


def safe_spawn(state: dict, obj: dict) -> bool:
    if obj["lane"] == state["lane"] and obj["y"] > -190:
        return False
    return True


def maybe_spawn_entities(state: dict):
    cfg = state["cfg"]
    diff = DIFFICULTY_FACTOR[state["difficulty"]]
    level = state["speed_level"]
    if random.random() < min(0.02 + level * 0.002, 0.09) * diff:
        obj = spawn_in_lane(cfg, -cfg.traffic_h - random.randint(0, 200), 5.5 + level * 0.12)
        if safe_spawn(state, obj):
            state["traffic"].append(obj)
    if random.random() < min(0.015 + level * 0.0025, 0.08) * diff:
        obj = spawn_in_lane(cfg, -60 - random.randint(0, 200), 4.5 + level * 0.1)
        if safe_spawn(state, obj):
            obj["kind"] = random.choice(["barrier", "oil", "pothole", "slow"])
            state["hazards"].append(obj)
    if random.random() < 0.028:
        obj = spawn_in_lane(cfg, -40 - random.randint(0, 260), 6.5)
        if safe_spawn(state, obj):
            obj["value"] = random.choices([1, 2, 5], weights=[65, 25, 10], k=1)[0]
            state["coins_obj"].append(obj)
    if state["active_powerup"] is None and random.random() < 0.005:
        obj = spawn_in_lane(cfg, -50 - random.randint(0, 240), 5.8)
        if safe_spawn(state, obj):
            obj["kind"] = random.choice(["nitro", "shield", "repair"])
            obj["ttl"] = 4200
            state["powerups"].append(obj)


def update_game(state: dict, dt: int):
    if not state["alive"]:
        return
    cfg = state["cfg"]
    state["distance"] += max(1, dt // 16)
    state["road_offset"] = (state["road_offset"] + 10) % 80
    state["speed_level"] = state["distance"] // 400
    maybe_spawn_entities(state)
    if state["active_powerup"] == "nitro":
        state["powerup_left_ms"] -= dt
        if state["powerup_left_ms"] <= 0:
            state["active_powerup"] = None
    player = car_rect(lane_center(cfg, state["lane"]), state["player_y"], cfg.player_w, cfg.player_h)

    def move(items, base_speed):
        res = []
        for obj in items:
            bonus = 2 if state["active_powerup"] == "nitro" else 0
            obj["y"] += obj["speed"] + base_speed + bonus
            if obj["y"] < cfg.height + 100:
                res.append(obj)
        return res

    flow = 0.8 + state["speed_level"] * 0.05
    state["traffic"] = move(state["traffic"], flow)
    state["hazards"] = move(state["hazards"], flow)
    state["coins_obj"] = move(state["coins_obj"], flow)

    kept_power = []
    for p in state["powerups"]:
        p["y"] += p["speed"] + flow
        p["ttl"] -= dt
        if p["y"] < cfg.height + 80 and p["ttl"] > 0:
            kept_power.append(p)
    state["powerups"] = kept_power

    for t in state["traffic"]:
        if player.colliderect(car_rect(t["x"], t["y"], cfg.traffic_w, cfg.traffic_h)):
            if state["active_powerup"] == "shield":
                state["active_powerup"] = None
                continue
            state["alive"] = False
            return

    next_h = []
    for h in state["hazards"]:
        h_rect = pygame.Rect(int(h["x"] - 24), int(h["y"]), 48, 28)
        if player.colliderect(h_rect):
            if state["active_powerup"] == "shield":
                state["active_powerup"] = None
                continue
            if h["kind"] == "slow":
                state["distance"] = max(0, state["distance"] - 20)
            elif h["kind"] in {"barrier", "pothole"}:
                state["alive"] = False
                return
        else:
            next_h.append(h)
    state["hazards"] = next_h

    next_c = []
    for c in state["coins_obj"]:
        c_rect = pygame.Rect(int(c["x"] - 16), int(c["y"]), 32, 32)
        if player.colliderect(c_rect):
            state["coins"] += c["value"]
        else:
            next_c.append(c)
    state["coins_obj"] = next_c

    next_p = []
    for p in state["powerups"]:
        p_rect = pygame.Rect(int(p["x"] - 18), int(p["y"]), 36, 36)
        if player.colliderect(p_rect):
            if state["active_powerup"] is None:
                state["active_powerup"] = p["kind"]
                if p["kind"] == "nitro":
                    state["powerup_left_ms"] = random.randint(3000, 5000)
                elif p["kind"] == "shield":
                    state["powerup_left_ms"] = 999999
                elif p["kind"] == "repair":
                    state["distance"] += 60
                    state["active_powerup"] = None
            else:
                next_p.append(p)
        else:
            next_p.append(p)
    state["powerups"] = next_p

    state["score"] = state["coins"] * 10 + state["distance"] + (120 if state["active_powerup"] == "nitro" else 0)


def draw_game(screen: pygame.Surface, fonts: dict, state: dict):
    cfg = state["cfg"]
    draw_road(screen, cfg, state["road_offset"])
    player = car_rect(lane_center(cfg, state["lane"]), state["player_y"], cfg.player_w, cfg.player_h)
    draw_car(screen, player, CAR_COLORS[state["car_color"]])

    for t in state["traffic"]:
        draw_car(screen, car_rect(t["x"], t["y"], cfg.traffic_w, cfg.traffic_h), (235, 65, 65))
    for h in state["hazards"]:
        rect = pygame.Rect(int(h["x"] - 24), int(h["y"]), 48, 28)
        color = {"barrier": (220, 110, 20), "oil": (25, 25, 25), "pothole": (90, 60, 45), "slow": (120, 140, 255)}[h["kind"]]
        pygame.draw.rect(screen, color, rect, border_radius=6)
    for c in state["coins_obj"]:
        color = {1: (235, 185, 30), 2: (170, 210, 255), 5: (210, 140, 255)}[c["value"]]
        pygame.draw.circle(screen, color, (int(c["x"]), int(c["y"]) + 16), 16)
    for p in state["powerups"]:
        color = {"nitro": (50, 210, 255), "shield": (120, 255, 180), "repair": (255, 170, 80)}[p["kind"]]
        pygame.draw.circle(screen, color, (int(p["x"]), int(p["y"]) + 18), 18)

    pygame.draw.rect(screen, (0, 0, 0, 80), (0, 0, cfg.width, 100))
    screen.blit(fonts["normal"].render(f"Coins: {state['coins']}", True, (255, 255, 255)), (16, 12))
    screen.blit(fonts["normal"].render(f"Score: {state['score']}", True, (255, 255, 255)), (16, 40))
    rem = max(0, cfg.finish_distance - state["distance"])
    screen.blit(fonts["small"].render(f"Distance: {state['distance']} | Remaining: {rem}", True, (235, 235, 235)), (16, 70))
    ptxt = state["active_powerup"] or "none"
    if state["active_powerup"] == "nitro":
        ptxt += f" ({max(0, state['powerup_left_ms']) // 1000}s)"
    elif state["active_powerup"] == "shield":
        ptxt += " (until hit)"
    screen.blit(fonts["small"].render(f"Power-up: {ptxt}", True, (255, 240, 170)), (300, 12))
