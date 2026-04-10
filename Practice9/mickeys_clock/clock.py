import math
import os
from datetime import datetime

import pygame


class MickeyClock:
    def __init__(self) -> None:
        pygame.init()
        self.width, self.height = 700, 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mickey's Clock")
        self.clock = pygame.time.Clock()
        self.center = (self.width // 2, self.height // 2)

        self.bg_color = (245, 245, 245)
        self.face_color = (255, 245, 210)
        self.mark_color = (30, 30, 30)

        image_path = os.path.join(os.path.dirname(__file__), "images", "mickey_hand.png")
        self.hand_image = self._load_hand_image(image_path)
        self.font = pygame.font.SysFont("arial", 30, bold=True)

    def _load_hand_image(self, image_path: str) -> pygame.Surface:
        if os.path.exists(image_path):
            image = pygame.image.load(image_path).convert_alpha()
            return pygame.transform.smoothscale(image, (380, 380))

        fallback = pygame.Surface((20, 180), pygame.SRCALPHA)
        pygame.draw.rect(fallback, (20, 20, 20), (7, 30, 6, 130), border_radius=3)
        pygame.draw.circle(fallback, (255, 255, 255), (10, 30), 15)
        pygame.draw.circle(fallback, (20, 20, 20), (10, 30), 15, width=2)
        return fallback

    def _draw_face(self) -> None:
        self.screen.fill(self.bg_color)
        pygame.draw.circle(self.screen, self.face_color, self.center, 280)
        pygame.draw.circle(self.screen, (170, 170, 170), self.center, 283, width=6)

        for i in range(60):
            angle = math.radians(i * 6 - 90)
            outer_r = 267
            inner_r = 240 if i % 5 == 0 else 250
            x1 = self.center[0] + int(math.cos(angle) * inner_r)
            y1 = self.center[1] + int(math.sin(angle) * inner_r)
            x2 = self.center[0] + int(math.cos(angle) * outer_r)
            y2 = self.center[1] + int(math.sin(angle) * outer_r)
            width = 4 if i % 5 == 0 else 2
            pygame.draw.line(self.screen, self.mark_color, (x1, y1), (x2, y2), width)

    def _draw_numbers(self) -> None:
        for hour in range(1, 13):
            angle = math.radians(hour * 30 - 90)
            x = self.center[0] + int(math.cos(angle) * 210)
            y = self.center[1] + int(math.sin(angle) * 210)
            text = self.font.render(str(hour), True, (25, 25, 25))
            rect = text.get_rect(center=(x, y))
            self.screen.blit(text, rect)

    def _draw_hand(self, angle: float, scale: tuple[int, int], is_minute: bool) -> None:
        hand = pygame.transform.smoothscale(self.hand_image, scale)
        rotated = pygame.transform.rotate(hand, -angle)
        rect = rotated.get_rect(center=self.center)
        self.screen.blit(rotated, rect)

        # Add a simple color cue: right/minute hand is darker, left/second lighter.
        radius = 6 if is_minute else 4
        color = (20, 20, 20) if is_minute else (150, 10, 10)
        tip_distance = 175 if is_minute else 200
        rad = math.radians(angle - 90)
        tip = (
            self.center[0] + int(math.cos(rad) * tip_distance),
            self.center[1] + int(math.sin(rad) * tip_distance),
        )
        pygame.draw.circle(self.screen, color, tip, radius)

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            now = datetime.now()
            minute_angle = now.minute * 6 + now.second * 0.1
            second_angle = now.second * 6

            self._draw_face()
            self._draw_numbers()

            # Right hand -> minute hand
            self._draw_hand(minute_angle, (240, 240), is_minute=True)
            # Left hand -> second hand
            self._draw_hand(second_angle, (200, 200), is_minute=False)

            pygame.draw.circle(self.screen, (30, 30, 30), self.center, 12)
            pygame.display.flip()
            self.clock.tick(1)

        pygame.quit()
