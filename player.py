import pygame
import app  # Contains global settings like WIDTH, HEIGHT, PLAYER_SPEED, etc.
import math
 
from bullet import Bullet
 
class Player:
    def __init__(self, x, y, assets):
        self.x = x
        self.y = y
 
        self.speed = app.PLAYER_SPEED
        self.animations = assets["player"]
        self.state = "idle"
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 8
 
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.facing_left = False
       
        self.health = 5
        self.xp = 0
 
        self.bullet_speed = 10
        self.bullet_size = 10
        self.bullet_count = 1
        self.shoot_cooldown = 70
        self.shoot_timer = 40
        self.bullets = []

        self.level = 1
    def handle_input(self):
        # TODO: 1. Capture Keyboard Input
        keys = pygame.key.get_pressed()
 
        vel_x, vel_y = 0, 0
 
        # TODO: 2. Adjust player position with keys pressed, updating the player position to vel_x and vel_y
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            # Move character Left
            vel_x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            vel_x += self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vel_y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            vel_y += self.speed
 
        self.x += vel_x
        self.y += vel_y

        # TODO: 3. Clamp player position to screen bounds
        self.x = max(0, min(self.x, app.WIDTH))
        self.y = max(0, min(self.y, app.HEIGHT))
        self.rect.center = (self.x, self.y)

        # animation state
        if vel_x != 0 or vel_y != 0:
            self.state = "run"
        else:
            self.state = "idle"
 
        # direction
        if vel_x < 0:
            self.facing_left = True
        elif vel_x > 0:
            self.facing_left = False
       
    def update(self):
        for bullet in self.bullets:
            bullet.update()
 
            if bullet.y < 0 or bullet.y > app.HEIGHT or bullet.x < 0 or bullet.x > app.WIDTH:
                self.bullets.remove(bullet)

        self.animation_timer += 2
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            frames = self.animations[self.state]
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
            center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = center
 
    def draw(self, surface):
        if self.facing_left:
            flipped_img = pygame.transform.flip(self.image, True, False)
            surface.blit(flipped_img, self.rect)
        else:
            surface.blit(self.image, self.rect)
 
        for bullet in self.bullets:
            bullet.draw(surface)
 
    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
       
    def shoot_toward_position(self, tx, ty):
        if self.shoot_timer >= self.shoot_cooldown:
            return
       
        dx = tx - self.x
        dy = ty - self.y
        dist = math.sqrt(dx**2 + dy**2)
        if dist == 0:
            return
       
        vx = (dx / dist) * self.bullet_speed
        vy = (dy / dist) * self.bullet_speed
 
        angle_spread = 5
        base_angle = math.atan2(vy, vx)
        mid = (self.bullet_count - 1) / 2
 
        for i in range(self.bullet_count):
            offset = i - mid
            spread_radians = math.radians(angle_spread * offset)
            angle = base_angle + spread_radians
 
            final_vx = math.cos(angle) * self.bullet_speed
            final_vy = math.sin(angle) * self.bullet_speed
 
            bullet = Bullet(self.x, self.y, final_vx, final_vy, self.bullet_size)
            self.bullets.append(bullet)
        self.shoot_timer = 0
 
    def shoot_toward_mouse(self, pos):
        mx, my = pos
        self.shoot_toward_position(mx, my)
 
    def shoot_toward_enemy(self, enemy):
        self.shoot_toward_position(enemy.x, enemy.y)

    def add_xp(self, amount):
        self.xp += amount

 
def play_music(self, music_file):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # Loop indefinitely

def stop_music(self):
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()