import pygame


def draw_text(screen: pygame.Surface, text: str, font, color, x: int, y: int, center: bool = False):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y)) if center else surf.get_rect(topleft=(x, y))
    screen.blit(surf, rect)
    return rect


def button(screen: pygame.Surface, rect: pygame.Rect, text: str, font, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    bg = (170, 210, 255) if hovered else (240, 240, 245)
    pygame.draw.rect(screen, bg, rect, border_radius=8)
    pygame.draw.rect(screen, (80, 80, 90), rect, 2, border_radius=8)
    draw_text(screen, text, font, (20, 20, 20), rect.centerx, rect.centery, center=True)


def draw_menu(screen, fonts, username, buttons):
    screen.fill((22, 30, 48))
    draw_text(screen, "TSIS3 Racer", fonts["title"], (255, 255, 255), 240, 90)
    draw_text(screen, f"Player: {username}", fonts["small"], (210, 220, 235), 240, 140)
    mouse_pos = pygame.mouse.get_pos()
    for text, rect in buttons:
        button(screen, rect, text, fonts["normal"], mouse_pos)


def draw_settings(screen, fonts, settings, options, back_rect):
    screen.fill((26, 32, 40))
    draw_text(screen, "Settings", fonts["title"], (255, 255, 255), 240, 60)
    draw_text(screen, f"Sound: {'ON' if settings['sound'] else 'OFF'}", fonts["normal"], (220, 220, 230), 120, 160)
    draw_text(screen, f"Car color: {settings['car_color']}", fonts["normal"], (220, 220, 230), 120, 240)
    draw_text(screen, f"Difficulty: {settings['difficulty']}", fonts["normal"], (220, 220, 230), 120, 320)
    draw_text(screen, "Click option buttons to cycle values", fonts["small"], (180, 190, 205), 120, 380)
    mouse_pos = pygame.mouse.get_pos()
    for text, rect in options:
        button(screen, rect, text, fonts["normal"], mouse_pos)
    button(screen, back_rect, "Back", fonts["normal"], mouse_pos)


def draw_leaderboard(screen, fonts, rows, back_rect):
    screen.fill((22, 28, 35))
    draw_text(screen, "Top 10 Leaderboard", fonts["title"], (255, 255, 255), 240, 60)
    y = 120
    if not rows:
        draw_text(screen, "No scores yet", fonts["normal"], (200, 200, 210), 160, y)
    else:
        for i, row in enumerate(rows, start=1):
            line = f"{i:>2}. {row['name']:<18} score={row['score']:<5} distance={row['distance']}"
            draw_text(screen, line, fonts["small"], (210, 220, 235), 120, y)
            y += 34
    button(screen, back_rect, "Back", fonts["normal"], pygame.mouse.get_pos())


def draw_name_input(screen, fonts, name):
    screen.fill((18, 22, 32))
    draw_text(screen, "Enter username", fonts["title"], (255, 255, 255), 240, 120)
    draw_text(screen, "Press Enter to continue", fonts["small"], (170, 180, 200), 240, 170)
    pygame.draw.rect(screen, (245, 245, 250), (120, 240, 350, 52), border_radius=8)
    pygame.draw.rect(screen, (90, 90, 110), (120, 240, 350, 52), 2, border_radius=8)
    draw_text(screen, name + "|", fonts["normal"], (20, 20, 30), 136, 255)
