import pygame
from fighters import Fighter
from healthbars import HealthBar
from animations_data import DIO_data, Sasuke_data, Aizen_data, Rukia_data
from timer_class import Timer

from ctypes import *

pygame.init()
SCREEN_WIDTH = windll.user32.GetSystemMetrics(0)
SCREEN_HEIGHT = windll.user32.GetSystemMetrics(1) - 50
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


def draw_background(file_name):
    screen.fill((0, 0, 0))
    background_ = pygame.image.load(f'project_files\\{file_name}.jpg').convert()
    background = pygame.transform.scale(background_, (960, 480))
    background_rect = background.get_rect()
    background_width = background_rect[2]
    background_height = background_rect[3]
    background_x1 = (SCREEN_WIDTH - background_width) / 2
    background_y1 = (SCREEN_HEIGHT - background_height) / 2

    screen.blit(background, (background_x1, background_y1, background_x1 + background_width,
                             background_y1 + background_height))
    return background_rect, background_width, background_height, background_x1, background_y1


background_rect, background_width, background_height, background_x1, background_y1 = draw_background('forest')


def draw_intro(seconds, screen):
    font = pygame.font.Font(None, 90)
    if seconds == 0:
        text = font.render('FIGHT!', True, (255, 0, 0))
    else:
        text = font.render(str(seconds), True, (255, 0, 0))

    text_w = text.get_width()
    text_x = background_x1 + background_width // 2 - text_w // 2
    text_y = background_y1 + 100
    screen.blit(text, (text_x, text_y))


def draw_player_name(name, number):
    font = pygame.font.Font(None, 40)
    text = font.render(name, True, (255, 255, 255))
    if number == 1:
        text_x = background_x1 + 60
    else:
        text_x = background_x1 + background_width - 328
    text_y = background_y1 + 20
    screen.blit(text, (text_x, text_y))


def start_fighting(player1_name, player2_name, selected_background, character1, character2):
    pygame.mixer.music.play(-1)
    background_rect, background_width, background_height, background_x1, background_y1 = draw_background(
        selected_background)
    fps = 60
    WIDTH, HEIGHT = background_x1 + background_width, background_height + background_y1
    pygame.display.set_caption('Fighting')
    clock = pygame.time.Clock()
    iteration_counter = 0

    all_sprites = pygame.sprite.Group()

    # загрузка спрайт листов
    DIO_sprite_sheet = pygame.image.load('project_files/Dio Brando spritesheet.png')
    Sasuke_sprite_sheet = pygame.image.load('project_files/Sasuke spritesheet.png')
    Aizen_sprite_sheet = pygame.image.load('project_files/Aizen Sousuke spritesheet.png')
    Rukia_sprite_sheet = pygame.image.load('project_files/Kuchiki Rukia spritesheet.png')

    start_x1, start_y1 = background_x1 + background_width * 0.2, HEIGHT * 0.95
    start_x2, start_y2 = background_x1 + background_width * 0.7, HEIGHT * 0.95


    # Бойцы
    if character1 == 'Dio Brando':
        fighter1 = Fighter(player1_name, 1, start_x1, start_y1, WIDTH, HEIGHT,
                           DIO_sprite_sheet, DIO_data, all_sprites)
    elif character1 == 'Sasuke':
        fighter1 = Fighter(player1_name, 1, start_x1, start_y1, WIDTH, HEIGHT,
                           Sasuke_sprite_sheet, Sasuke_data, all_sprites)
    elif character1 == 'Aizen Sousuke':
        fighter1 = Fighter(player1_name, 1, start_x1, start_y1, WIDTH, HEIGHT,
                           Aizen_sprite_sheet, Aizen_data, all_sprites)
    elif character1 == 'Kuchiki Rukia':
        fighter1 = Fighter(player1_name, 1, start_x1, start_y1, WIDTH, HEIGHT,
                           Rukia_sprite_sheet, Rukia_data, all_sprites)

    if character2 == 'Dio Brando':
        fighter2 = Fighter(player2_name, 2, start_x2, start_y2, WIDTH, HEIGHT,
                           DIO_sprite_sheet, DIO_data, all_sprites)
    elif character2 == 'Sasuke':
        fighter2 = Fighter(player2_name, 2, start_x2, start_y2, WIDTH, HEIGHT,
                           Sasuke_sprite_sheet, Sasuke_data, all_sprites)
    elif character2 == 'Aizen Sousuke':
        fighter2 = Fighter(player1_name, 2, start_x2, start_y2, WIDTH, HEIGHT,
                           Aizen_sprite_sheet, Aizen_data, all_sprites)
    elif character2 == 'Kuchiki Rukia':
        fighter2 = Fighter(player1_name, 2, start_x2, start_y2, WIDTH, HEIGHT,
                           Rukia_sprite_sheet, Rukia_data, all_sprites)

    # Полоски здоровья
    health_bar1 = HealthBar(background_height * 0.05, background_width * 0.3, fighter1.health, background_x1 + 50, background_y1 + 50)
    health_bar2 = HealthBar(background_height * 0.05, background_width * 0.3, fighter2.health, background_x1 + background_width - 338, background_y1 + 50)
    timer = Timer(SCREEN_WIDTH // 2, SCREEN_HEIGHT + background_y1 + 30)

    pygame.display.flip()
    running = True

    get_time_before_quit = True
    seconds_before_quit = -1
    winners_name, winners_character, winners_time, weak_at, medium_at, heavy_at, low_at = 0, 0, 0, 0, 0, 0, 0
    start_time = pygame.time.get_ticks()
    game_started = False
    seconds_before_start = 3

    while running:
        if not fighter1.attacking and not fighter1.low_attacking:
            attack_type1 = 0
        if not fighter2.attacking and not fighter2.low_attacking:
            attack_type2 = 0

        # Очистка экрана
        draw_background(selected_background)

        if pygame.time.get_ticks() - start_time >= 1000:
            seconds_before_start -= 1
            start_time = pygame.time.get_ticks()

        if seconds_before_start <= -1:
            game_started = True
        else:
            draw_intro(seconds_before_start, screen)

        if game_started:
            timer.update()

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
        if iteration_counter % 5 == 0:
            all_sprites.update()
        all_sprites.draw(screen)

        # отрисовка полосок здоровья
        health_bar1.change_health(fighter1.health, screen)
        health_bar2.change_health(fighter2.health, screen)

        # отрисовка имён игроков
        draw_player_name(player1_name, 1)
        draw_player_name(player2_name, 2)

        pygame.display.flip()
        clock.tick(fps)
        iteration_counter += 1

        if fighter1.won or fighter2.won:
            timer.stop_counting = True
            if get_time_before_quit:
                seconds_before_quit = timer.seconds + 3
                get_time_before_quit = False
            if fighter1.won:
                winners_name = player1_name
                winners_character = character1
                winners_time = timer.text
                weak_at = fighter1.attacks_were_made[0]
                medium_at = fighter1.attacks_were_made[1]
                heavy_at = fighter1.attacks_were_made[2]
                low_at = fighter1.attacks_were_made[3]
            else:
                winners_name = player2_name
                winners_character = character2
                winners_time = timer.text
                weak_at = fighter2.attacks_were_made[0]
                medium_at = fighter2.attacks_were_made[1]
                heavy_at = fighter2.attacks_were_made[2]
                low_at = fighter2.attacks_were_made[3]

        if timer.seconds == seconds_before_quit:
            running = False

    pygame.mixer.music.stop()
    return winners_name, winners_character, winners_time, heavy_at, medium_at, weak_at, low_at
