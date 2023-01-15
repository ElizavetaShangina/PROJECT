import pygame
from ctypes import *
import sys
from first_window import draw_background

pygame.init()
SCREEN_WIDTH = windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = windll.user32.GetSystemMetrics(1) - 50
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
characters = ['Dio Brando', 'Sasuke', 'Kuchiki Rukia', 'Aizen Sousuke']
image_num = [13, 12, 7, 14]
scales = [2, 5, 1, 1]
fps = 10
all_sprites = pygame.sprite.Group()


def load_image(path, colorkey=None):
    image = pygame.image.load(path)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Character(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.name = name
        self.x, self.y = x, y
        self.columns = image_num[characters.index(self.name)]
        self.scale = scales[characters.index(self.name)]
        sheet = load_image(f'project_files\\{self.name} win.png')
        self.cut_sheet(sheet, self.columns)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(self.x, self.y)
        all_sprites.add(self)

    def cut_sheet(self, sheet, columns, rows=1):
        frame_width = sheet.get_width() // columns
        frame_height = sheet.get_height()
        self.rect = pygame.Rect(0, 0, frame_width, frame_height)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                image = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                transformed_image = pygame.transform.scale(image, (frame_width * self.scale, frame_height * self.scale))
                self.frames.append(transformed_image)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Button:
    def __init__(self, width, height, x, y, text, action=None):
        self.width = width
        self.height = height
        self.x, self.y = x, y
        self.text = text
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 30)
        text = font.render(self.text, True, (255, 255, 255))
        text_x, text_y = self.x + 20, self.y + 15
        screen.blit(text, (text_x, text_y))
        pygame.display.flip()

    def update(self, pos):
        if self.action and self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            action = self.action
            action()


def terminate():
    pygame.quit()
    sys.exit()


def draw_end(winners_name, winners_character):
    background_rect, background_width, background_height, background_x1, background_y1 = draw_background()
    text = f'The Winner is {winners_name}'
    font = pygame.font.Font(None, 100)
    text = font.render(text, True, (255, 0, 0))
    text_w = text.get_width()
    text_h = text.get_height()
    text_x = background_x1 + 0.5 * background_width - text_w // 2
    text_y = background_y1 + 100
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()

    button_exit = Button(200, 50, background_x1 + background_width - 300,
                         background_y1 + background_height - 100, 'Выйти из игры', terminate)
    button_exit.draw()

    Character(winners_character, background_x1 + background_width // 2 - 50, background_y1 + background_height // 2 - 50)
    all_sprites.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_exit.update(event.pos)
        draw_background()
        screen.blit(text, (text_x, text_y))
        button_exit.draw()
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
