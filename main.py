from first_window import draw_background, draw_first_window
from player_names import input_player_names
from character_selecting_menu import draw_menu

draw_first_window()
player1, player2 = input_player_names()
player1_character, player2_character = draw_menu(player1, player2)

# Подключение самой игры