from pathlib import Path
import pygame
from persistence import add_leaderboard_entry, load_leaderboard, load_settings, save_settings
from racer import draw_game, make_game_state, update_game
from ui import draw_leaderboard, draw_menu, draw_name_input, draw_settings

pygame.init()
screen = pygame.display.set_mode((520, 760))
pygame.display.set_caption("TSIS3 Racer")
clock = pygame.time.Clock()
fonts = {
    "title": pygame.font.SysFont("arial", 44, bold=True),
    "normal": pygame.font.SysFont("arial", 28),
    "small": pygame.font.SysFont("arial", 22),
}

base = Path(__file__).resolve().parent
settings_path = base / "settings.json"
leaderboard_path = base / "leaderboard.json"
settings = load_settings(settings_path)
leaderboard = load_leaderboard(leaderboard_path)

screen_state = "name_input"
username = ""
game = None
result = {"score": 0, "distance": 0, "coins": 0}

menu_buttons = [("Play", pygame.Rect(140, 220, 240, 52)), ("Leaderboard", pygame.Rect(140, 290, 240, 52)), ("Settings", pygame.Rect(140, 360, 240, 52)), ("Quit", pygame.Rect(140, 430, 240, 52))]
settings_buttons = [("Toggle sound", pygame.Rect(120, 180, 260, 50)), ("Change car color", pygame.Rect(120, 260, 260, 50)), ("Change difficulty", pygame.Rect(120, 340, 260, 50))]
back_rect = pygame.Rect(140, 680, 240, 52)
retry_rect = pygame.Rect(120, 560, 130, 52)
menu_rect = pygame.Rect(270, 560, 130, 52)

running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if screen_state == "name_input" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                username = username.strip() or "Player"
                screen_state = "menu"
            elif event.key == pygame.K_BACKSPACE:
                username = username[:-1]
            elif event.unicode and event.unicode.isprintable() and len(username) < 18:
                username += event.unicode
        elif screen_state == "menu" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for label, rect in menu_buttons:
                if rect.collidepoint(event.pos):
                    if label == "Play":
                        game = make_game_state(settings)
                        screen_state = "game"
                    elif label == "Leaderboard":
                        leaderboard = load_leaderboard(leaderboard_path)
                        screen_state = "leaderboard"
                    elif label == "Settings":
                        screen_state = "settings"
                    else:
                        running = False
        elif screen_state == "settings" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if settings_buttons[0][1].collidepoint(event.pos):
                settings["sound"] = not settings["sound"]
            elif settings_buttons[1][1].collidepoint(event.pos):
                colors = ["blue", "green", "orange"]
                settings["car_color"] = colors[(colors.index(settings["car_color"]) + 1) % 3]
            elif settings_buttons[2][1].collidepoint(event.pos):
                levels = ["easy", "normal", "hard"]
                settings["difficulty"] = levels[(levels.index(settings["difficulty"]) + 1) % 3]
            elif back_rect.collidepoint(event.pos):
                save_settings(settings_path, settings)
                screen_state = "menu"
        elif screen_state == "leaderboard" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if back_rect.collidepoint(event.pos):
                screen_state = "menu"
        elif screen_state == "game" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game["lane"] = max(0, game["lane"] - 1)
            elif event.key == pygame.K_RIGHT:
                game["lane"] = min(game["cfg"].lane_count - 1, game["lane"] + 1)
            elif event.key == pygame.K_ESCAPE:
                screen_state = "menu"
        elif screen_state == "game_over" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if retry_rect.collidepoint(event.pos):
                game = make_game_state(settings)
                screen_state = "game"
            elif menu_rect.collidepoint(event.pos):
                screen_state = "menu"

    if screen_state == "name_input":
        draw_name_input(screen, fonts, username)
    elif screen_state == "menu":
        draw_menu(screen, fonts, username or "Player", menu_buttons)
    elif screen_state == "settings":
        draw_settings(screen, fonts, settings, settings_buttons, back_rect)
    elif screen_state == "leaderboard":
        draw_leaderboard(screen, fonts, leaderboard, back_rect)
    elif screen_state == "game":
        update_game(game, dt)
        draw_game(screen, fonts, game)
        if (not game["alive"]) or game["distance"] >= game["cfg"].finish_distance:
            result = {"score": game["score"], "distance": game["distance"], "coins": game["coins"]}
            leaderboard = add_leaderboard_entry(leaderboard_path, username or "Player", result["score"], result["distance"])
            screen_state = "game_over"
    elif screen_state == "game_over":
        draw_game(screen, fonts, game)
        over = pygame.Surface((520, 760), pygame.SRCALPHA)
        over.fill((0, 0, 0, 170))
        screen.blit(over, (0, 0))
        mouse = pygame.mouse.get_pos()
        from ui import button, draw_text
        draw_text(screen, "Game Over", fonts["title"], (255, 255, 255), 260, 200, center=True)
        draw_text(screen, f"Score: {result['score']}", fonts["normal"], (255, 255, 255), 260, 270, center=True)
        draw_text(screen, f"Distance: {result['distance']}  Coins: {result['coins']}", fonts["small"], (230, 230, 230), 260, 310, center=True)
        button(screen, retry_rect, "Retry", fonts["normal"], mouse)
        button(screen, menu_rect, "Menu", fonts["normal"], mouse)

    pygame.display.flip()

pygame.quit()
