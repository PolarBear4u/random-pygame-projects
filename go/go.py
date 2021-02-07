import pygame
from pygame import *
import sys
import os

pygame.init()

# settings
fps = 30
lines = 19
stone_scale = 18
white_stone_outline_width = 2
description_distance = 30
line_width = 2
orientation_point_radius = 8
description_top, description_bot, description_left, description_right = True, True, True, True
WIDTH, HEIGHT = 900, 900

board_width, board_height = int(WIDTH * 0.8), int(HEIGHT * 0.8)
board_edge = (WIDTH - board_width) // 2


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

c_background = white
c_line = black
c_stone_black = black
c_stone_white = white
c_description = black

font_32 = pygame.font.Font(pygame.font.get_default_font(), 32)


class Area:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.radius = r

        self.color = None

        self.left = self.x - self.radius
        self.top = self.y - self.radius
        self.width = self.radius * 2
        self.height = self.width

        self.neighbors = list()
        self.previous = list()

    def draw_black(self):

        pygame.draw.circle(screen, c_stone_black,
                           (self.x, self.y), self.radius)

    def draw_white(self):

        pygame.draw.circle(screen, c_stone_white,
                           (self.x, self.y), self.radius)
        pygame.draw.circle(screen, black, (self.x, self.y),
                           self.radius, white_stone_outline_width)

    def draw(self):
        if self.color == c_stone_black:
            self.draw_black()
        elif self.color == c_stone_white:
            self.draw_white()
        else:
            pass

    def res_color(self):
        self.color = None

    def set_color(self, color):
        self.color = color

    def my_color(self):
        return self.color

    def is_stone(self):
        if self.color == c_stone_black or self.color == c_stone_white:
            return True
        return False

    def touch(self, x, y):

        if x > self.left and x < self.left + self.width and y > self.top and y < self.top + self.height:
            return True
        return False

    def dead(self):
        if not self.is_stone():
            return False
        count = 0
        self.previous = [self]
        for neighbor in self.neighbors:

            count += 1
            if neighbor is None:
                if count == 4:
                    return True
                continue
            elif not neighbor.is_stone():
                return False
            else:
                if neighbor.my_color() == self.color:
                    if neighbor.dead_sup(self.previous):
                        if count == 4:
                            return True
                        continue
                    else:
                        return False
                else:
                    if count == 4:
                        return True
                    continue

    def dead_sup(self, previous):
        self.previous = previous
        count = 0
        for neighbor in self.neighbors:
            count += 1
            if neighbor is None:
                if count == 4:
                    return True
                continue
            elif not neighbor.is_stone():
                return False
            elif neighbor in self.previous:
                if count == 4:
                    return True
                continue
            else:
                if neighbor.my_color() == self.color:
                    self.previous.append(self)
                    if neighbor.dead_sup(self.previous):
                        if count == 4:
                            return True

                        continue
                    else:
                        return False
                else:
                    if count == 4:
                        return True
                    continue

    def receive_neighbors(self, neighbors):
        self.neighbors = neighbors


