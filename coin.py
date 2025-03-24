import app
import random

class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = app.pygame.Surface((7, 7), app.pygame.SRCALPHA)
        self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.x += random.choice([-1, 0, 1])
        self.y += random.choice([-1, 0, 1])
        self.rect.center = (self.x, self.y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)



