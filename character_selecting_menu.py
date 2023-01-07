import pygame
import sys
from ctypes import *
from first_window import draw_background

pygame.init()
SCREEN_WIDTH = windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = windll.user32.GetSystemMetrics(1) - 50
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


def terminate():
    pygame.quit()
    sys.exit()


def draw_menu(player1, player2, current_player=-1, player1_character='', player2_character=''):
    background_rect, background_width, background_height, background_x1, background_y1 = draw_background()
    pygame.display.flip()
    fps = 10
    character_number = 4
    character_card_width = 100
    character_card_height = 150
    characters = ['Dio Brando', 'Sasuke', 'Rycon', 'Aizen Sousuke']
    font = pygame.font.Font(None, 50)
    text = font.render("Выберите своего персонажа:", True, (255, 255, 255))
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = background_x1 + 25
    text_y = background_y1 + 50
    text_y = background_y1 + 50
    screen.blit(text, (text_x, text_y))

    # Отрисовка выбора номера игрока и кнопки далее
    button_names = [player1, player2, 'Continue']
    card_height = 60
    card_width = 150
    useful_card_start_width = 150 + background_x1
    useful_card_start_height = text_h + background_y1 + background_height - card_height - 70
    start_width = useful_card_start_width
    colors = ['red', 'blue']
    for i in range(3):
        pygame.draw.rect(screen, pygame.Color('black'),
                         (start_width + i * card_width,
                          useful_card_start_height, card_width, card_height))
        if current_player - 1 == i:
            pygame.draw.rect(screen, pygame.Color(colors[i]),
                             (start_width + i * card_width - 2,
                              useful_card_start_height - 2, card_width + 2, card_height + 2), 2)
        font = pygame.font.Font(None, 30)
        text = font.render(button_names[i], True, (255, 255, 255))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = start_width + (i + 0.5) * card_width - text_w // 2
        text_y = useful_card_start_height + card_height // 2 - text_h // 2
        screen.blit(text, (text_x, text_y))
        start_width += 100
    pygame.display.flip()

    # Отрисовка карточек персонажей
    character_card_start_width = 120 + background_x1
    character_card_start_height = 140 + background_y1
    start_width = character_card_start_width
    all_sprites = pygame.sprite.Group()
    for i in range(character_number):
        color = 'black'
        if player1_character == characters[i]:
            color = 'red'
        elif player2_character == characters[i]:
            color = 'blue'
        pygame.draw.rect(screen, pygame.Color(color),
                         (start_width + i * character_card_width - 2, character_card_start_height - 2,
                          character_card_width + 3, character_card_height + 3), 2)
        fullname = f'project_files\\{characters[i]}.jpg'
        sprite = pygame.sprite.Sprite()
        image = pygame.image.load(fullname)
        image1 = pygame.transform.scale(image, (character_card_width, character_card_height))
        sprite.image = image1
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = start_width + i * character_card_width
        sprite.rect.y = character_card_start_height
        all_sprites.add(sprite)
        font = pygame.font.Font(None, 30)
        text = font.render(characters[i], True, (255, 255, 255))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = start_width + (i + 0.5) * character_card_width - text_w // 2
        text_y = character_card_start_height + character_card_height + 5
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()
        start_width += 100
    all_sprites.draw(screen)
    pygame.display.flip()

    # Обработка нажатий
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = list(event.pos)
                if character_card_start_height <= position[1] <= character_card_start_height + character_card_height:
                    character_number = round((position[0] - character_card_start_width) //
                                             (character_card_width + 100))
                    if current_player != -1:
                        if current_player == 1:
                            if characters[character_number] == player2_character:
                                draw_menu(player1, player2, current_player, player1_character, player2_character)
                            elif player1_character:
                                player1_character = characters[character_number]
                                draw_menu(player1, player2, current_player, player1_character, player2_character)
                            else:
                                color = 'red'
                                player1_character = characters[character_number]
                        else:
                            if characters[character_number] == player1_character:
                                draw_menu(player1, player2, current_player, player1_character, player2_character)
                            elif player2_character:
                                player2_character = characters[character_number]
                                draw_menu(player1, player2, current_player, player1_character, player2_character)
                            else:
                                player2_character = characters[character_number]
                                color = 'blue'
                        pygame.draw.rect(screen, pygame.Color(color),
                                         (character_card_start_width + character_number *
                                          (character_card_width + 100) - 2, character_card_start_height - 2,
                                          character_card_width + 3, character_card_height + 3), 2)
                        pygame.display.flip()
                    draw_menu(player1, player2, current_player, player1_character, player2_character)
                elif useful_card_start_height <= position[1] <= card_height + useful_card_start_height:
                    button_number = round((position[0] - useful_card_start_width) // (card_width + 100))
                    if button_number == 2 and player1_character and player2_character:
                        return player1_character, player2_character
                    elif button_number == 2:
                        print('Выберите персонажа для обоих игроков')
                    else:
                        if button_number == 0:
                            current_player = 1
                        if button_number == 1:
                            current_player = 2
                        draw_menu(player1, player2, current_player, player1_character, player2_character)
        pygame.display.flip()
        clock.tick(fps)
