import pygame
import app  # Contains global settings like WIDTH, HEIGHT, PLAYER_SPEED, etc.
import math
import app 
 
from bullet import Bullet
from enemy import Enemy
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
        self.speed = app.PLAYER_SPEED

        self.level = 1
        #dash stuff
        self.dash_cooldown = 0  # Cooldown timer for dashing
        self.is_dashing = False  # Whether the player is currently dashing
        self.dash_duration = 0  # Duration of the dash
        self.dash_speed = 15  # Speed of the dash
        self.direction = [0, 0]  # Direction of the dash
    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.direction = [0, 0]  # Reset direction

        # Check for movement keys
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction[1] = -1  # Move up
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction[1] = 1  # Move down
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction[0] = -1  # Move left
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction[0] = 1  # Move right

        # Normalize the direction vector to prevent faster diagonal movement
        if self.direction != [0, 0]:
            length = (self.direction[0]**2 + self.direction[1]**2)**0.5
            self.direction[0] /= length
            self.direction[1] /= length

        # Move the player based on direction and speed
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed

        # Clamp player position to screen bounds
        self.x = max(0, min(self.x, app.WIDTH))
        self.y = max(0, min(self.y, app.HEIGHT))
        self.rect.center = (self.x, self.y)
        

        # TODO: 3. Clamp player position to screen bounds
        self.x = max(0, min(self.x, app.WIDTH))
        self.y = max(0, min(self.y, app.HEIGHT))
        self.rect.center = (self.x, self.y)

        # animation state
        if self.direction[0] != 0 or self.direction[1] != 0:
            self.state = "run"
        else:
            self.state = "idle"
 
        # direction
        if self.direction[0] < 0:
            self.facing_left = True
        elif self.direction[0] > 0:
            self.facing_left = False
       
    def update(self):
        self.handle_input()
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
        # Handle dashing
        if self.is_dashing:
            self.x += self.dash_speed * self.direction[0]  # Dash in the current direction
            self.y += self.dash_speed * self.direction[1]
            self.dash_duration -= 1
            if self.dash_duration <= 0:
                self.is_dashing = False

        # Handle dash cooldown
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
    def start_dash(self): #dash
        if not self.is_dashing and self.dash_cooldown == 0:
            self.is_dashing = True
            self.dash_duration = 10  # Dash lasts for 10 frames
            self.dash_cooldown = 300  # Cooldown lasts for 5 seconds (300 frames at 60 FPS)
   
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
 
        angle_spread = 10
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
        dx = mx - self.x
        dy = my - self.y
        self.create_bullet(dx, dy)
 
    def shoot_toward_enemy(self, enemy):
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        self.create_bullet(dx, dy)
    

    def add_xp(self, amount):
        self.xp += amount

    def create_bullet(self, dx, dy):
        # Normalize the direction vector
        length = math.sqrt(dx**2 + dy**2)
        if length == 0:
            return
        dx /= length
        dy /= length

        # Apply upgrades to bullet properties
        bullet_speed = self.bullet_speed  # Base speed
        bullet_size = self.bullet_size  # Base size
        bullet_damage = 1  # Example: Add damage if needed
        angle_spread = 10  # Spread angle in degrees
        mid = (self.bullet_count - 1) / 2  # Center of the spread

        # Create multiple bullets if bullet_count > 1
        for i in range(self.bullet_count):
            offset = i - mid
            spread_radians = math.radians(angle_spread * offset)
            spread_dx = math.cos(math.atan2(dy, dx) + spread_radians)
            spread_dy = math.sin(math.atan2(dy, dx) + spread_radians)

            # Create the bullet
            bullet = Bullet(self.x, self.y, spread_dx * bullet_speed, spread_dy * bullet_speed, bullet_size)
            self.bullets.append(bullet)
            print(f"Bullet created at ({self.x}, {self.y}) with velocity ({spread_dx * bullet_speed}, {spread_dy * bullet_speed}) and size {bullet_size}")  # Debug

 
def play_music(self, music_file):
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)  # Loop indefinitely

def stop_music(self):
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
