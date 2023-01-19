import pygame


class HealthBar:
    def __init__(self, height, width, full_health, x, y):
        self.x_coord = x
        self.y_coord = y
        self.width = width
        self.height = height
        self.health_coef = self.width / full_health
        self.borders = pygame.Rect(self.x_coord - 2, self.y_coord - 2, self.width + 4, self.height + 4)
        self.lost_health = pygame.Rect(self.x_coord, self.y_coord, self.width, self.height)

    def change_health(self, health, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.borders)
        pygame.draw.rect(screen, (0, 0, 0), self.lost_health)
        health_left = pygame.Rect(self.x_coord, self.y_coord, health * self.health_coef, self.height)
        pygame.draw.rect(screen, (255, 0, 0), health_left)
