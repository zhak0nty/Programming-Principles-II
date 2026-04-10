import os
from dataclasses import dataclass

import pygame


@dataclass
class TrackState:
    index: int = 0
    is_playing: bool = False
    started_at_ms: int = 0


class MusicPlayer:
    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()

        self.width, self.height = 840, 380
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Music Player")
        self.clock = pygame.time.Clock()

        self.big_font = pygame.font.SysFont("arial", 34, bold=True)
        self.font = pygame.font.SysFont("consolas", 26)
        self.small_font = pygame.font.SysFont("arial", 22)

        self.tracks = self._discover_tracks()
        self.state = TrackState()
        self.status_text = "Ready"

    def _discover_tracks(self) -> list[str]:
        music_dir = os.path.join(os.path.dirname(__file__), "music")
        supported = (".mp3", ".wav", ".ogg")
        tracks = []
        for root, _, files in os.walk(music_dir):
            for name in sorted(files):
                if name.lower().endswith(supported):
                    tracks.append(os.path.join(root, name))
        return tracks

    def _play(self, index: int | None = None) -> None:
        if not self.tracks:
            self.status_text = "No tracks found in music/"
            return

        if index is not None:
            self.state.index = index % len(self.tracks)

        track_path = self.tracks[self.state.index]
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        self.state.is_playing = True
        self.state.started_at_ms = pygame.time.get_ticks()
        self.status_text = "Playing"

    def _stop(self) -> None:
        pygame.mixer.music.stop()
        self.state.is_playing = False
        self.status_text = "Stopped"

    def _next(self) -> None:
        if not self.tracks:
            self.status_text = "No tracks found in music/"
            return
        self._play(self.state.index + 1)

    def _prev(self) -> None:
        if not self.tracks:
            self.status_text = "No tracks found in music/"
            return
        self._play(self.state.index - 1)

    def _position_seconds(self) -> int:
        if not self.state.is_playing:
            return 0
        elapsed_ms = pygame.time.get_ticks() - self.state.started_at_ms
        return max(0, elapsed_ms // 1000)

    def _draw(self) -> None:
        self.screen.fill((32, 36, 42))

        title = self.big_font.render("Keyboard Music Player", True, (230, 230, 230))
        self.screen.blit(title, (24, 20))

        if self.tracks:
            current = os.path.basename(self.tracks[self.state.index])
        else:
            current = "No track loaded"

        lines = [
            f"Track:   {current}",
            f"Status:  {self.status_text}",
            f"Pos:     {self._position_seconds()} s",
        ]
        y = 100
        for line in lines:
            text = self.font.render(line, True, (214, 214, 214))
            self.screen.blit(text, (24, y))
            y += 42

        keys = "P=Play  S=Stop  N=Next  B=Back  Q=Quit"
        controls = self.small_font.render(keys, True, (180, 220, 255))
        self.screen.blit(controls, (24, self.height - 56))

        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_p:
                        self._play()
                    elif event.key == pygame.K_s:
                        self._stop()
                    elif event.key == pygame.K_n:
                        self._next()
                    elif event.key == pygame.K_b:
                        self._prev()

            self._draw()
            self.clock.tick(30)

        pygame.mixer.music.stop()
        pygame.quit()
