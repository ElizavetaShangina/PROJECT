import pygame


class Fighter:
    def __init__(self, player_numb, x_pos, y_pos, screen_width, screen_height):
        self.x = x_pos
        self.y = y_pos
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.player_numb = player_numb
        if self.player_numb == 1:
            self.color = pygame.Color('red')
        else:
            self.color = pygame.Color('blue')
        self.speed = 10
        self.jump = 40

        self.rect = pygame.Rect(self.x, self.y, 80, 150)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, direction):
        if direction == 'right':
            if self.rect.x + 80 + self.speed <= self.screen_width:
                self.rect.x += self.speed
        elif direction == 'left':
            if self.rect.x - self.speed >= 0:
                self.rect.x -= self.speed

    def jump(self):
        pass

    def bend_down(self):  # пригнуться
        pass

    def attack(self):
        pass
