from __future__ import annotations

import json
from pathlib import Path

import pygame

from db import fetch_personal_best, fetch_top10, init_db, save_game_result
from game import draw_game, new_game_state, speed_for_level, update_logic


def load_settings(path: Path):
    defaults = {"snake_color": [58, 210, 82], "grid": True, "sound": True}
    if not path.exists():
        return defaults
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return defaults
        defaults.update(data)
        return defaults
    except (json.JSONDecodeError, OSError):
        return defaults


def save_settings(path: Path, settings: dict):
    path.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")


def draw_button(screen, rect, text, font):
    hov = rect.collidepoint(pygame.mouse.get_pos())
    pygame.draw.rect(screen, (170, 210, 255) if hov else (238, 238, 244), rect, border_radius=8)
    pygame.draw.rect(screen, (70, 70, 85), rect, 2, border_radius=8)
    surf = font.render(text, True, (20, 20, 30))
    screen.blit(surf, surf.get_rect(center=rect.center))


def main():
    pygame.init()
    cfg_cols, cfg_rows, cell = 30, 26, 24
    width, height = cfg_cols * cell, cfg_rows * cell
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("TSIS4 Snake")
    clock = pygame.time.Clock()
    fonts = {
        "title": pygame.font.SysFont("arial", 42, bold=True),
        "menu": pygame.font.SysFont("arial", 26),
        "hud": pygame.font.SysFont("consolas", 22),
        "small": pygame.font.SysFont("arial", 18),
    }

    base = Path(__file__).resolve().parent
    settings_path = base / "settings.json"
    settings = load_settings(settings_path)
    snake_color = tuple(settings["snake_color"])

    db_ok = True
    try:
        init_db()
    except Exception:
        db_ok = False

    state = "menu"
    username = ""
    game = None
    personal_best = 0
    leaderboard = []
    saved_once = False

    menu_buttons = [("Play", pygame.Rect(width // 2 - 120, 230, 240, 50)), ("Leaderboard", pygame.Rect(width // 2 - 120, 290, 240, 50)), ("Settings", pygame.Rect(width // 2 - 120, 350, 240, 50)), ("Quit", pygame.Rect(width // 2 - 120, 410, 240, 50))]
    back_rect = pygame.Rect(width // 2 - 120, height - 80, 240, 50)
    save_back_rect = pygame.Rect(width // 2 - 140, height - 90, 280, 52)
    retry_rect = pygame.Rect(width // 2 - 140, 360, 130, 50)
    menu_rect = pygame.Rect(width // 2 + 10, 360, 130, 50)

    running = True
    while running:
        now = pygame.time.get_ticks()
        fps = 12 if game is None else speed_for_level(game["level"])
        if game and game["active_power"] == "speed":
            fps += 4
        elif game and game["active_power"] == "slow":
            fps = max(6, fps - 4)
        dt = clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif state == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == pygame.K_RETURN and username.strip():
                        username = username.strip()
                    elif event.unicode and event.unicode.isprintable() and len(username) < 20:
                        username += event.unicode
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for label, rect in menu_buttons:
                        if rect.collidepoint(event.pos):
                            if label == "Play":
                                if not username.strip():
                                    username = "Player"
                                game = new_game_state(username.strip(), snake_color)
                                saved_once = False
                                if db_ok:
                                    try:
                                        personal_best = fetch_personal_best(username.strip())
                                    except Exception:
                                        personal_best = 0
                                else:
                                    personal_best = 0
                                state = "game"
                            elif label == "Leaderboard":
                                if db_ok:
                                    try:
                                        leaderboard = fetch_top10()
                                    except Exception:
                                        leaderboard = []
                                else:
                                    leaderboard = []
                                state = "leaderboard"
                            elif label == "Settings":
                                state = "settings"
                            else:
                                running = False
            elif state == "settings" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.Rect(120, 180, 420, 48).collidepoint(event.pos):
                    settings["grid"] = not settings["grid"]
                elif pygame.Rect(120, 250, 420, 48).collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                elif pygame.Rect(120, 320, 420, 48).collidepoint(event.pos):
                    palette = [[58, 210, 82], [80, 165, 255], [245, 160, 70], [210, 120, 255]]
                    idx = palette.index(settings["snake_color"]) if settings["snake_color"] in palette else 0
                    settings["snake_color"] = palette[(idx + 1) % len(palette)]
                elif save_back_rect.collidepoint(event.pos):
                    save_settings(settings_path, settings)
                    snake_color = tuple(settings["snake_color"])
                    state = "menu"
            elif state == "leaderboard" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_rect.collidepoint(event.pos):
                    state = "menu"
            elif state == "game":
                if event.type == pygame.KEYDOWN:
                    mapping = {pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1), pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}
                    if event.key in mapping:
                        nd = mapping[event.key]
                        d = game["dir"]
                        if not (nd[0] == -d[0] and nd[1] == -d[1]):
                            game["next_dir"] = nd
                    elif event.key == pygame.K_ESCAPE:
                        state = "menu"
            elif state == "game_over" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if retry_rect.collidepoint(event.pos):
                    game = new_game_state(username.strip() or "Player", snake_color)
                    saved_once = False
                    state = "game"
                elif menu_rect.collidepoint(event.pos):
                    state = "menu"

        if state == "menu":
            screen.fill((20, 24, 34))
            screen.blit(fonts["title"].render("TSIS4 Snake", True, (255, 255, 255)), (width // 2 - 130, 100))
            prompt = "Enter username:"
            screen.blit(fonts["menu"].render(prompt, True, (220, 220, 235)), (width // 2 - 140, 170))
            pygame.draw.rect(screen, (245, 245, 250), (width // 2 - 140, 198, 280, 42), border_radius=6)
            pygame.draw.rect(screen, (80, 80, 95), (width // 2 - 140, 198, 280, 42), 2, border_radius=6)
            screen.blit(fonts["menu"].render((username or "") + "|", True, (20, 20, 30)), (width // 2 - 130, 206))
            for label, rect in menu_buttons:
                draw_button(screen, rect, label, fonts["menu"])
            if not db_ok:
                screen.blit(fonts["small"].render("DB unavailable: leaderboard disabled", True, (255, 180, 180)), (width // 2 - 150, height - 30))

        elif state == "settings":
            screen.fill((24, 28, 36))
            screen.blit(fonts["title"].render("Settings", True, (255, 255, 255)), (width // 2 - 95, 90))
            rows = [
                (f"Grid overlay: {'ON' if settings['grid'] else 'OFF'}", pygame.Rect(120, 180, 420, 48)),
                (f"Sound: {'ON' if settings['sound'] else 'OFF'}", pygame.Rect(120, 250, 420, 48)),
                ("Snake color: click to cycle", pygame.Rect(120, 320, 420, 48)),
            ]
            for text, rect in rows:
                draw_button(screen, rect, text, fonts["menu"])
            col = tuple(settings["snake_color"])
            pygame.draw.rect(screen, col, (540, 320, 40, 40), border_radius=5)
            draw_button(screen, save_back_rect, "Save & Back", fonts["menu"])

        elif state == "leaderboard":
            screen.fill((18, 22, 30))
            screen.blit(fonts["title"].render("Leaderboard Top 10", True, (255, 255, 255)), (100, 70))
            y = 140
            if not leaderboard:
                screen.blit(fonts["menu"].render("No data", True, (210, 210, 225)), (width // 2 - 40, y))
            else:
                for i, row in enumerate(leaderboard, start=1):
                    line = f"{i:>2}. {row['username']:<12} score={row['score']:<5} level={row['level_reached']}  {row['played_at']}"
                    screen.blit(fonts["small"].render(line, True, (220, 220, 235)), (40, y))
                    y += 34
            draw_button(screen, back_rect, "Back", fonts["menu"])

        elif state == "game":
            update_logic(game, dt, now)
            draw_game(screen, fonts, game, settings["grid"], personal_best)
            if (not game["alive"]) and (not saved_once):
                saved_once = True
                if db_ok:
                    try:
                        save_game_result(game["username"], game["score"], game["level"])
                        personal_best = max(personal_best, game["score"])
                    except Exception:
                        pass
                state = "game_over"

        elif state == "game_over":
            draw_game(screen, fonts, game, settings["grid"], personal_best)
            ov = pygame.Surface((width, height), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 165))
            screen.blit(ov, (0, 0))
            screen.blit(fonts["title"].render("Game Over", True, (255, 255, 255)), (width // 2 - 120, 180))
            screen.blit(fonts["menu"].render(f"Score: {game['score']}  Level: {game['level']}  Personal best: {personal_best}", True, (235, 235, 235)), (width // 2 - 240, 250))
            draw_button(screen, retry_rect, "Retry", fonts["menu"])
            draw_button(screen, menu_rect, "Main Menu", fonts["menu"])

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
