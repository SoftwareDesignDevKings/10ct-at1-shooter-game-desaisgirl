import pygame
import app
import math

class Enemy:
    def __init__(self, x, y, enemy_type, enemy_assets, speed=app.DEFAULT_ENEMY_SPEED):
        self.x = x
        self.y = y
        self.speed = speed

        self.frames = enemy_assets[enemy_type]
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.enemy_type = enemy_type
        self.facing_left = False

        # TODO: Define knockback properties

    def update(self, player):
        self.move_toward_player(player)
        self.animate()

    def move_toward_player(self, player):
        # Calculates direction vector toward player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = (dx**2 + dy**2) ** 0.5

        if dist != 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

        self.facing_left = dx < 0

        # Updates enemy position
        self.rect.center = (self.x, self.y)

    def apply_knockback(self):
        step = min(app.ENEMY_KNOCKBACK_SPEED, self.knockback_dist_remaining)
        self.knockback_dist_remaining -= step

        # TODO: Apply knockback effect to enemy position
        # Hint: apply the dx, dy attributes

        # TODO: Update facing direction based on knockback direction
        pass

    def animate(self):
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            center = self.rect.center
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = center

    def draw(self, surface):
        if self.facing_left:
            flipped_image = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_image, self.rect)
        else:
            surface.blit(self.image, self.rect)

    def set_knockback(self, px, py, dist):
        dx = self.x - px
        dy = self.y - py
        length = math.sqrt(dx**2 + dy**2)
        if length != 0:
            self.knockback_dx = dx / length
            self.knockback_dy = dy / length
            self.knockback_dist_remaining = dist