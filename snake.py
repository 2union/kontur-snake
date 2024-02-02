import sys
from itertools import chain

import pygame
from pygame.math import Vector2

from game.client import Client
from game.fruit import Fruit
from game.keys_emulate import *
from game.resources import Resources
from game.snake import Snake
from game.teams import Teams
from game.timer import GameTimer
from settings import *


class MAIN:
    def __init__(self):
        self.snake = Snake(5, screen, cell_number, cell_size)
        self.second_snake = Snake(20, screen, cell_number, cell_size, 'BlueSnake')
        self.resources = Resources()
        self.fruit = Fruit(screen, cell_size, self.resources.apple, cell_number)
        self.net = Client(SOCKET_POINT, PACKAGE_SIZE)
        self.name_team_one = ''
        self.players_team_one = []
        self.name_team_two = ''
        self.players_team_two = []
        self.team_stack = []
        self.team_stack_is_available = False
        self.is_initialized = False
        self.timer = GameTimer(SESSION_LENGTH)
        self.goals = [0, 0]
        self.last_goals = [0, 0]
        self.resources.t1.play(-1)
        self.teams = Teams()
        self.leaders = []

    def team_initialize(self):
        resp = self.net.send('1:')
        if resp == '1:':
            return

        if self.team_stack_is_available and len(resp) > 1:
            self.team_stack.append(resp)

        if len(resp) == 1:
            if int(resp) == 1:
                self.team_stack_is_available = True
            if int(resp) > 1:
                self.team_stack_is_available = False

            if int(resp) == 1 and len(self.team_stack):
                if len(self.players_team_one):
                    self.name_team_two = self.teams.append_team(set(self.team_stack))
                    self.players_team_two = self.team_stack.copy()
                else:
                    self.name_team_one = self.teams.append_team(set(self.team_stack))
                    self.players_team_one = self.team_stack.copy()
                self.team_stack = []

                if len(self.players_team_one) and len(self.players_team_two):
                    self.is_initialized = True
                    self.team_stack_is_available = False
                    self.net.send(f'1:T1:{self.name_team_one}')
                    self.net.send(f'1:T2:{self.name_team_two}')
                    self.resources.t1.stop()
                    self.resources.t2.play(-1)

    def stop_the_game(self):
        resp = self.net.send(f'1:finish:{self.goals[0]}:{self.goals[1]}')
        self.teams.save_score((self.name_team_one, self.name_team_two), tuple(self.goals))
        self.name_team_one = ''
        self.players_team_one = []
        self.name_team_two = ''
        self.players_team_two = []
        self.leaders = self.teams.get_top_teams()
        self.is_initialized = False
        self.resources.t1.stop()
        self.resources.t2.stop()
        self.resources.t3.stop()
        self.resources.t4.stop()
        self.last_goals = self.goals
        self.goals = [0, 0]
        self.timer = GameTimer(SESSION_LENGTH)
        self.game_over()
        self.resources.t1.play(-1)

    def get_network_keys(self):
        resp = self.net.send('1:')
        if resp == '1:':
            return

        if len(resp) == 1:
            if int(resp) == 2:
                key_right()
            if int(resp) == 3:
                key_left()
            if int(resp) == 4:
                key_up()
            if int(resp) == 5:
                key_down()
            if int(resp) == 6:
                key_d()
            if int(resp) == 7:
                key_a()
            if int(resp) == 8:
                key_w()
            if int(resp) == 9:
                key_s()

            if int(resp) == 0:
                self.stop_the_game()

    def update(self):
        if not self.is_initialized:
            self.team_initialize()
        else:
            self.get_network_keys()
        self.snake.move_snake()
        self.second_snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.check_timer()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.second_snake.draw_snake()
        self.draw_scoreboard()
        self.draw_score()
        self.draw_score_second()
        self.draw_timer()
        self.draw_goals()

    def draw_team(self, cells_padding, window_width, score, name):
        team_surface = self.resources.player_font.render(f'[{score}] {name}', True, (255, 255, 255))
        team_rect = team_surface.get_rect(center=(window_width // 2, cell_size * (cells_padding + 0.5)))
        screen.blit(team_surface, team_rect)

    def draw_waiting_screen(self):
        window_width = cell_size * (info_cells + cell_number)
        window_height = cell_size * cell_number
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(0, 0, window_width, window_height))
        rect = pygame.Rect(window_width // 4, window_height // 4, cell_size, cell_size)
        screen.blit(self.resources.wait, rect)

        score_surface = self.resources.score_font.render(f'{self.last_goals[0]}:{self.last_goals[1]}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(window_width // 2, window_height // 1.1))
        screen.blit(score_surface, score_rect)

        i = 1
        for score, name in self.leaders:
            self.draw_team(i, window_width, score, name)
            i += 2

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.append_goal(0)

        if self.fruit.pos == self.second_snake.body[0]:
            self.fruit.randomize()
            self.second_snake.add_block()
            self.second_snake.play_crunch_sound()
            self.append_goal(1)

        for block in chain(self.snake.body[1:], self.second_snake.body[1:]):
            if block == self.fruit.pos:
                self.fruit.randomize()

    def append_goal(self, pos):
        if pos:
            snake = self.second_snake
        else:
            snake = self.snake
        snake_len = len(snake.body) - 3

        res = snake_len//5
        goal = 1 + res
        self.goals[pos] += goal

    def check_fail(self):
        if self.snake.bite_myself():
            self.snake.reset()

        if self.snake.bite_me(self.second_snake.body[0]):
            if self.second_snake.body[0] == self.snake.body[0]:
                self.snake.reset()
            self.second_snake.reset()

        if self.second_snake.bite_myself():
            self.second_snake.reset()

        if self.second_snake.bite_me(self.snake.body[0]):
            if self.second_snake.body[0] == self.snake.body[0]:
                self.second_snake.reset()
            self.snake.reset()

    def check_timer(self):
        if self.timer.is_finished:
            self.stop_the_game()

    def game_over(self):
        self.snake.reset()
        self.second_snake.reset()

    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_player(self, cells_padding, direction, name):
        resource = self.resources.__getattribute__(f'i_{direction}')
        resized = pygame.transform.scale(resource, (cell_size, cell_size))

        rect = pygame.Rect(cell_size * (cell_number + 2), cell_size * cells_padding, cell_size, cell_size)
        screen.blit(resized, rect)

        player_surface = self.resources.player_font.render(name, True, (255, 255, 255))
        player_rect = player_surface.get_rect(center=(cell_size * (cell_number + 6), cell_size * (cells_padding + 0.5)))
        screen.blit(player_surface, player_rect)

    def draw_scoreboard(self):
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(cell_size * cell_number, 0, cell_size * info_cells, cell_size * cell_number))
        kontur_logo_rect = pygame.Rect(cell_size * cell_number + cell_size / 2,
                                       cell_size / 2, cell_size * info_cells, cell_size * 3)
        # kontur_logo_resized = pygame.transform.scale(self.resources.kontur_logo, (cell_size * (info_cells - 1), 97))
        kontur_logo_resized = self.resources.kontur_logo
        screen.blit(kontur_logo_resized, kontur_logo_rect)

        snake_surface = self.resources.snake_font.render("Змейка", True, (255, 255, 255))
        snake_rect = snake_surface.get_rect(center=(cell_size * (cell_number + 7.3), cell_size * 3.3))
        screen.blit(snake_surface, snake_rect)

        directions = ['up', 'down', 'right', 'left']
        # first team
        pygame.draw.rect(screen, (255, 211, 66),
                         pygame.Rect(cell_size * (cell_number + 1), cell_size * 4, cell_size * (info_cells - 2),
                                     cell_size * (cell_number - 6) / 2))
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(cell_size * (cell_number + 1) + 4, cell_size * 4 + 4,
                                     cell_size * (info_cells - 2) - 8,
                                     cell_size * (cell_number - 6) / 2 - 8))

        team_surface = self.resources.team_font.render(self.name_team_one, True, (255, 211, 66))
        team_rect = team_surface.get_rect(center=(cell_size * (cell_number + 5.2), cell_size * 5))
        screen.blit(team_surface, team_rect)

        position = 6
        for i, player in enumerate(self.players_team_one):
            self.draw_player(position, directions[i], player)
            position += 2

        # second team
        pygame.draw.rect(screen, (91, 123, 249),
                         pygame.Rect(cell_size * (cell_number + 1), cell_size * (cell_number / 2 + 2),
                                     cell_size * (info_cells - 2),
                                     cell_size * (cell_number - 6) / 2))
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(cell_size * (cell_number + 1) + 4, cell_size * (cell_number / 2 + 2) + 4,
                                     cell_size * (info_cells - 2) - 8,
                                     cell_size * (cell_number - 6) / 2 - 8))

        team_two_surface = self.resources.team_font.render(self.name_team_two, True, (91, 123, 249))
        team_two_rect = team_two_surface.get_rect(center=(cell_size * (cell_number + 5.2), cell_size * 16))
        screen.blit(team_two_surface, team_two_rect)

        position = 17
        for i, player in enumerate(self.players_team_two):
            self.draw_player(position, directions[i], player)
            position += 2

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = self.resources.game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number + cell_size * info_cells - cell_size * 2)
        score_y = int(cell_size * (cell_number / 2 + 1))
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.resources.apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(self.resources.apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def draw_score_second(self):
        score_text = str(len(self.second_snake.body) - 3)
        score_surface = self.resources.game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number + cell_size * info_cells - cell_size * 2)
        score_y = int(cell_size * cell_number - cell_size)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = self.resources.apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(self.resources.apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def draw_timer(self):
        score_text = f'{int(self.timer.timer//60)}:{int(self.timer.timer%60)}'
        score_surface = self.resources.game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - cell_size * 2)
        score_y = int(cell_size * cell_number - cell_size)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

    def draw_goals(self):
        score_text = f'{int(self.goals[0])}:{int(self.goals[1])}'
        score_surface = self.resources.game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - cell_size * 2)
        score_y = int(cell_size * cell_number - cell_size * 2)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 26
info_cells = 10
screen = pygame.display.set_mode((cell_number * cell_size + info_cells * cell_size, cell_number * cell_size))
# screen = pygame.display.set_mode((cell_number * cell_size + info_cells * cell_size, cell_number * cell_size), pygame.FULLSCREEN)
pygame.display.set_caption('Контур.Змейка')
icon = pygame.image.load('Graphics/snake.ico')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_w:
                if main_game.second_snake.direction.y != 1:
                    main_game.second_snake.direction = Vector2(0, -1)
            if event.key == pygame.K_d:
                if main_game.second_snake.direction.x != -1:
                    main_game.second_snake.direction = Vector2(1, 0)
            if event.key == pygame.K_s:
                if main_game.second_snake.direction.y != -1:
                    main_game.second_snake.direction = Vector2(0, 1)
            if event.key == pygame.K_a:
                if main_game.second_snake.direction.x != 1:
                    main_game.second_snake.direction = Vector2(-1, 0)

    screen.fill((175, 215, 70))
    if main_game.is_initialized:
        main_game.timer.count(clock.tick(20) / 800)
        main_game.draw_elements()
    else:
        main_game.draw_waiting_screen()
    pygame.display.update()
    clock.tick(60)
