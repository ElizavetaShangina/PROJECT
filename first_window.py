import pygame
import sys
from ctypes import *

pygame.init()
SCREEN_WIDTH = windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = windll.user32.GetSystemMetrics(1) - 50
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def draw_background():
    screen.fill((0, 0, 0))
    background = pygame.image.load('project_files\\forest.jpg')
    background_rect = background.get_rect()
    background_width = background_rect[2]
    background_height = background_rect[3]
    background_x1 = (SCREEN_WIDTH - background_width) / 2
    background_y1 = (SCREEN_HEIGHT - background_height) / 2
    screen.blit(background, (background_x1, background_y1, background_x1 + background_width,
                             background_y1 + background_height))
    return background_rect, background_width, background_height, background_x1, background_y1


def draw_first_window():
    background_rect, background_width, background_height, background_x1, background_y1 = draw_background()
    fps = 60

    #  Вывод названия игры
    for i in range(125):
        draw_background()
        font = pygame.font.Font(None, i)
        text = font.render("Межвселенная битва", True, (255, 0, 0))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = background_x1 + 0.5 * background_width - text_w // 2
        text_y = background_y1 + 0.5 * background_height - text_h // 2 + 10
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()
        clock.tick(fps)

    # "Нажмите, чтобы продолжить"
    font = pygame.font.Font(None, 40)
    text = font.render("Нажмите, чтобы продолжить", True, (255, 255, 255))
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = background_x1 + 0.5 * background_width - text_w // 2
    text_y = background_y1 + background_height - text_h - 20
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)
