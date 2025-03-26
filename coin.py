import pygame
import random

class Coin:
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/coin.png").convert_alpha()  # Load the coin image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)



