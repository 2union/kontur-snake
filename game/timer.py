import pygame


class GameTimer:
    def __init__(self, timer_count: int):
        self.clock = pygame.time.Clock()
        self.timer = timer_count
        self.is_finished = False

    def count(self, delta_time: float) -> float:
        if self.timer <= 0:
            self.is_finished = True
            return 0.0
        self.timer -= delta_time
        return self.timer
