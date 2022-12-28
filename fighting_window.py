import pygame
from fighters import Fighter
from healthbars import HealthBar


pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fighting')
clock = pygame.time.Clock()
fps = 60

# Фон
background_image = pygame.image.load('data/backgrounds/forest.jpg')
scaled_background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
screen.blit(scaled_background_image, (0, 0))

# Бойцы
fighter1 = Fighter(1, 200, 350, WIDTH, HEIGHT)
fighter2 = Fighter(2, 920, 350, WIDTH, HEIGHT)

# Полоски здоровья
health_bar1 = HealthBar(1, HEIGHT, screen)
health_bar2 = HealthBar(2, HEIGHT, screen)

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
            if event.key == pygame.K_s:
                fighter1.bending_down = True
                fighter1.bend_down()
            elif event.key == pygame.K_k:
                fighter2.bending_down = True
                fighter2.bend_down()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                fighter1.bending_down = False
                fighter1.bend_down()
            elif event.key == pygame.K_k:
                fighter2.bending_down = False
                fighter2.bend_down()

            # обычные атаки
            if not fighter1.jumping and not (keys[pygame.K_d] or keys[pygame.K_a]):
                if keys[pygame.K_1]:
                    fighter1.attack(screen, 1, fighter2)
                elif keys[pygame.K_2]:
                    fighter1.attack(screen, 2, fighter2)
                elif keys[pygame.K_3]:
                    fighter1.attack(screen, 3, fighter2)

            if not fighter2.jumping and not (keys[pygame.K_j] or keys[pygame.K_l]):
                if keys[pygame.K_8]:
                    fighter2.attack(screen, 1, fighter1)
                elif keys[pygame.K_9]:
                    fighter2.attack(screen, 2, fighter1)
                elif keys[pygame.K_0]:
                    fighter2.attack(screen, 3, fighter1)

    # движение вправо/влево
    if not (keys[pygame.K_d] and keys[pygame.K_a]):
        if keys[pygame.K_d]:
            fighter1.move('right')
        elif keys[pygame.K_a]:
            fighter1.move('left')
    if not (keys[pygame.K_j] and keys[pygame.K_l]):
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

    # отрисовка полосок здоровья
    health_bar1.change_health(fighter1.health, screen)
    health_bar2.change_health(fighter2.health, screen)

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()