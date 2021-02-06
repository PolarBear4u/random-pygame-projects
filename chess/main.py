import pygame
from pygame import *


pygame.init()


fps = 60

WIDTH, HEIGHT = 900, 900
board_width, board_height = 800, 800

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

c_background = red
c_black = black
c_white = white
c_board_black = blue
c_board_white = orange

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chess || Erxuan Li")
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(c_background)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
