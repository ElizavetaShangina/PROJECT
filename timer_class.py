import pygame
from ctypes import *

pygame.init()
SCREEN_WIDTH = windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = windll.user32.GetSystemMetrics(1) - 50
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Timer:
    def __init__(self, middle_x, start_y):
        self.seconds = 0
        self.minutes = 0
        self.text = ''
        self.counter = -1
        self.stop_counting = False
        self.fight_started = False
        self.middle_x = middle_x
        self.start_y = start_y

    def update(self):
        self.counter += 1
        if self.counter % 60 == 0:
            self.seconds += 1
            self.minutes += self.seconds // 60
            self.seconds %= 60
            if not self.stop_counting:
                self.text = f'{self.minutes}:{str(self.seconds).rjust(2, "0")}'
        font = pygame.font.Font(None, 55)
        text = font.render(self.text, True, (255, 0, 0))
        text_w = text.get_width()
        text_x = self.middle_x - text_w // 2
        screen.blit(text, (text_x, self.start_y))

