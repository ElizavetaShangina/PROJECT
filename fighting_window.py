import pygame
from fighters import Fighter
from healthbars import HealthBar
from animations_data import DIO_data, Sasuke_data, Aizen_data, Rukia_data


def start_fighting(player1_name, player2_name, selected_background, character1, character2):
    pygame.init()
    WIDTH, HEIGHT = 1200, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Fighting')
    clock = pygame.time.Clock()
    fps = 60
    iteration_counter = 0

    # Фон
    background_image = pygame.image.load(f'project_files/{selected_background}.jpg').convert()
    scaled_background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    screen.blit(scaled_background_image, (0, 0))

    all_sprites = pygame.sprite.Group()

    # загрузка спрайт листов
    DIO_sprite_sheet = pygame.image.load('project_files/Dio Brando spritesheet.png')
    Sasuke_sprite_sheet = pygame.image.load('project_files/Sasuke spritesheet.png')
    Aizen_sprite_sheet = pygame.image.load('project_files/Aizen Sousuke spritesheet.png')
    Rukia_sprite_sheet = pygame.image.load('project_files/Kuchiki Rukia spritesheet.png')

    # Бойцы
    if character1 == 'Dio Brando':
        fighter1 = Fighter(player1_name, 1, WIDTH * 0.2, HEIGHT * 0.95, WIDTH, HEIGHT,
                           DIO_sprite_sheet, DIO_data, all_sprites)
    elif character1 == 'Sasuke':
        fighter1 = Fighter(player1_name, 1, WIDTH * 0.2, HEIGHT * 0.95, WIDTH, HEIGHT,
                           Sasuke_sprite_sheet, Sasuke_data, all_sprites)
    elif character1 == 'Aizen Sousuke':
        fighter1 = Fighter(player1_name, 1, WIDTH * 0.2, HEIGHT * 0.95, WIDTH, HEIGHT,
                           Aizen_sprite_sheet, Aizen_data, all_sprites)
    elif character1 == 'Kuchiki Rukia':
        fighter1 = Fighter(player1_name, 1, WIDTH * 0.2, HEIGHT * 0.95, WIDTH, HEIGHT,
                           Rukia_sprite_sheet, Rukia_data, all_sprites)

    if character2 == 'Dio Brando':
        fighter2 = Fighter(player2_name, 2, WIDTH * 0.7, HEIGHT * 0.95, WIDTH, HEIGHT,
                           DIO_sprite_sheet, DIO_data, all_sprites)
    elif character2 == 'Sasuke':
        fighter2 = Fighter(player2_name, 2, WIDTH * 0.7, HEIGHT * 0.95, WIDTH, HEIGHT,
                           Sasuke_sprite_sheet, Sasuke_data, all_sprites)
    elif character2 == 'Aizen Sousuke':
        fighter2 = Fighter(player1_name, 2, WIDTH * 0.7, HEIGHT * 0.95, WIDTH, HEIGHT,
                           Aizen_sprite_sheet, Aizen_data, all_sprites)
    elif character2 == 'Kuchiki Rukia':
        fighter2 = Fighter(player1_name, 2, WIDTH * 0.7, HEIGHT * 0.95, WIDTH, HEIGHT,
                           Rukia_sprite_sheet, Rukia_data, all_sprites)

    # Полоски здоровья
    health_bar1 = HealthBar(1, HEIGHT, WIDTH, fighter1.health)
    health_bar2 = HealthBar(2, HEIGHT, WIDTH, fighter2.health)

    pygame.display.flip()
    running = True
    start_ticks = pygame.time.get_ticks()
    seconds_passed = 0

    while running:
        if not fighter1.attacking and not fighter1.low_attacking:
            attack_type1 = 0
        if not fighter2.attacking and not fighter2.low_attacking:
            attack_type2 = 0
        # Очистка экрана
        screen.blit(scaled_background_image, (0, 0))

        # проверка кнопок
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    fighter1.finish_bending_down_animation = True
                if event.key == pygame.K_k:
                    fighter2.finish_bending_down_animation = True

                # обычные атаки
                if not fighter1.jumping and not fighter1.moving:
                    if not fighter1.bending_down:
                        if keys[pygame.K_1]:
                            attack_type1 = 1
                            fighter1.attacking = True
                        elif keys[pygame.K_2]:
                            attack_type1 = 2
                            fighter1.attacking = True
                        elif keys[pygame.K_3]:
                            attack_type1 = 3
                            fighter1.attacking = True
                    elif fighter1.bending_down:
                        if keys[pygame.K_4]:
                            attack_type1 = 4
                            fighter1.low_attacking = True

                if not fighter2.jumping and not fighter2.moving:
                    if not fighter2.bending_down:
                        if keys[pygame.K_7]:
                            attack_type2 = 1
                            fighter2.attacking = True
                        elif keys[pygame.K_8]:
                            attack_type2 = 2
                            fighter2.attacking = True
                        elif keys[pygame.K_9]:
                            attack_type2 = 3
                            fighter2.attacking = True
                    elif fighter2.bending_down:
                        if keys[pygame.K_0]:
                            attack_type2 = 4
                            fighter2.low_attacking = True

        # смерть
        fighter1.die()
        fighter2.die()

        # атаки
        fighter1.attack(attack_type1, fighter2)
        fighter2.attack(attack_type2, fighter1)

        # движение вправо/влево
        fighter1.move(keys, fighter2)
        fighter2.move(keys, fighter1)

        # пригибание
        fighter1.bend_down(keys)
        fighter2.bend_down(keys)

        # прыжок
        fighter1.jump(keys)
        fighter2.jump(keys)

        # проверка на бездействие
        states1 = [fighter1.moving,
                   fighter1.attacking, fighter1.low_attacking,
                   fighter1.jumping, fighter1.bending_down, fighter1.dead]
        if not any(states1):
            fighter1.start_new_animation(0)

        states2 = [fighter2.moving,
                   fighter2.attacking, fighter2.low_attacking,
                   fighter2.jumping, fighter2.bending_down, fighter2.dead]
        if not any(states2):
            fighter2.start_new_animation(0)

        # обновление позиций
        fighter1.update_rect()
        fighter2.update_rect()

        # отрисовка персонажей
        fighter1.draw(screen)
        fighter2.draw(screen)
        if iteration_counter % 5 == 0:
            all_sprites.update()
        all_sprites.draw(screen)

        # отрисовка полосок здоровья
        health_bar1.change_health(fighter1.health, screen)
        health_bar2.change_health(fighter2.health, screen)

        # отрисовка имён игроков
        fighter1.show_player_name(screen)
        fighter2.show_player_name(screen)

        pygame.display.flip()
        clock.tick(fps)
        iteration_counter += 1

    pygame.quit()
