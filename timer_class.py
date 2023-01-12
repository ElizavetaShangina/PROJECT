import pygame

pygame.init()
screen = pygame.display.set_mode((1200, 600))


class Timer:
    def __init__(self):
        self.seconds = 0
        self.minutes = 0
        self.text = ''
        self.counter = -1

    def update(self):
        self.counter += 1
        if self.counter % 60 == 0:
            self.seconds += 1
            self.minutes += self.seconds // 60
            self.seconds %= 60
            self.text = f'{self.minutes}:{str(self.seconds).rjust(2, "0")}'

        font = pygame.font.Font(None, 55)
        text = font.render(self.text, True, (255, 0, 0))
        text_w = text.get_width()
        text_x = screen.get_width() // 2 - text_w // 2
        text_y = 30
        screen.blit(text, (text_x, text_y))


