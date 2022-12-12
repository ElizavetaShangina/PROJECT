import pygame
from fighters import Fighter

pygame.init()

WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fighting')
clock = pygame.time.Clock()
fps = 60

# Фон
background_image = pygame.image.load('images/backgrounds/forest.jpg')
scaled_background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
screen.blit(scaled_background_image, (0, 0))

# Бойцы
fighter1 = Fighter(1, 200, 350, WIDTH, HEIGHT)
fighter2 = Fighter(2, 920, 350, WIDTH, HEIGHT)


pygame.display.flip()
running = True

while running:
    clock.tick(fps)
    # Очистка экрана
    screen.blit(scaled_background_image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # проверка кнопок
    keys = pygame.key.get_pressed()
    # проверка на две кнопки одновременно
    if not(keys[pygame.K_d] and keys[pygame.K_a]):
        if keys[pygame.K_d]:
            fighter1.move('right')
        elif keys[pygame.K_a]:
            fighter1.move('left')
    fighter1.jump()

    if not(keys[pygame.K_j] and keys[pygame.K_l]):
        if keys[pygame.K_l]:
            fighter2.move('right')
        elif keys[pygame.K_j]:
            fighter2.move('left')
    fighter2.jump()

    fighter1.draw(screen)
    fighter2.draw(screen)

    pygame.display.flip()

pygame.quit()