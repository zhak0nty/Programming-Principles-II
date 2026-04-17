import pygame

from racer_game import (
    RacerConfig,
    car_rect,
    draw_car,
    draw_road,
    lane_center,
    spawn_coin,
    spawn_enemy,
)


pygame.init()
config = RacerConfig()
screen = pygame.display.set_mode((config.width, config.height))
pygame.display.set_caption("Practice 10 - Racer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28, bold=True)
info_font = pygame.font.SysFont("arial", 24)

player_lane = 1
player_y = config.height - config.player_h - 30
enemy = spawn_enemy(config, speed=7.0)
coin = None
coin_speed = 7.0
coin_spawn_timer_ms = 0
coin_spawn_delay_ms = 900
score = 0
distance = 0
bg_offset = 0
running = True
alive = True


while running:
    dt_ms = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif alive and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_lane = max(0, player_lane - 1)
            elif event.key == pygame.K_RIGHT:
                player_lane = min(config.lane_count - 1, player_lane + 1)
        elif not alive and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                player_lane = 1
                enemy = spawn_enemy(config, speed=7.0)
                coin = None
                coin_spawn_timer_ms = 0
                score = 0
                distance = 0
                bg_offset = 0
                alive = True
            elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                running = False

    if alive:
        distance += 1
        enemy.y += enemy.speed
        if enemy.y > config.height:
            enemy = spawn_enemy(config, speed=enemy.speed + 0.05)

        coin_spawn_timer_ms += dt_ms
        if coin is None and coin_spawn_timer_ms >= coin_spawn_delay_ms:
            coin_spawn_timer_ms = 0
            coin = spawn_coin(config, coin_speed)

        if coin is not None:
            coin.y += coin.speed
            if coin.y > config.height:
                coin = None

        player_rect = car_rect(lane_center(config, player_lane), player_y, config.player_w, config.player_h)
        enemy_rect = car_rect(enemy.x, enemy.y, config.enemy_w, config.enemy_h)

        if player_rect.colliderect(enemy_rect):
            alive = False

        if coin is not None:
            coin_rect = pygame.Rect(
                int(coin.x - config.coin_size // 2),
                int(coin.y),
                config.coin_size,
                config.coin_size,
            )
            # Coin collection is handled in main game loop.
            if player_rect.colliderect(coin_rect):
                score += 1
                coin = None

        bg_offset = (bg_offset + 12) % 80

    draw_road(screen, config, bg_offset)

    player_rect = car_rect(lane_center(config, player_lane), player_y, config.player_w, config.player_h)
    enemy_rect = car_rect(enemy.x, enemy.y, config.enemy_w, config.enemy_h)
    draw_car(screen, enemy_rect, (230, 60, 60))
    draw_car(screen, player_rect, (60, 130, 240))

    if coin is not None:
        coin_rect = pygame.Rect(
            int(coin.x - config.coin_size // 2),
            int(coin.y),
            config.coin_size,
            config.coin_size,
        )
        pygame.draw.circle(screen, (235, 185, 30), coin_rect.center, config.coin_size // 2)
        pygame.draw.circle(screen, (255, 238, 120), coin_rect.center, config.coin_size // 4)

    coin_text = font.render(f"Coins: {score}", True, (255, 255, 255))
    screen.blit(coin_text, coin_text.get_rect(topright=(config.width - 16, 12)))

    dist_text = info_font.render(f"Distance: {distance}", True, (240, 240, 240))
    screen.blit(dist_text, (16, 18))

    if not alive:
        overlay = pygame.Surface((config.width, config.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        line1 = font.render("Game Over", True, (255, 255, 255))
        line2 = info_font.render(f"Coins collected: {score}", True, (255, 255, 255))
        line3 = info_font.render("Press R to restart or Q to quit", True, (255, 255, 255))
        screen.blit(line1, line1.get_rect(center=(config.width // 2, config.height // 2 - 40)))
        screen.blit(line2, line2.get_rect(center=(config.width // 2, config.height // 2 + 2)))
        screen.blit(line3, line3.get_rect(center=(config.width // 2, config.height // 2 + 42)))

    pygame.display.flip()

pygame.quit()
