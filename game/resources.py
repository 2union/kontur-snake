import pygame


class Resources:
    def __init__(self):
        self.apple = pygame.image.load('./Graphics/apple.png').convert_alpha()
        self.kontur_logo = pygame.image.load('./Graphics/logo-kontur.png').convert_alpha()
        self.i_up = pygame.image.load('./Graphics/up.png')
        self.i_down = pygame.image.load('./Graphics/down.png')
        self.i_left = pygame.image.load('./Graphics/left.png')
        self.i_right = pygame.image.load('./Graphics/right.png')
        self.wait = pygame.image.load('./Graphics/wait.png')
        self.game_font = pygame.font.Font('./Font/PoetsenOne-Regular.ttf', 25)
        self.score_font = pygame.font.Font('./Font/PoetsenOne-Regular.ttf', 48)
        self.player_font = pygame.font.Font('./Font/JB/JetBrainsMono-VariableFont_wght.ttf', 25)
        self.team_font = pygame.font.Font('./Font/JB/JetBrainsMono-VariableFont_wght.ttf', 20)
        self.snake_font = pygame.font.Font('./Font/C/Caveat-VariableFont_wght.ttf', 32)
        self.t1 = pygame.mixer.Sound('Sound/theme1.wav')
        self.t2 = pygame.mixer.Sound('Sound/theme2.wav')
        self.t3 = pygame.mixer.Sound('Sound/theme3.wav')
        self.t4 = pygame.mixer.Sound('Sound/theme4.wav')
