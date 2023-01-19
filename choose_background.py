import pygame
import sys
from ctypes import *
from first_window import draw_background

pygame.init()
SCREEN_WIDTH = windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = windll.user32.GetSystemMetrics(1) - 50
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
fonts = [['night town', 'ruined house in the forest'], ['ruined village', 'sunset']]
background_rect, background_width, background_height, background_x1, background_y1 = draw_background()
start_width = background_x1 + 250
start_height = 90 + background_y1
card_width = 200
card_height = 150
chosen_font = ''


class Font(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        self.name = name
        image = pygame.image.load(f'project_files\\{name}.jpg')
        image1 = pygame.transform.scale(image, (card_width, card_height))
        self.image = image1
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.is_selected = False
        all_sprites.add(self)

    def update(self, pos=(0, 0)):
        global chosen_font
        if self.rect.collidepoint(pos[0], pos[1]):
            if not self.is_selected:
                self.is_selected = True
                chosen_font = self.name
        elif chosen_font != self.name:
            self.is_selected = False


font_sprites = []
for i in range(2):
    font1 = []
    for j in range(2):
        font1.append(Font(start_width + 250 * i, start_height + 200 * j, fonts[i][j]))
    font_sprites.append(font1)


def terminate():
    pygame.quit()
    sys.exit()


def select_background():
    global start_height, start_width, chosen_font
    background_rect, background_width, background_height, background_x1, background_y1 = draw_background()
    pygame.display.flip()
    fps = 10
    font = pygame.font.Font(None, 50)
    text = font.render("Выберите арену:", True, (255, 255, 255))
    text_x = background_x1 + 25
    text_y = background_y1 + 40
    screen.blit(text, (text_x, text_y))

    #Отрисовка кнопки далее
    btn_x, btn_y = background_x1 + background_width - 200, background_y1 + background_height - 80
    btn_w, btn_h = 110, 40
    pygame.draw.rect(screen, pygame.Color('black'),
                     (btn_x, btn_y, btn_w, btn_h))
    font = pygame.font.Font(None, 30)
    text = font.render("Continue", True, (255, 255, 255))
    text_x = btn_x + 10
    text_y = btn_y + 10
    screen.blit(text, (text_x, text_y))

    # Отрисовка карточек фона
    for i in range(2):
        for j in range(2):
            color = 'black'
            if font_sprites[i][j].is_selected:
                color = 'red'
            pygame.draw.rect(screen, pygame.Color(color),
                             (font_sprites[i][j].rect.x - 5, font_sprites[i][j].rect.y - 5,
                              card_width + 10, card_height + 10), 5)
            font = pygame.font.Font(None, 30)
            text = font.render(fonts[i][j], True, (255, 255, 255))
            text_w = text.get_width()
            text_h = text.get_height()
            text_x = font_sprites[i][j].rect.x + card_width // 2 - text_w // 2
            text_y = font_sprites[i][j].rect.y + card_height + 10
            screen.blit(text, (text_x, text_y))
            pygame.display.flip()
    all_sprites.draw(screen)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if btn_x < pos[0] <= btn_w + btn_x and btn_y < pos[1] < btn_h + btn_y:
                    if chosen_font:
                        return chosen_font
                else:
                    all_sprites.update(pos)
                    all_sprites.update()
                    for i in range(2):
                        for j in range(2):
                            color = 'black'
                            if font_sprites[i][j].is_selected:
                                color = 'red'
                            pygame.draw.rect(screen, pygame.Color(color),
                                             (font_sprites[i][j].rect.x - 5, font_sprites[i][j].rect.y - 5,
                                              card_width + 10, card_height + 10), 5)

        pygame.display.flip()
        clock.tick(fps)
