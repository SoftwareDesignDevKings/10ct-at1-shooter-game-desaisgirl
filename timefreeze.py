import pygame

class TimeFreeze:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/time_freeze.png")  # Add a cool image for the Time Freeze
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)