class Main:
    def __init__(self):
        self.board = list()
        self.build_board_list()
        self.build()
        self.give_neightbors()

    def update(self):
        self.build()
        self.update_stones()

    def update_stones(self):
        for row in self.board:
            for area in row:
                area.draw()

    def build(self):
        for i in range(board_edge, WIDTH - board_edge + 1, (WIDTH - board_edge) // (lines + 1)):
            pygame.draw.line(screen, c_line, (board_edge, i),
                             (HEIGHT - board_edge, i), line_width)
        for i in range(board_edge, HEIGHT - board_edge + 1, (HEIGHT - board_edge) // (lines + 1)):
            pygame.draw.line(screen, c_line, (i, board_edge),
                             (i, WIDTH - board_edge), line_width)

        self.orientation_points()
        self.board_description(
            description_top, description_bot, description_left, description_right)

    def build_board_list(self):
        for y in range(board_edge, WIDTH - board_edge + 1, (WIDTH - board_edge) // (lines + 1)):
            row = list()
            for x in range(board_edge, HEIGHT - board_edge + 1, (HEIGHT - board_edge) // (lines + 1)):
                row.append(Area(x, y, stone_scale))
            self.board.append(row)

    def orientation_points(self):
        for y in range(board_edge + (3 * board_height // lines) + 8, HEIGHT - board_edge - (3 * board_height // lines), 6 * board_height // lines + 13):
            for x in range(board_edge + (3 * board_width // lines) + 8, WIDTH - board_edge - (3 * board_width // lines), 6 * board_width // lines + 13):
                pygame.draw.circle(screen, c_line, (x, y),
                                   orientation_point_radius)

    def board_description(self, top, bot, left, right):

        if bot:
            n = None
            for i in range(lines):
                y = board_edge + board_height + description_distance
                x = board_edge + (i * (WIDTH - board_edge) // (lines + 1)) - 12
                char = 65 + i
                if i == 8:
                    char += 1
                    n = 0
                if n != None and i != 8:
                    char += 1
                screen.blit(font_32.render(
                    chr(char), True, c_description), (x, y))
        if top:
            n = None
            for i in range(lines):
                y = board_edge - description_distance - 30
                x = board_edge + (i * (WIDTH - board_edge) // (lines + 1)) - 12
                char = 65 + i
                if i == 8:
                    char += 1
                    n = 0
                if n != None and i != 8:
                    char += 1
                screen.blit(font_32.render(
                    chr(char), True, c_description), (x, y))

        if left:

            for i in range(lines, 0, -1):
                y = board_edge + \
                    (abs(i - 19) * (HEIGHT - board_edge) // (lines + 1)) - 20
                x = board_edge - description_distance - 30
                screen.blit(font_32.render(
                    str(i), True, c_description), (x, y))

        if right:

            for i in range(lines, 0, -1):
                y = board_edge + \
                    (abs(i - 19) * (HEIGHT - board_edge) // (lines + 1)) - 20
                x = board_width + board_edge + description_distance
                screen.blit(font_32.render(
                    str(i), True, c_description), (x, y))

    def stone_clicked(self, x, y, color, admin):
        for row in self.board:
            for area in row:
                if area.touch(x, y):
                    if not area.is_stone() or admin:
                        area.set_color(color)
                    

    def test_stones(self):
        for row in self.board:
            for item in row:
                item.draw_black()

        self.board[7][4].draw_white()

    def give_neightbors(self):
        for y in range(0, len(self.board)):
            for x in range(0, len(self.board[0])):
                neighbors = list()
                for i in range(4):
                    try:
                        if i == 0:  # top
                            if y - 1 < 0:
                                raise IndexError
                            neighbors.append(self.board[y - 1][x])
                        elif i == 1:  # right
                            if x + 1 > len(self.board[0]) - 1:
                                raise IndexError
                            neighbors.append(self.board[y][x + 1])
                        elif i == 2:  # bot
                            if y + 1 > len(self.board) - 1:
                                raise IndexError
                            neighbors.append(self.board[y + 1][x])
                        elif i == 3:  # left
                            if x - 1 < 0:
                                raise IndexError
                            neighbors.append(self.board[y][x - 1])
                    except IndexError:
                        neighbors.append(None)
                self.board[y][x].receive_neighbors(neighbors)

    def remove_dead(self):
        dead_stones = list()
        for row in self.board:
            for area in row:
                if area.dead():
                    dead_stones.append(area)
        for dead_stone in dead_stones:
            dead_stone.res_color()

    def test_neightbors(self):
        print(self.board[0][0].neighbors)
        for nei in self.board[0][0].neighbors:
            try:
                print(nei.x)
            except:
                print("None")

    def test_dead(self):
        return self.board[0][0].dead()

    def reset_all(self):
        for row in self.board:
            for area in row:
                area.res_color()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(
    "go || Erxuan || i, j, k, l --> toggle description || left --> black ; right --> white ; mid --> del")
background_image = pygame.image.load(resource_path("oak_texture.jpg"))
clock = pygame.time.Clock()

main = Main()

running = True
while running:
    screen.fill(c_background)
    screen.blit(background_image, (0, 0))
    main.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                main.stone_clicked(mouse_x, mouse_y, c_stone_black, False)
            elif event.button == 2:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                main.stone_clicked(mouse_x, mouse_y, None, True)
            elif event.button == 3:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                main.stone_clicked(mouse_x, mouse_y, c_stone_white, False)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                print(main.test_dead())
            elif event.key == pygame.K_i:
                description_top = not description_top
            elif event.key == pygame.K_j:
                description_left = not description_left
            elif event.key == pygame.K_k:
                description_bot = not description_bot
            elif event.key == pygame.K_l:
                description_right = not description_right
            elif event.key == pygame.K_r:
                main.reset_all()

    main.remove_dead()
    pygame.display.update()
    clock.tick(fps)
