from collections import deque

import pygame

from snake_game import SnakeConfig, build_walls, draw_grid, level_info, spawn_food


pygame.init()
config = SnakeConfig()
width = config.cols * config.cell_size
height = config.rows * config.cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Practice 10 - Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 26)
small_font = pygame.font.SysFont("arial", 20)

walls = build_walls(config)
cx, cy = config.cols // 2, config.rows // 2
snake = deque([(cx, cy), (cx - 1, cy), (cx - 2, cy)])
direction = (1, 0)
next_direction = (1, 0)
score = 0
alive = True
food = spawn_food(config, snake, walls)
running = True


while running:
    info = level_info(score)
    clock.tick(info.speed_fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if alive:
                mapping = {
                    pygame.K_UP: (0, -1),
                    pygame.K_DOWN: (0, 1),
                    pygame.K_LEFT: (-1, 0),
                    pygame.K_RIGHT: (1, 0),
                }
                if event.key in mapping:
                    new_dir = mapping[event.key]
                    if not (new_dir[0] == -direction[0] and new_dir[1] == -direction[1]):
                        next_direction = new_dir
            else:
                if event.key == pygame.K_r:
                    snake = deque([(cx, cy), (cx - 1, cy), (cx - 2, cy)])
                    direction = (1, 0)
                    next_direction = (1, 0)
                    score = 0
                    alive = True
                    food = spawn_food(config, snake, walls)
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False

    if alive:
        direction = next_direction
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        x, y = new_head
        # Border, wall and self-collision checks in main loop.
        if x < 0 or y < 0 or x >= config.cols or y >= config.rows:
            alive = False
        elif new_head in walls or new_head in snake:
            alive = False
        else:
            snake.appendleft(new_head)
            if new_head == food:
                score += 1
                food = spawn_food(config, snake, walls)
            else:
                snake.pop()

    draw_grid(screen, config)

    for x, y in walls:
        rect = pygame.Rect(x * config.cell_size, y * config.cell_size, config.cell_size, config.cell_size)
        pygame.draw.rect(screen, (95, 95, 105), rect)

    fx, fy = food
    food_rect = pygame.Rect(
        fx * config.cell_size + 4,
        fy * config.cell_size + 4,
        config.cell_size - 8,
        config.cell_size - 8,
    )
    pygame.draw.rect(screen, (230, 80, 70), food_rect, border_radius=6)

    for idx, (sx, sy) in enumerate(snake):
        rect = pygame.Rect(sx * config.cell_size, sy * config.cell_size, config.cell_size, config.cell_size)
        if idx == 0:
            pygame.draw.rect(screen, (58, 210, 82), rect, border_radius=6)
        else:
            pygame.draw.rect(screen, (42, 165, 68), rect, border_radius=4)

    info = level_info(score)
    hud = font.render(f"Score: {score}   Level: {info.level}", True, (235, 235, 235))
    screen.blit(hud, (12, 10))

    hint = small_font.render(
        f"Food to next level: {info.foods_to_next_level}   Speed: {info.speed_fps}",
        True,
        (205, 205, 210),
    )
    screen.blit(hint, (12, 40))

    if not alive:
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        over = font.render("Game Over", True, (255, 255, 255))
        score_text = small_font.render(f"Final score: {score}", True, (255, 255, 255))
        prompt = small_font.render("Press R to restart, Q to quit", True, (255, 255, 255))
        screen.blit(over, over.get_rect(center=(width // 2, height // 2 - 30)))
        screen.blit(score_text, score_text.get_rect(center=(width // 2, height // 2 + 2)))
        screen.blit(prompt, prompt.get_rect(center=(width // 2, height // 2 + 34)))

    pygame.display.flip()

pygame.quit()
