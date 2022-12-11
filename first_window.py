import pygame
import sys
from ctypes import *


class MainWindow:
    def __init__(self):
        self.fps = 60
        self.character_number = 4
        self.character_card_width = 100
        self.character_card_height = 150
        self.characters = ['персонаж 1', 'персонаж 2', 'персонаж 3', 'персонаж 4']
        self.player1 = ''
        self.player2 = ''
        self.current_player = -1

    def draw_background(self):
        screen.fill((0, 0, 0))
        background = pygame.image.load('project_files\\forest.jpg')
        background_rect = background.get_rect()
        self.background_width = background_rect[2]
        self.background_height = background_rect[3]
        self.background_x1 = (SCREEN_WIDTH - self.background_width) / 2
        self.background_y1 = (SCREEN_HEIGHT - self.background_height) / 2
        screen.blit(background, (self.background_x1, self.background_y1, self.background_x1 + self.background_width,
                                 self.background_y1 + self.background_height))

    def draw_first_window(self):
        self.draw_background()

        #  Вывод названия игры
        for i in range(125):
            self.draw_background()
            font = pygame.font.Font(None, i)
            text = font.render("Межвселенная битва", True, (255, 0, 0))
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = self.background_x1 + 0.5 * self.background_width - text_w // 2
            text_y = self.background_y1 + 0.5 * self.background_height - text_h // 2 + 10
            screen.blit(text, (text_x, text_y))
            pygame.display.flip()
            clock.tick(self.fps)

        # "Нажмите, чтобы продолжить"
        font = pygame.font.Font(None, 40)
        text = font.render("Нажмите, чтобы продолжить", True, (255, 255, 255))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = self.background_x1 + 0.5 * self.background_width - text_w // 2
        text_y = self.background_y1 + self.background_height - text_h - 20
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()

    def draw_character_selection_menu(self):
        self.draw_background()
        pygame.display.flip()

        # Название окна
        font = pygame.font.Font(None, 50)
        text = font.render("Выберите своего персонажа:", True, (255, 255, 255))
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = self.background_x1 + 25
        text_y = self.background_y1 + 50
        screen.blit(text, (text_x, text_y))

        # Отрисовка выбора номера игрока и кнопки далее
        button_names = ['Player 1', 'Player 2', 'Continue']
        self.card_height = 60
        self.card_width = 150
        self.useful_card_start_width = 150 + self.background_x1
        self.useful_card_start_height = text_h + 80 + self.background_y1 + self.background_height - self.card_height
        start_width = self.useful_card_start_width
        colors = ['red', 'blue']
        for i in range(3):
            pygame.draw.rect(screen, pygame.Color('black'),
                             (start_width + i * self.card_width,
                              self.useful_card_start_height, self.card_width, self.card_height))
            if self.current_player - 1 == i:
                pygame.draw.rect(screen, pygame.Color(colors[i]),
                                 (start_width + i * self.card_width - 2,
                                  self.useful_card_start_height - 2, self.card_width + 2, self.card_height + 2), 2)
            font = pygame.font.Font(None, 30)
            text = font.render(button_names[i], True, (255, 255, 255))
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = start_width + (i + 0.5) * self.card_width - text_w // 2
            text_y = self.useful_card_start_height + self.card_height // 2 - text_h // 2
            screen.blit(text, (text_x, text_y))
            start_width += 100
        pygame.display.flip()

        # Отрисовка карточек персонажей
        self.character_card_start_width = 120 + self.background_x1
        self.character_card_start_height = 140 + self.background_y1
        start_width = self.character_card_start_width
        for i in range(self.character_number):
            color = 'black'
            if self.player1 == self.characters[i]:
                color = 'red'
            elif self.player2 == self.characters[i]:
                color = 'blue'
            pygame.draw.rect(screen, pygame.Color(color),
                             (start_width + i * self.character_card_width - 2, self.character_card_start_height - 2,
                              self.character_card_width + 2, self.character_card_height + 2), 2)
            font = pygame.font.Font(None, 30)
            text = font.render(self.characters[i], True, (255, 255, 255))
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = start_width + (i + 0.5) * self.character_card_width - text_w // 2
            text_y = self.character_card_start_height + self.character_card_height + 5
            screen.blit(text, (text_x, text_y))
            pygame.display.flip()
            start_width += 100
        pygame.display.flip()

    def draw_main_window(self):
        pass

    def on_click(self, position, window_name):
        if window_name == 'first_window':
            self.draw_character_selection_menu()
            return 'second_window'
        elif window_name == 'second_window':
            if self.character_card_start_height <= position[1] <= self.character_card_start_height + \
                    self.character_card_height:
                character_number = round((position[0] - self.character_card_start_width) //
                                         (self.character_card_width + 100))
                if self.current_player != -1:
                    if self.current_player == 1:
                        if self.player1:
                            self.player1 = self.characters[character_number]
                            self.draw_character_selection_menu()
                            return 'second_window'
                        else:
                            color = 'red'
                            self.player1 = self.characters[character_number]
                    else:
                        if self.player2:
                            self.player2 = self.characters[character_number]
                            self.draw_character_selection_menu()
                            return 'second_window'
                        else:
                            self.player2 = self.characters[character_number]
                            color = 'blue'
                    pygame.draw.rect(screen, pygame.Color(color),
                                     (self.character_card_start_width + character_number *
                                      (self.character_card_width + 100) - 2,
                                      self.character_card_start_height - 2, self.character_card_width + 2,
                                      self.character_card_height + 2), 2)
                    pygame.display.flip()
                    return 'second_window'
            elif self.useful_card_start_height <= position[1] <= self.card_height + self.useful_card_start_height:
                button_number = round((position[0] - self.useful_card_start_width) // (self.card_width + 100))
                if button_number == 2 and self.player1 and self.player2:
                    self.draw_main_window()
                    return 'third_window'
                elif button_number == 2:
                    print('Выберите персонажа для обоих игроков')
                else:
                    if button_number == 0:
                        self.current_player = 1
                    if button_number == 1:
                        self.current_player = 2
                    self.draw_character_selection_menu()
                    return 'second_window'


if __name__ == '__main__':
    pygame.init()
    SCREEN_WIDTH = windll.user32.GetSystemMetrics(0)
    SCREEN_HEIGHT = windll.user32.GetSystemMetrics(1) - 50
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    window = MainWindow()
    window.draw_first_window()
    current_window = 'first_window'
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_window = window.on_click(event.pos, current_window)
        pygame.time.delay(20)
    pygame.quit()
