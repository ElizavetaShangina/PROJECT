import pygame


class HealthBar:
    def __init__(self, player_number, screen_height, screen):
        if player_number == 1:
            self.x_coord = 100
        else:
            self.x_coord = 700
        self.y_coord = int(screen_height * 0.1)
        self.width = 400
        self.height = 40
        self.player_numb = player_number

    def change_health(self, health, screen):
        borders = pygame.Rect(self.x_coord - 2, self.y_coord - 2, self.width + 4, self.height + 4)
        pygame.draw.rect(screen, (255, 255, 255), borders)
        lost_health = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)
        pygame.draw.rect(screen, (0, 0, 0), lost_health)
        health_left = pygame.Rect(self.x_coord, self.y_coord, health * 2, self.height)
        pygame.draw.rect(screen, (255, 0, 0), health_left)