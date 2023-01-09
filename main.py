import pygame
from first_window import draw_background, draw_first_window
from player_names import input_player_names
from character_selecting_menu import draw_menu
from choose_background import select_background


intro_sound = pygame.mixer.Sound('project_files\\intro.wav')
pygame.mixer.Sound.play(intro_sound)

draw_first_window()

font = pygame.mixer.Sound('project_files\\select.wav')
pygame.mixer.Sound.play(font, -1)

player1, player2 = input_player_names()
player1_character, player2_character = draw_menu(player1, player2)
background = select_background()

pygame.mixer.Sound.stop(font)
"""
fight_intro = pygame.mixer.Sound('project_files\\fight_intro.wav')
pygame.mixer.Sound.play(fight_intro)
fight_music = pygame.mixer.Sound('project_files\\fight_font.wav')
pygame.mixer.Sound.play(fight_music, -1)

# Вызов основной функции

pygame.mixer.Sound.stop(fight_music)
win = pygame.mixer.Sound('project_files\\winner.mp3')
pygame.mixer.Sound.play(win)
pygame.mixer.Sound.play(font, -1)

# Вызов завершающей функции
"""
