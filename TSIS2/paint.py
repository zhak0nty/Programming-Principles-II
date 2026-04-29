from pathlib import Path

import pygame

from tools import (
    circle_radius,
    equilateral_triangle_points,
    flood_fill,
    in_canvas,
    make_color_buttons,
    make_size_buttons,
    make_tool_buttons,
    rectangle_rect,
    rhombus_points,
    right_triangle_points,
    save_canvas_png,
    square_rect,
    to_canvas,
)


pygame.init()
width, height = 1280, 760
toolbar_h = 136
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TSIS2 - Extended Paint")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 18)
small = pygame.font.SysFont("arial", 16)
text_font = pygame.font.SysFont("arial", 30)

canvas = pygame.Surface((width, height - toolbar_h))
canvas.fill((255, 255, 255))

tool_buttons = make_tool_buttons()
size_buttons = make_size_buttons()
color_buttons = make_color_buttons()

current_tool = "pencil"
current_color = (0, 0, 0)
brush_size = 5
dragging = False
start_pos = (0, 0)
last_pos = (0, 0)
status_message = "Ready"
status_timer = 0

text_mode_active = False
text_anchor = (0, 0)
text_buffer = ""

shape_tools = {
    "line",
    "rectangle",
    "circle",
    "square",
    "right_triangle",
    "equilateral_triangle",
    "rhombus",
}


def draw_shape(surface: pygame.Surface, tool: str, start: tuple[int, int], end: tuple[int, int]) -> None:
    if tool == "line":
        pygame.draw.line(surface, current_color, start, end, brush_size)
    elif tool == "rectangle":
        rect = rectangle_rect(start, end)
        if rect.width > 0 and rect.height > 0:
            pygame.draw.rect(surface, current_color, rect, brush_size)
    elif tool == "circle":
        radius = circle_radius(start, end)
        if radius > 0:
            pygame.draw.circle(surface, current_color, start, radius, brush_size)
    elif tool == "square":
        rect = square_rect(start, end)
        if rect.width > 0:
            pygame.draw.rect(surface, current_color, rect, brush_size)
    elif tool == "right_triangle":
        pygame.draw.polygon(surface, current_color, right_triangle_points(start, end), brush_size)
    elif tool == "equilateral_triangle":
        pygame.draw.polygon(surface, current_color, equilateral_triangle_points(start, end), brush_size)
    elif tool == "rhombus":
        pygame.draw.polygon(surface, current_color, rhombus_points(start, end), brush_size)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if text_mode_active:
                if event.key == pygame.K_RETURN:
                    if text_buffer:
                        rendered = text_font.render(text_buffer, True, current_color)
                        canvas.blit(rendered, text_anchor)
                    text_mode_active = False
                    text_buffer = ""
                elif event.key == pygame.K_ESCAPE:
                    text_mode_active = False
                    text_buffer = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                else:
                    if event.unicode and event.unicode.isprintable():
                        text_buffer += event.unicode
                continue

            if event.key == pygame.K_c:
                canvas.fill((255, 255, 255))
            elif event.key == pygame.K_1:
                brush_size = 2
            elif event.key == pygame.K_2:
                brush_size = 5
            elif event.key == pygame.K_3:
                brush_size = 10
            elif event.key == pygame.K_s and (event.mod & pygame.KMOD_CTRL):
                save_path = save_canvas_png(canvas, Path(__file__).resolve().parent)
                status_message = f"Saved: {save_path.name}"
                status_timer = pygame.time.get_ticks()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[1] < toolbar_h:
                for name, rect in tool_buttons:
                    if rect.collidepoint(event.pos):
                        current_tool = name
                        text_mode_active = False
                        text_buffer = ""
                        break
                for size, rect in size_buttons:
                    if rect.collidepoint(event.pos):
                        brush_size = size
                for color, rect in color_buttons:
                    if rect.collidepoint(event.pos):
                        current_color = color
                continue

            if in_canvas(event.pos, width, height, toolbar_h):
                dragging = True
                start_pos = event.pos
                last_pos = event.pos
                canvas_point = to_canvas(event.pos, toolbar_h)

                if current_tool == "fill":
                    flood_fill(canvas, canvas_point, current_color)
                    dragging = False
                elif current_tool == "text":
                    text_mode_active = True
                    text_anchor = canvas_point
                    text_buffer = ""
                    dragging = False

        elif event.type == pygame.MOUSEMOTION and dragging:
            if current_tool in ("pencil", "eraser"):
                p1 = to_canvas(last_pos, toolbar_h)
                p2 = to_canvas(event.pos, toolbar_h)
                color = current_color if current_tool == "pencil" else (255, 255, 255)
                pygame.draw.line(canvas, color, p1, p2, brush_size)
                last_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging:
            if in_canvas(event.pos, width, height, toolbar_h):
                if current_tool in shape_tools:
                    start = to_canvas(start_pos, toolbar_h)
                    end = to_canvas(event.pos, toolbar_h)
                    draw_shape(canvas, current_tool, start, end)
            dragging = False

    screen.fill((245, 245, 245))
    pygame.draw.rect(screen, (232, 232, 236), (0, 0, width, toolbar_h))
    pygame.draw.line(screen, (170, 170, 170), (0, toolbar_h), (width, toolbar_h), 2)

    for name, rect in tool_buttons:
        active = name == current_tool
        pygame.draw.rect(screen, (166, 214, 255) if active else (252, 252, 252), rect, border_radius=7)
        pygame.draw.rect(screen, (120, 120, 120), rect, 2, border_radius=7)
        label = small.render(name, True, (25, 25, 25))
        screen.blit(label, label.get_rect(center=rect.center))

    for size, rect in size_buttons:
        active = size == brush_size
        pygame.draw.rect(screen, (190, 240, 200) if active else (252, 252, 252), rect, border_radius=7)
        pygame.draw.rect(screen, (120, 120, 120), rect, 2, border_radius=7)
        label = font.render(str(size), True, (20, 20, 20))
        screen.blit(label, label.get_rect(center=rect.center))

    for color, rect in color_buttons:
        pygame.draw.rect(screen, color, rect, border_radius=5)
        pygame.draw.rect(screen, (40, 40, 40), rect, 3 if color == current_color else 1, border_radius=5)

    info = "Brush: 1/2/3 keys | Ctrl+S save | C clear | Text: Enter confirm, Esc cancel"
    screen.blit(small.render(info, True, (50, 50, 50)), (680, 100))
    if status_message and pygame.time.get_ticks() - status_timer < 2200:
        screen.blit(small.render(status_message, True, (20, 110, 20)), (680, 78))

    screen.blit(canvas, (0, toolbar_h))

    if dragging and current_tool in shape_tools and in_canvas(pygame.mouse.get_pos(), width, height, toolbar_h):
        preview = canvas.copy()
        s = to_canvas(start_pos, toolbar_h)
        e = to_canvas(pygame.mouse.get_pos(), toolbar_h)
        draw_shape(preview, current_tool, s, e)
        screen.blit(preview, (0, toolbar_h))

    if text_mode_active:
        preview = canvas.copy()
        rendered = text_font.render(text_buffer + "|", True, current_color)
        preview.blit(rendered, text_anchor)
        screen.blit(preview, (0, toolbar_h))

    pygame.display.flip()
    clock.tick(120)

pygame.quit()
