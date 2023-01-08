import pygame.time

from first_window import draw_background, draw_first_window
from player_names import input_player_names
from character_selecting_menu import draw_menu


intro_sound = pygame.mixer.Sound('project_files\\intro.wav')
pygame.mixer.Sound.play(intro_sound)

draw_first_window()

font = pygame.mixer.Sound('project_files\\select.wav')
pygame.mixer.Sound.play(font, -1)

player1, player2 = input_player_names()
player1_character, player2_character = draw_menu(player1, player2)

pygame.mixer.Sound.stop(font)
print(player1, player2)
