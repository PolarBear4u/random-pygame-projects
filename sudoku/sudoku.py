import pygame
import random

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

background_color = white
center_mark_color = light_gray
center_note_mark_color = orange
neighbor_mark_color = light_gray_2
grid_color = black
main_grid_color = blue
number_color = black
note_number_color = gray
correct_number_color = lime
puzzle_number_area_color = light_blue_2

difficulty_of_game = 90

font_32 = pygame.font.Font(pygame.font.get_default_font(), 32)
font_64 = pygame.font.Font(pygame.font.get_default_font(), 64)


class Area:
    def __init__(self, x, y, width, height, number, note_number):
        self.x = x
        self.y = y
        self.endX = x + width
        self.endY = y + height
        self.width = width
        self.height = height
        self.number = number
        self.note_number = note_number

    def paint_area(self, color):
        pygame.draw.rect(screen, color, pygame.Rect(
            self.x + 1, self.y + 1, self.width - 1, self.height - 1))
        self.color = color

    def show_number(self):
        if self.number != None:
            num_txt = font_64.render(f"{self.number}", True, number_color)
            screen.blit(num_txt, (self.x + 34, self.y + 22))

    def show_note_number(self):
        if self.note_number != None:
            note_num_txt = font_32.render(
                f"{self.note_number}", True, note_number_color)
            screen.blit(note_num_txt, (self.x + 76, self.y + 6))

    def change_number(self, number):
        self.number = number

    def change_note_number(self, note_number):
        self.note_number = note_number

    def get_cors(self):
        return self.x, self.y

    def get_color(self):
        return self.color

    def get_number(self):
        return self.number

    def get_note_number(self):
        return self.note_number

    def is_in_area(self, x, y):
        if x > self.x and x <= self.endX and y > self.y and y <= self.endY:
            return True
        return False


def build_board_9x9():

    global all_nums_9x9
    all_nums_9x9 = [[[] for i in range(9)] for j in range(9)]

    gapsW = WIDTH // 9
    gapsH = HEIGHT // 9
    for i in range(0, WIDTH + 1, gapsW):
        pygame.draw.line(screen, grid_color, (i, 0), (i, HEIGHT))
        if i == WIDTH // 3 or i == WIDTH // 3 * 2:
            pygame.draw.line(screen, main_grid_color, (i, 0), (i, HEIGHT))

    for i in range(0, HEIGHT + 1, gapsH):
        pygame.draw.line(screen, grid_color, (0, i), (WIDTH, i))
        if i == HEIGHT // 3 or i == HEIGHT // 3 * 2:
            pygame.draw.line(screen, main_grid_color, (0, i), (WIDTH, i))

    for y in range(len(all_nums_9x9)):
        for x in range(len(all_nums_9x9[y])):
            all_nums_9x9[y][x] = Area(
                x * gapsW, y * gapsH, gapsW, gapsH, None, None)


def num_pos_valid(x, y, num):
    for i in range(9):
        if all_nums_9x9[i][x].get_number() == num:
            return False
    for i in range(9):
        if all_nums_9x9[y][i].get_number() == num:
            return False
    gX = x // 3 * 3
    gY = y // 3 * 3
    for i in range(3):
        for j in range(3):
            if all_nums_9x9[i + gY][j + gX].get_number() == num:
                return False
    return True


def solve_puzzle_9x9(user_puzzle):
    if not user_puzzle:
        for y in range(9):
            for x in range(9):
                if all_nums_9x9[y][x].get_color() != puzzle_number_area_color and all_nums_9x9[y][x].get_color() != correct_number_color:
                    all_nums_9x9[y][x].change_number(None)
                    all_nums_9x9[y][x].change_note_number(None)

    first_time = True
    try:
        def solve():

            for y in range(9):
                for x in range(9):
                    if all_nums_9x9[y][x].get_number() == None:
                        n_range = list(range(1, 10))
                        # shuffling the numbers for the usage of this method in generate_puzzle_9x9()
                        random.shuffle(n_range)
                        for i in n_range:
                            if num_pos_valid(x, y, i):
                                all_nums_9x9[y][x].paint_area(
                                    correct_number_color)
                                all_nums_9x9[y][x].change_number(i)
                                solve()
                                all_nums_9x9[y][x].paint_area(white)
                                all_nums_9x9[y][x].change_number(None)

                        return
            raise IndexError

        if first_time:
            first_time = False
            solve()
    except IndexError:
        pass


