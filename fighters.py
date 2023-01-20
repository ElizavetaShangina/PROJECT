import pygame

fatality_sound = pygame.mixer.Sound('project_files\\fatality.wav')
finish_him_sound = pygame.mixer.Sound('project_files\\finish_him.wav')
pygame.mixer.music.load('project_files\\fight_font.mp3')


class Fighter(pygame.sprite.Sprite):
    def __init__(self, player_name, player_numb, x, y, background_x, screen_width, screen_height, sheet, data, group):
        super().__init__(group)

        self.player_name = player_name
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
        self.scale = data[5]
        self.cut_sheet(sheet, data[2], data[0], data[1], self.x, self.bottom_y)
        self.cur_frame = 0
        self.image = self.full_animations[0][self.cur_frame]
        self.fighter_height = self.rect.h
        self.fighter_width = self.rect.w
        self.rect.x = self.x
        self.rect.bottom = self.bottom_y

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background_x = background_x
        self.floor_line = self.screen_height * 0.95

        self.speed = data[7]
        self.moving = False

        self.jump_v = 30
        self.jumping = False

        self.bending_down = False
        self.health = 200
        self.finish_me = False

        self.won = False
        self.animation_number = 0

        self.mask = pygame.mask.from_surface(self.image)
        self.cycled_frames = data[3]

        self.finish_bending_down_animation = False

        self.offsets = data[4]
        self.cur_frame_offsets = self.offsets[self.animation_number][self.cur_frame]
        if self.direction == 'right':
            check_collisions_x = self.x + self.cur_frame_offsets[0] * self.scale
            self.x -= self.cur_frame_offsets[0] * self.scale
        else:
            check_collisions_x = self.x + self.cur_frame_offsets[2] * self.scale
            self.x -= self.cur_frame_offsets[2] * self.scale
        check_collisions_y = self.rect.y
        self.bottom_y += self.cur_frame_offsets[1] * self.scale
        check_collisions_h = self.rect.h - self.cur_frame_offsets[1] * self.scale
        check_collisions_w = self.rect.w - self.scale * (self.cur_frame_offsets[0] + self.cur_frame_offsets[2])
        self.check_collisions_rect = pygame.Rect(check_collisions_x, check_collisions_y, check_collisions_w,
                                                 check_collisions_h)

        self.attacking = False
        self.can_damage = True
        self.damage = 0
        self.low_attacking = False
        self.get_up = False
        self.dead = False
        self.cycle_death = False
        self.animation_changed = False

        self.attacks_were_made = [0, 0, 0, 0]
        self.attacks_damage = data[6]

    def cut_sheet(self, sheet, animations_data, width, height, x, y):
        for animation_number in range(len(animations_data)):
            frames = []
            self.rect = pygame.Rect(x, y, width, height)
            for frame_number in range(animations_data[animation_number]):
                frame_location = (width * frame_number, height * animation_number)
                img = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                img = pygame.transform.scale(img, (width * self.scale, height * self.scale))
                frames.append(img)
            self.full_animations.append(frames)
        self.rect.w *= self.scale
        self.rect.h *= self.scale

    def update(self):
        if not self.cycle_death:
            self.cur_frame = (self.cur_frame + 1) % len(self.full_animations[self.animation_number])
            # зацикливание некоторых кадров анимаций
            if self.dead:
                if self.cur_frame == len(self.full_animations[8]) - 1:
                    self.cycle_death = True
            elif self.bending_down:
                if not self.finish_bending_down_animation:
                    if not self.low_attacking:
                        if self.cur_frame == self.cycled_frames[0] + 1:
                            self.cur_frame = self.cycled_frames[0]
                    else:
                        if self.cur_frame == len(self.full_animations[7]) - 1:
                            self.low_attacking = False
                            self.can_damage = True
                            self.start_new_animation(1)
                            self.cur_frame = self.cycled_frames[0]
                            if self.get_up:
                                self.cur_frame = (self.cur_frame + 1) % len(self.full_animations[self.animation_number])
                                self.get_up = False

            elif self.jumping:
                if self.jump_v > 0 and self.cur_frame > self.cycled_frames[1]:
                    self.cur_frame = self.cycled_frames[1]
                if self.jump_v < 0:
                    self.cur_frame = self.cycled_frames[2]

            elif self.attacking:
                if self.cur_frame == len(self.full_animations[self.animation_number]) - 1:
                    self.attacking = False
                    self.can_damage = True
        else:
            self.cur_frame = len(self.full_animations[self.animation_number]) - 1
        try:
            self.image = self.full_animations[self.animation_number][self.cur_frame]
            self.cur_frame_offsets = self.offsets[self.animation_number][self.cur_frame]
        except IndexError:
            self.cur_frame = 0
            self.image = self.full_animations[self.animation_number][self.cur_frame]
            self.cur_frame_offsets = self.offsets[self.animation_number][self.cur_frame]
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.image, True, False)
        self.mask = pygame.mask.from_surface(self.image)

    def update_rect(self):
        self.rect.x = self.x
        self.rect.bottom = self.bottom_y
        self.update_check_collisions_rect()

    def update_check_collisions_rect(self):
        try:
            self.cur_frame_offsets = self.offsets[self.animation_number][self.cur_frame]
        except IndexError:
            self.cur_frame = 0
            self.cur_frame_offsets = self.offsets[self.animation_number][self.cur_frame]
        if self.direction == 'right':
            check_collisions_x = self.x + self.cur_frame_offsets[0] * self.scale
        else:
            check_collisions_x = self.x + self.cur_frame_offsets[2] * self.scale
        check_collisions_y = self.rect.y
        check_collisions_h = self.rect.h - self.cur_frame_offsets[1] * self.scale
        check_collisions_w = self.rect.w - self.scale * (self.cur_frame_offsets[0] + self.cur_frame_offsets[2])
        self.check_collisions_rect = pygame.Rect(check_collisions_x, check_collisions_y, check_collisions_w,
                                                 check_collisions_h)

    def start_new_animation(self, new_animation_number):
        if new_animation_number != self.animation_number and not self.finish_bending_down_animation:
            self.animation_number = new_animation_number
            self.cur_frame = 0
            self.animation_changed = True
        else:
            self.animation_changed = False

    def move(self, keys, enemy):
        if not self.dead:
            # проверка кнопок для каждого игрока
            if self.player_numb == 1:
                if keys[pygame.K_a] and not self.attacking and not self.bending_down:
                    self.moving = True
                    self.direction = 'left'
                elif keys[pygame.K_d] and not self.attacking and not self.bending_down:
                    self.moving = True
                    self.direction = 'right'
                else:
                    self.moving = False
            elif self.player_numb == 2:
                if keys[pygame.K_j] and not self.attacking and not self.bending_down:
                    self.moving = True
                    self.direction = 'left'
                elif keys[pygame.K_l] and not self.attacking and not self.bending_down:
                    self.moving = True
                    self.direction = 'right'
                else:
                    self.moving = False

            # движение и проверка на столкновения
            if self.moving:
                self.start_new_animation(3)
                is_to_the_left = self.check_collisions_rect.right < enemy.check_collisions_rect.left
                is_to_the_right = self.check_collisions_rect.left > enemy.check_collisions_rect.right
                if self.direction == 'right':
                    if is_to_the_left and (self.check_collisions_rect.right + self.speed
                                           < enemy.check_collisions_rect.left):
                        self.x += self.speed
                    elif is_to_the_right and (self.check_collisions_rect.right + self.speed + 10
                                              < self.screen_width - 50):
                        self.x += self.speed

                elif self.direction == 'left':
                    if is_to_the_left and (self.check_collisions_rect.left - self.speed - 10 > self.background_x + 50):
                        self.x -= self.speed
                    elif is_to_the_right and self.check_collisions_rect.left - self.speed >\
                            enemy.check_collisions_rect.right:
                        self.x -= self.speed

    def jump(self, keys):
        if not self.dead:
            g = 2
            # проверка кнопок для каждого игрока
            if self.player_numb == 1:
                if keys[pygame.K_w] and not self.bending_down and not self.attacking and not self.low_attacking:
                    self.jumping = True
            elif self.player_numb == 2:
                if keys[pygame.K_i] and not self.bending_down and not self.attacking and not self.low_attacking:
                    self.jumping = True
            # прыжок
            if self.jumping:
                self.start_new_animation(2)
                if self.check_collisions_rect.bottom - self.jump_v >= self.floor_line:
                    self.jumping = False
                    self.jump_v = 30
                    self.start_new_animation(0)
                else:
                    self.jump_v -= g
                    self.bottom_y -= self.jump_v

    def bend_down(self, keys):  # пригнуться
        if not self.dead:
            # проверка кнопок для каждого игрока
            if self.player_numb == 1:
                if keys[pygame.K_s]:
                    if not self.low_attacking and not self.jumping and not self.attacking:
                        self.bending_down = True
                else:
                    if self.cur_frame == len(self.full_animations[1]) - 1:
                        self.finish_bending_down_animation = False
                        self.bending_down = False
            elif self.player_numb == 2:
                if keys[pygame.K_k]:
                    if not self.low_attacking and not self.jumping and not self.attacking:
                        self.bending_down = True
                else:
                    if self.cur_frame == len(self.full_animations[1]) - 1:
                        self.finish_bending_down_animation = False
                        self.bending_down = False

            # пригибание
            if self.bending_down and not self.low_attacking:
                self.start_new_animation(1)
            elif self.low_attacking and not self.bending_down:
                self.bending_down = True
                self.get_up = True

    def attack(self, attack_type, enemy):
        if not self.dead:
            if self.attacking or self.low_attacking:
                # определяем тип атаки и её урон
                if attack_type == 1 and self.animation_number not in [5, 6, 7]:
                    self.start_new_animation(4)
                elif attack_type == 2 and self.animation_number not in [4, 6, 7]:
                    self.start_new_animation(5)
                elif attack_type == 3 and self.animation_number not in [4, 5, 7]:
                    self.start_new_animation(6)
                elif attack_type == 4 and self.animation_number not in [4, 5, 6]:
                    self.start_new_animation(7)
                self.damage = self.attacks_damage[attack_type - 1]

                # меняем направление удара в сторону соперника
                if self.animation_changed:
                    if self.direction == 'right' and not enemy.attacking:
                        if self.check_collisions_rect.left <= enemy.check_collisions_rect.left:
                            self.direction = 'right'
                        else:
                            self.direction = 'left'
                    elif self.direction == 'left' and not enemy.attacking:
                        if self.check_collisions_rect.right >= enemy.check_collisions_rect.right:
                            self.direction = 'left'
                        else:
                            self.direction = 'right'

                # проверяем попадание
                if pygame.sprite.collide_mask(self, enemy) is not None and self.can_damage:
                    enemy.health -= self.damage
                    enemy.hurt = True
                    self.can_damage = False
                    self.damage = 0
                    self.attacks_were_made[attack_type - 1] += 1

                if enemy.health <= 20 and not self.finish_me:
                    pygame.mixer.Sound.play(finish_him_sound)
                    self.finish_me = True

                if enemy.health <= 0:
                    pygame.mixer.Sound.play(fatality_sound)
                    self.won = True
                    enemy.dead = True

    def die(self):
        if self.dead:
            self.start_new_animation(8)
