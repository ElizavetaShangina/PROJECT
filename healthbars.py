import pygame


class HealthBar:
    def __init__(self, player_number, screen_height, screen_width, full_health):
        if player_number == 1:
            self.x_coord = screen_width * 0.1
        else:
            self.x_coord = screen_width * 0.6
        self.y_coord = screen_height * 0.1
        self.width = screen_width * 0.3
        self.height = screen_height * 0.05
        self.health_coef = self.width / full_health
        self.borders = pygame.Rect(self.x_coord - 2, self.y_coord - 2, self.width + 4, self.height + 4)
        self.lost_health = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)

    def change_health(self, health, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.borders)
        pygame.draw.rect(screen, (0, 0, 0), self.lost_health)
        health_left = pygame.Rect(self.x_coord, self.y_coord, health * self.health_coef, self.height)
        pygame.draw.rect(screen, (255, 0, 0), health_left)
