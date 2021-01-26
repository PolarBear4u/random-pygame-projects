import pygame
from pygame import *
import time
import string
import random

pygame.init()

WIDTH, HEIGHT = 1000, 600
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
line_color = white
user_box_color = orange
box_color = yellow
title_color = black
wpm_txt_color = black
text_color = black
wront_text_color = red
user_text_color = black
high_score_color = black

icon = pygame.image.load("Fisch.jpg")
background_image = pygame.transform.scale(
    pygame.image.load("Sky.png"), (1000, 600))

font_32 = pygame.font.Font(pygame.font.get_default_font(), 32)
font_64 = pygame.font.Font(pygame.font.get_default_font(), 64)


def build():
    screen.fill(background_color)
    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, user_box_color, pygame.Rect(25, 475, 950, 100))
    pygame.draw.rect(screen, box_color, pygame.Rect(25, 75, 950, 300))
    title = font_32.render("WPM Tester", True, wpm_txt_color)
    screen.blit(title, (20, 20))


def show_text(text, right):
    if right:
        txt = font_32.render(text, True, text_color)
    else:
        txt = font_32.render(text, True, wront_text_color)
    screen.blit(txt, (50, 100))


def show_user_text(user_text):
    text = font_32.render(f"{user_text}|", True, user_text_color)
    screen.blit(text, (50, 500))


def show_high_score(score, current_high_score):
    score_text = None
    if score > current_high_score:
        score_text = score
    else:
        score_text = current_high_score
    text = font_32.render(f"High Score: {score} WPM", True, high_score_color)
    screen.blit(text, (50., 300))
    return score_text


def set_wpm_text(start_time, len_of_all_words, done, last_time):
    if not done:
        current_time = time.time()

    else:
        current_time = last_time
    wpm_txt = font_32.render(
        f"WPM: {(score := int((len_of_all_words / 5) / ((current_time - start_time) / 60)))}", True, black)
    screen.blit(wpm_txt, (825, 20))

    return current_time, score


def sync(text, user_text):
    t_list = text.split()
    u_list = user_text.split()
    right = True
    len_of_word = None
    done = False
    if len(u_list) != 0 and len(t_list) != 0:
        if t_list[0] == u_list[0]:
            len_of_word = len(t_list[0])
            t_list.pop(0)
            u_list.pop(0)
            text = ' '.join(t_list)
            user_text = ' '.join(u_list)
        else:
            if t_list[0].startswith(u_list[0]):
                right = True
            else:
                right = False
    if len(text) == 0:
        done = True

    return text, user_text, right, len_of_word, done


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(icon)
pygame.display.set_caption("WPM Tester || Erxuan Li")
clock = pygame.time.Clock()

user_text = ""
text = "Welcome xD"
start_time = time.time()
len_of_all_words = 0
current_high_score = 0
last_time = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and event.mod & pygame.KMOD_LCTRL:

                if len(user_text) != 0:
                    user_text_list = user_text.split()
                    user_text_list.pop()
                    user_text = ' '.join(user_text_list)

            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]

            elif event.key == pygame.K_n and event.mod & pygame.KMOD_LCTRL:
                user_text = ""
                start_time = time.time()
                len_of_all_words = 0
                text = ' '.join([''.join([random.choice(string.ascii_lowercase) for i in range(random.randint(5, 7))]) for j in range(7)])
            else:
                if len(user_text) <= 50:
                    user_text += event.unicode

            

    text, user_text, right, len_of_word, done = sync(text, user_text)
    if len_of_word is not None:
        len_of_all_words += len_of_word + 1
    build()
    last_time, score = set_wpm_text(start_time, len_of_all_words, done, last_time)
    show_text(text, right)
    show_user_text(user_text)
    current_high_score = show_high_score(current_high_score, score)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
