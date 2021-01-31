import pygame
from pygame import *
import random

# settings
difficulty = 15
snake_starting_length = 4
random_starting_position = False
game_zoom = 30

pygame.init()

WIDTH, HEIGHT = 900, 900
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
lime = (0, 255, 0)
yellow = (255, 255, 0)
gray = (128, 128, 128)
darker_gray = (128, 128, 128)
light_gray = (160, 160, 160)
light_gray_2 = (192, 192, 192)
blue = (0, 0, 255)
light_blue = (153, 255, 255)
light_blue_2 = (204, 255, 255)
orange = (255, 178, 102)

# color settings
c_background = black
c_snake = orange
c_treasure = red


class Area:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def paint(self, color):
        pygame.draw.rect(screen, color, pygame.Rect(
            self.x, self.y, self.width, self.height))


class Snake():
    def __init__(self):
        self.x = (len(board[0]) - 1) // 2
        self.y = ((len(board)) - 1) // 2
        if random_starting_position:
            self.x = random.randint(0, len(board[0])) - 1
            self.y = random.randint(0, len(board)) - 1
        self.snake_ = list()
        for i in range(snake_starting_length):
            self.snake_.append([self.x - i, self.y])
        self.direction = "right"

    def paint(self, color):
        board[self.y][self.x].paint(color)

    def change_direction(self, direction):
        if self.direction == "right" or self.direction == "left":
            if direction != "right" and direction != "left":
                self.direction = direction
        elif self.direction == "up" or self.direction == "down":
            if direction != "up" and direction != "down":
                self.direction = direction

    def update_movement(self):
        old_x, old_y = self.snake_[0]
        if self.direction == "right":
            self.snake_[0][0] += 1
            if self.snake_[0][0] > len(board[0]) - 1:
                self.snake_[0][0] = 0
        elif self.direction == "left":
            self.snake_[0][0] -= 1
            if self.snake_[0][0] < 0:
                self.snake_[0][0] = len(board[0]) - 1
        elif self.direction == "up":
            self.snake_[0][1] -= 1
            if self.snake_[0][1] < 0:
                self.snake_[0][1] = len(board) - 1
        elif self.direction == "down":
            self.snake_[0][1] += 1
            if self.snake_[0][1] > len(board) - 1:
                self.snake_[0][1] = 0

        for i in range(len(self.snake_) - 1, 0, -1):
            if i == 1:
                self.snake_[i] = [old_x, old_y]
            else:
                self.snake_[i] = self.snake_[i - 1]

    def update(self):
        for snake_part in self.snake_:
            board[snake_part[1]][snake_part[0]].paint(c_snake)

    def is_dead(self):
        snake_copy = self.snake_.copy()
        head_cor = snake_copy[0]
        snake_copy.pop(0)
        if head_cor in snake_copy:
            return True
        return False

    def grow(self, treasure):
        x, y = self.snake_[0]
        if treasure.is_treasure(x, y):
            if len(self.snake_) != 1:
                self.snake_.append(self.snake_[-1])
            else:
                self.snake_.append(None)

            treasure.change()


class Treasure:
    def __init__(self):
        self.change()

    def is_treasure(self, x, y):
        if x == self.x and y == self.y:
            return True
        return False

    def change(self):
        self.x = random.randint(0, len(board[0]) - 1)
        self.y = random.randint(0, len(board)) - 1

    def update(self):
        board[self.y][self.x].paint(c_treasure)


def build():
    global board
    board = list()
    for y in range(0, HEIGHT, HEIGHT // game_zoom):
        row = list()
        for x in range(0, WIDTH, WIDTH // game_zoom):
            row.append(Area(x, y, WIDTH // game_zoom, HEIGHT // game_zoom))
        board.append(row)
    board_reset()


def board_reset():
    for y in range(len(board)):
        for x in range(len(board[y])):
            board[y][x].paint(c_background)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(c_background)
pygame.display.set_caption("snake || Erxuan Li")
clock = pygame.time.Clock()

build()
snake = Snake()
treasure = Treasure()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                snake.change_direction("left")
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                snake.change_direction("right")
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                snake.change_direction("up")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                snake.change_direction("down")

    board_reset()
    if not snake.is_dead():
        snake.update_movement()

    treasure.update()
    snake.update()
    snake.grow(treasure)
    pygame.display.update()
    clock.tick(difficulty)
