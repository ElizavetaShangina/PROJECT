import pygame
from fighters import Fighter
from healthbars import HealthBar


# конец раунда
def round_over(winner):
    print(f'Player {winner} is a winner!')


pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fighting')
clock = pygame.time.Clock()
fps = 60

# Фон
background_image = pygame.image.load('project_files/backgrounds/ruined_house_in_the_forest.jpg').convert()
scaled_background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
screen.blit(scaled_background_image, (0, 0))

# загрузка листов спрайтов
DIO_sprite_sheet = pygame.image.load('project_files/characters/DIO/1x2.png').convert_alpha()
#DIO_animation_steps = [18, 7, 12, 16, 4, 11, 11, 12, 4, 11]
DIO_animations_data = [[18, 69, 124], [7, 89, 120]]
DIO_scale = 2

all_sprites = pygame.sprite.Group()

# Бойцы
fighter1 = Fighter(1, WIDTH * 0.2, HEIGHT * 0.95, WIDTH, HEIGHT,
                   DIO_animations_data, DIO_sprite_sheet,
                   DIO_scale, all_sprites)
fighter2 = Fighter(2, WIDTH * 0.7, HEIGHT * 0.95, WIDTH, HEIGHT,
                   DIO_animations_data, DIO_sprite_sheet,
                   DIO_scale, all_sprites)

# Полоски здоровья
health_bar1 = HealthBar(1, HEIGHT, WIDTH, fighter1.health)
health_bar2 = HealthBar(2, HEIGHT, WIDTH, fighter2.health)

pygame.display.flip()
running = True

while running:
    # Очистка экрана
    screen.blit(scaled_background_image, (0, 0))

    # проверка кнопок
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # проверка на нажатие/отжатие клавиш пригибания
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and not fighter1.jumping:
                fighter1.bending_down = True
                fighter1.animation_number = 1
                fighter1.bend_down()
            elif event.key == pygame.K_k and not fighter2.jumping:
                fighter2.bending_down = True
                fighter2.bend_down()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                fighter1.bending_down = False
                fighter1.animation_number = 0
                fighter1.bend_down()
            elif event.key == pygame.K_k:
                fighter2.bending_down = False
                fighter2.bend_down()

            # обычные атаки
            if not fighter1.jumping and not (keys[pygame.K_d] or keys[pygame.K_a]):
                if not fighter1.bending_down:
                    if keys[pygame.K_1]:
                        fighter1.attack(screen, 1, fighter2)
                    elif keys[pygame.K_2]:
                        fighter1.attack(screen, 2, fighter2)
                    elif keys[pygame.K_3]:
                        fighter1.attack(screen, 3, fighter2)
                else:
                    if keys[pygame.K_4]:
                        fighter1.attack(screen, 4, fighter2)

            if not fighter2.jumping and not (keys[pygame.K_j] or keys[pygame.K_l]):
                if not fighter2.bending_down:
                    if keys[pygame.K_8]:
                        fighter2.attack(screen, 1, fighter1)
                    elif keys[pygame.K_9]:
                        fighter2.attack(screen, 2, fighter1)
                    elif keys[pygame.K_0]:
                        fighter2.attack(screen, 3, fighter1)
                else:
                    if keys[pygame.K_4]:
                        fighter2.attack(screen, 4, fighter1)

    # движение вправо/влево
    if not (keys[pygame.K_d] and keys[pygame.K_a]) and not fighter1.bending_down:
        if keys[pygame.K_d]:
            fighter1.move('right')
        elif keys[pygame.K_a]:
            fighter1.move('left')
    if not (keys[pygame.K_j] and keys[pygame.K_l]) and not fighter2.bending_down:
        if keys[pygame.K_l]:
            fighter2.move('right')
        elif keys[pygame.K_j]:
            fighter2.move('left')

    # прыжок
    fighter1.jump()
    fighter2.jump()

    # отрисовка персонажей
    fighter1.draw(screen)
    fighter2.draw(screen)
    all_sprites.update()
    all_sprites.draw(screen)

    # отрисовка полосок здоровья
    health_bar1.change_health(fighter1.health, screen)
    health_bar2.change_health(fighter2.health, screen)

    # проверка на конец раунда
    if fighter1.won or fighter2.won:
        if fighter1.won:
            round_over(1)
        else:
            round_over(2)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()