import pygame


class MovingBallGame:
    def __init__(self) -> None:
        pygame.init()
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Moving Ball")
        self.clock = pygame.time.Clock()

        self.radius = 25
        self.step = 20
        self.x = self.width // 2
        self.y = self.height // 2

    def _move(self, dx: int, dy: int) -> None:
        new_x = self.x + dx
        new_y = self.y + dy
        if self.radius <= new_x <= self.width - self.radius:
            self.x = new_x
        if self.radius <= new_y <= self.height - self.radius:
            self.y = new_y

    def _draw(self) -> None:
        self.screen.fill((255, 255, 255))
        pygame.draw.circle(self.screen, (225, 25, 25), (self.x, self.y), self.radius)
        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self._move(0, -self.step)
                    elif event.key == pygame.K_DOWN:
                        self._move(0, self.step)
                    elif event.key == pygame.K_LEFT:
                        self._move(-self.step, 0)
                    elif event.key == pygame.K_RIGHT:
                        self._move(self.step, 0)

            self._draw()
            self.clock.tick(60)

        pygame.quit()
