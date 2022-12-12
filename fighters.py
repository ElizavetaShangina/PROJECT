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

        self.fighter_height = 150
        self.jump_v = 30
        self.floor_line = 500
        self.jumping = False

        self.bending_down = False

        self.rect = pygame.Rect(self.x, self.y, 80, self.fighter_height)

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
        g = 2
        keys = pygame.key.get_pressed()
        # проверка кнопок для каждого игрока
        if self.player_numb == 1:
            if keys[pygame.K_w]:
                self.jumping = True
        elif self.player_numb == 2:
            if keys[pygame.K_i]:
                self.jumping = True
        # прыжок
        if self.jumping:
            if self.rect.y + self.fighter_height - self.jump_v >= self.floor_line:
                self.jumping = False
                self.jump_v = 30
            else:
                self.jump_v -= g
                self.rect.y -= self.jump_v

    def bend_down(self):  # пригнуться
        if self.bending_down:
            self.rect.height = self.fighter_height // 2
            self.rect.y = self.y + self.fighter_height // 2
            self.speed = 5
        else:
            self.rect.height = self.fighter_height
            self.rect.y = self.y
            self.speed = 10

    def attack(self):
        pass
