import pygame
import sys
from ctypes import *
from first_window import draw_background

pygame.init()
SCREEN_WIDTH = windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = windll.user32.GetSystemMetrics(1) - 50
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
fps = 60


def terminate():
    pygame.quit()
    sys.exit()


def print_text(background_x1, background_y1, name1='', name2=''):
    draw_background()
    font = pygame.font.Font(None, 50)
    text = font.render('First player name:     ' + name1, True, (255, 255, 255))
    text_x, text_y = 50 + background_x1, background_y1 + 100
    screen.blit(text, (text_x, text_y))
    font = pygame.font.Font(None, 50)
    text = font.render('Second player name:    ' + name2, True, (255, 255, 255))
    text_x, text_y = 50 + background_x1, background_y1 + 300
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()


def input_player_names():
    background_rect, background_width, background_height, background_x1, background_y1 = draw_background()
    need_input1, need_input2 = True, False
    player1_name, player2_name = '', ''
    print_text(background_x1, background_y1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if need_input1:
                    if event.key == pygame.K_RETURN:
                        need_input1 = False
                        need_input2 = True
                    elif event.key == pygame.K_BACKSPACE:
                        player1_name = player1_name[:-1]
                    else:
                        player1_name += event.unicode
                elif need_input2:
                    if event.key == pygame.K_RETURN:
                        need_input2 = False
                        return player1_name, player2_name
                    elif event.key == pygame.K_BACKSPACE:
                        player2_name = player2_name[:-1]
                    else:
                        player2_name += event.unicode
            print_text(background_x1, background_y1, player1_name, player2_name)
        pygame.display.flip()
        clock.tick(fps)