def generate_puzzle_9x9(difficulty):

    reset_all()
    solve_puzzle_9x9(False)
    for y in range(9):
        for x in range(9):
            all_nums_9x9[y][x].paint_area(puzzle_number_area_color)
    for i in range(difficulty):
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        all_nums_9x9[y][x].paint_area(background_color)
        all_nums_9x9[y][x].change_number(None)


def mark_neighbors_and_cen(x, y, cen_color):
    for i in range(9):
        if all_nums_9x9[y][i].get_color() == puzzle_number_area_color or all_nums_9x9[y][i].get_color() == correct_number_color:
            pass
        else:
            all_nums_9x9[y][i].paint_area(neighbor_mark_color)
    for i in range(9):
        if all_nums_9x9[i][x].get_color() == puzzle_number_area_color or all_nums_9x9[i][x].get_color() == correct_number_color:
            pass
        else:
            all_nums_9x9[i][x].paint_area(neighbor_mark_color)
    gX = x // 3 * 3
    gY = y // 3 * 3
    for i in range(3):
        for j in range(3):
            if all_nums_9x9[gY + i][gX + j].get_color() == puzzle_number_area_color or all_nums_9x9[gY + i][gX + j].get_color() == correct_number_color:
                pass
            else:
                all_nums_9x9[gY + i][gX + j].paint_area(neighbor_mark_color)
    if all_nums_9x9[y][x].get_color() != puzzle_number_area_color and all_nums_9x9[y][x].get_color() != correct_number_color:
        all_nums_9x9[y][x].paint_area(cen_color)


def reset_all():
    for y in range(9):
        for x in range(9):
            all_nums_9x9[y][x].paint_area(background_color)
            all_nums_9x9[y][x].change_number(None)
            all_nums_9x9[y][x].change_note_number(None)


icon = pygame.image.load("Fisch.jpg")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(background_color)
pygame.display.set_caption(
    "Sudoku | Erxuan Li || n: generate new puzzle | s: solve puzzle | d: solve own puzzle | r: reset || possible loading time: solving, generating")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

build_board_9x9()

for i in range(9):
    for j in range(9):
        all_nums_9x9[i][j].paint_area(background_color)


number_inputs = list()
for i in range(1, 10):
    number_inputs.append("pygame.K_" + str(i))
    print(number_inputs)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left mouse button
                color = center_mark_color
            elif event.button == 3:  # right mouse button
                color = center_note_mark_color
            else:
                color = background_color
            lX, lY = None, None
            xcor, ycor = pygame.mouse.get_pos()
            for y in range(9):
                for x in range(9):
                    if all_nums_9x9[y][x].is_in_area(xcor, ycor):
                        lX, lY, =  x, y
                    if all_nums_9x9[y][x].get_color() != puzzle_number_area_color and all_nums_9x9[y][x].get_color() != correct_number_color:

                        all_nums_9x9[y][x].paint_area(background_color)
            mark_neighbors_and_cen(lX, lY, color)

        if event.type == pygame.KEYDOWN:

            # 1 to 9 on the keyboard and backspace
            for y in range(9):
                for x in range(9):
                    if all_nums_9x9[y][x].get_color() == center_mark_color:
                        for num in range(1, 10):
                            if event.key == eval(number_inputs[num - 1]):
                                all_nums_9x9[y][x].paint_area(
                                    center_mark_color)
                                all_nums_9x9[y][x].change_number(num)
                            elif event.key == pygame.K_BACKSPACE:
                                all_nums_9x9[y][x].paint_area(
                                    center_mark_color)
                                all_nums_9x9[y][x].change_number(None)
                    elif all_nums_9x9[y][x].get_color() == center_note_mark_color:
                        for num in range(1, 10):
                            if event.key == eval(number_inputs[num - 1]):
                                all_nums_9x9[y][x].paint_area(
                                    center_note_mark_color)
                                all_nums_9x9[y][x].change_note_number(num)
                            elif event.key == pygame.K_BACKSPACE:
                                all_nums_9x9[y][x].paint_area(
                                    center_note_mark_color)
                                all_nums_9x9[y][x].change_note_number(None)

            if event.key == pygame.K_s:
                solve_puzzle_9x9(False)

            if event.key == pygame.K_n:
                generate_puzzle_9x9(difficulty_of_game)

            if event.key == pygame.K_d:
                solve_puzzle_9x9(True)

            if event.key == pygame.K_r:
                reset_all()

        

    for y in range(9):
        for x in range(9):
            all_nums_9x9[y][x].show_number()
            all_nums_9x9[y][x].show_note_number()

    pygame.display.update()
    clock.tick(60)


pygame.quit()
