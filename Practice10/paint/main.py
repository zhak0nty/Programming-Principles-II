import pygame

from paint_app import canvas_pos, color_buttons, in_canvas, tool_buttons


pygame.init()
width, height = 1000, 680
toolbar_h = 96
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Practice 10 - Paint")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 22)
small_font = pygame.font.SysFont("arial", 18)

canvas = pygame.Surface((width, height - toolbar_h))
canvas.fill((255, 255, 255))

current_tool = "brush"
current_color = (0, 0, 0)
brush_size = 6
eraser_size = 20
dragging = False
start_pos = (0, 0)
last_pos = (0, 0)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                canvas.fill((255, 255, 255))
            elif event.key == pygame.K_LEFTBRACKET:
                brush_size = max(1, brush_size - 1)
                eraser_size = max(8, eraser_size - 2)
            elif event.key == pygame.K_RIGHTBRACKET:
                brush_size = min(32, brush_size + 1)
                eraser_size = min(72, eraser_size + 2)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[1] < toolbar_h:
                clicked_toolbar = False
                for tool, rect in tool_buttons():
                    if rect.collidepoint(event.pos):
                        current_tool = tool
                        clicked_toolbar = True
                        break
                if not clicked_toolbar:
                    for color, rect in color_buttons():
                        if rect.collidepoint(event.pos):
                            current_color = color
                            break
                continue

            if in_canvas(event.pos, width, height, toolbar_h):
                dragging = True
                start_pos = event.pos
                last_pos = event.pos

        elif event.type == pygame.MOUSEMOTION and dragging:
            if current_tool in ("brush", "eraser"):
                start = canvas_pos(last_pos, toolbar_h)
                end = canvas_pos(event.pos, toolbar_h)
                if current_tool == "brush":
                    pygame.draw.line(canvas, current_color, start, end, brush_size)
                else:
                    pygame.draw.line(canvas, (255, 255, 255), start, end, eraser_size)
                last_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging:
            if in_canvas(event.pos, width, height, toolbar_h):
                start = canvas_pos(start_pos, toolbar_h)
                end = canvas_pos(event.pos, toolbar_h)
                if current_tool == "rectangle":
                    rect = pygame.Rect(
                        min(start[0], end[0]),
                        min(start[1], end[1]),
                        abs(end[0] - start[0]),
                        abs(end[1] - start[1]),
                    )
                    if rect.width > 0 and rect.height > 0:
                        pygame.draw.rect(canvas, current_color, rect, 3)
                elif current_tool == "circle":
                    radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
                    if radius > 0:
                        pygame.draw.circle(canvas, current_color, start, radius, 3)
            dragging = False

    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (232, 232, 235), (0, 0, width, toolbar_h))
    pygame.draw.line(screen, (180, 180, 180), (0, toolbar_h), (width, toolbar_h), 2)

    for tool, rect in tool_buttons():
        active = tool == current_tool
        pygame.draw.rect(screen, (155, 210, 255) if active else (250, 250, 250), rect, border_radius=8)
        pygame.draw.rect(screen, (120, 120, 120), rect, 2, border_radius=8)
        label = font.render(tool.capitalize(), True, (30, 30, 30))
        screen.blit(label, label.get_rect(center=rect.center))

    for color, rect in color_buttons():
        pygame.draw.rect(screen, color, rect, border_radius=5)
        border = 3 if color == current_color else 1
        pygame.draw.rect(screen, (30, 30, 30), rect, border, border_radius=5)

    tip = small_font.render(
        "LMB draw. C=clear, [ / ] size. Tools: rectangle, circle, eraser, color selection.",
        True,
        (45, 45, 45),
    )
    screen.blit(tip, (360, 64))

    screen.blit(canvas, (0, toolbar_h))

    if dragging and current_tool in ("rectangle", "circle") and in_canvas(pygame.mouse.get_pos(), width, height, toolbar_h):
        preview = canvas.copy()
        start = canvas_pos(start_pos, toolbar_h)
        end = canvas_pos(pygame.mouse.get_pos(), toolbar_h)
        if current_tool == "rectangle":
            rect = pygame.Rect(
                min(start[0], end[0]),
                min(start[1], end[1]),
                abs(end[0] - start[0]),
                abs(end[1] - start[1]),
            )
            pygame.draw.rect(preview, current_color, rect, 3)
        else:
            radius = int(((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2) ** 0.5)
            pygame.draw.circle(preview, current_color, start, radius, 3)
        screen.blit(preview, (0, toolbar_h))

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
