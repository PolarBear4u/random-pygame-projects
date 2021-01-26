import pygame
from pygame import *
import random

pygame.init()

WIDTH, HEIGHT = 480, 840
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

background_color = black
line_color = white

font_32 = pygame.font.Font(pygame.font.get_default_font(), 32)
font_64 = pygame.font.Font(pygame.font.get_default_font(), 64)



def build():
    gap = WIDTH // 12
    for i in range(0, WIDTH + 1, gap):
        pygame.draw.line(screen, line_color, (i, 0), (i, HEIGHT))
    for i in range(0, HEIGHT + 1, gap):
        pygame.draw.line(screen, line_color, (0, i), (WIDTH, i))

screen = pygame.display.set_mode((WIDTH + 1, HEIGHT + 1))
screen.fill(background_color)
pygame.display.set_caption("Tetris || Erxuan Li")
clock = pygame.time.Clock()

build()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
 

