import pygame


class Fighter(pygame.sprite.Sprite):
    def __init__(self, player_numb, x, y, screen_width, screen_height,
                 animations_data, sheet, scale, group):
        super().__init__(group)

        self.player_numb = player_numb
        if self.player_numb == 1:
            self.color = pygame.Color('red')
            self.direction = 'right'
        else:
            self.color = pygame.Color('blue')
            self.direction = 'left'
        self.bottom_y = y
        self.x = x

        self.full_animations = []
        self.cut_sheet(sheet, animations_data, self.x, self.bottom_y, scale)
        self.cur_frame = 0
        self.image = self.full_animations[0][self.cur_frame]
        self.fighter_height = self.rect.h
        self.fighter_width = self.rect.w
        self.rect.x = self.x
        self.rect.bottom = self.bottom_y

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.floor_line = self.screen_height * 0.95

        self.speed = 7

        self.jump_v = 30
        self.jumping = False

        self.bending_down = False
        self.health = 200

        self.won = False
        self.animation_number = 0

        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, animations_data, x, y, scale):
        y = 0
        for animation_number in range(len(animations_data)):
            frames = []
            width = animations_data[animation_number][1]
            height = animations_data[animation_number][2]
            self.rect = pygame.Rect(x, y, width, height)
            for frame_number in range(animations_data[animation_number][0]):
                frame_location = (width * frame_number, y * animation_number)
                img = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                img = pygame.transform.scale(img, (width * scale, height * scale))
                frames.append(img)
            y += height
            self.full_animations.append(frames)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.full_animations[self.animation_number])
        self.image = self.full_animations[self.animation_number][self.cur_frame]
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.bottom = self.bottom_y
        self.fighter_height = self.rect.h
        if self.cur_frame > 3 and self.bending_down:
            self.cur_frame = 3
        self.fighter_width = self.rect.w

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def move(self, direction):
        self.direction = direction
        if direction == 'right':
            if self.x + self.rect.w + self.speed <= self.screen_width:
                self.x += self.speed
            else:
                self.x += self.screen_width - self.rect.right
        elif direction == 'left':
            if self.x - self.speed >= 0:
                self.x -= self.speed
            else:
                self.x -= self.x

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
            if self.bottom_y - self.jump_v >= self.floor_line:
                self.jumping = False
                self.jump_v = 30
            else:
                self.jump_v -= g
                self.bottom_y -= self.jump_v

    def bend_down(self):  # пригнуться
        if self.bending_down:
            self.rect.top = self.bottom_y - 120
            #self.rect.y = self.bottom_y + self.fighter_height // 2
        else:
            self.rect.top = self.bottom_y - self.fighter_height
            #self.rect.y = self.bottom_y

    def attack(self, screen, attack_type, enemy):

        # определяем типа атаки, её радиус и урон
        if attack_type == 1:
            attack_radius = 50
            damage = 1
        elif attack_type == 2:
            attack_radius = 70
            damage = 2
        elif attack_type == 3:
            attack_radius = 100
            damage = 3
        else:
            attack_radius = 50
            damage = 3

        # меняем направление удара в сторону соперника
        if self.rect.left >= enemy.rect.left:
            self.direction = 'left'
        else:
            self.direction = 'right'

        # определяем, в какую сторону бить
        if self.direction == 'right':
            attack_rect = pygame.Rect(self.rect.right, self.rect.top, attack_radius, self.rect.height)
        else:
            attack_rect = pygame.Rect(self.rect.left - attack_radius, self.rect.top, attack_radius, self.rect.height)

        # проверяем попадание
        if attack_rect.colliderect(enemy.rect):
            enemy.health -= damage

        if enemy.health <= 0:
            self.won = True

        pygame.draw.rect(screen, (0, 255, 0), attack_rect)

    def special_skill(self):
        pass

    def fatality(self):
        pass
