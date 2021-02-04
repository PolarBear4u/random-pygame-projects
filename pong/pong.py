import pygame
from pygame import *

pygame.init()

#settings
fps = 30
line_speed = 3

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

c_background = black
c_line = white



class Line:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def change_x(self, step): # subtract --> up; add --> down
        if self.y + step > 0 and self.y + step + self.height < HEIGHT:
            self.y += step
        print(self.y)

    def update(self):
        pygame.draw.rect(screen, c_line, pygame.Rect(self.x, self.y, self.width, self.height))

    
        


screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(c_background)
pygame.display.set_caption("pong || Erxuan Li")
clock = pygame.time.Clock()

line = Line(10, 10, 10, 20)

running = True
while running:
    screen.fill(c_background)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                line.change_x(10)


    line.update()
    pygame.display.update()
    clock.tick(fps)

pygame.quit()
