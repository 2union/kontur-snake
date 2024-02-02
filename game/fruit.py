import random

import pygame
from pygame.math import Vector2


class Fruit:
    def __init__(self, screen, cell_size, apple, cell_number):
        self.screen = screen
        self.cell_size = cell_size
        self.apple = apple
        self.cell_number = cell_number
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * self.cell_size),
                                 int(self.pos.y * self.cell_size),
                                 self.cell_size,
                                 self.cell_size)
        self.screen.blit(self.apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(1, self.cell_number - 2)
        self.y = random.randint(1, self.cell_number - 2)
        self.pos = Vector2(self.x, self.y)
