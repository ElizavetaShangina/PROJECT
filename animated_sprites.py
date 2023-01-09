import pygame


pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 10
running = True
all_sprites = pygame.sprite.Group()
background_image = pygame.image.load('data/backgrounds/forest.jpg')
scaled_background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
screen.blit(scaled_background_image, (0, 0))


def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, animation_steps, x, y, sprite_width, sprite_height):
        super().__init__(all_sprites)
        self.full_animations = []
        self.animation_steps = animation_steps
        self.cut_sheet(sheet, sprite_width, sprite_height)
        self.cur_frame = 0
        self.image = self.full_animations[0][self.cur_frame]
        self.rect = self.rect.move(x, y)

        self.fighter_height = self.rect.h
        self.floor_line = 400
        self.jumping = False
        self.jump_v = 15

    def cut_sheet(self, sheet, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        for animation_number in range(len(self.animation_steps)):
            frames = []
            for frame_number in range(self.animation_steps[animation_number]):
                frame_location = (width * frame_number, height * animation_number)
                img = sheet.subsurface(pygame.Rect(frame_location, self.rect.size))
                img = pygame.transform.scale(img, (width * 2, height * 2))
                frames.append(img)
            self.full_animations.append(frames)

    def update(self):
        if not self.jumping:
            self.cur_frame = (self.cur_frame + 1) % len(self.full_animations[0])
            self.image = self.full_animations[0][self.cur_frame]
        if self.jumping:
            if self.cur_frame >= 6 and self.jump_v > 0:
                self.cur_frame = 6
            elif self.cur_frame == 10 and self.jump_v < 0:
                self.cur_frame = 10
            else:
                self.cur_frame = (self.cur_frame + 1) % len(self.full_animations[0])
        self.image = self.full_animations[0][self.cur_frame]

    def jump(self):
        g = 1
        keys = pygame.key.get_pressed()
        # проверка кнопок для каждого игрока
        if keys[pygame.K_w]:
            self.jumping = True
        # прыжок
        if self.jumping:
            if self.rect.y + self.fighter_height - self.jump_v >= self.floor_line:
                self.jumping = False
                self.jump_v = 15
            else:
                self.jump_v -= g
                self.rect.y -= self.jump_v


# загрузка листов спрайтов
DIO_sprite_sheet = load_image('data/characters/DIO/basic_DIO_spritesheet.png')
DIO_animation_steps = [18, 7, 12, 16, 4, 11, 11, 12, 4, 4, 3, 12, 20, 11]
frame_width = 200
frame_height = 170
DIO = AnimatedSprite(DIO_sprite_sheet, DIO_animation_steps, 0, 200, frame_width, frame_height)


while running:
    screen.blit(scaled_background_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        DIO.rect.x += 10
    elif keys[pygame.K_a]:
        DIO.rect.x -= 10
    DIO.jump()
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
    clock.tick(fps)