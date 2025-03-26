# game.py
import pygame
import random
import os
 
import app
from player import Player
from enemy import Enemy
from coin import Coin
import math
 
class Game:
    def __init__(self):
        pygame.init()  # Initialize Pygame
        self.screen = pygame.display.set_mode((app.WIDTH, app.HEIGHT))
        pygame.display.set_caption("Shooter")
        self.clock = pygame.time.Clock()
 
        self.assets = app.load_assets()
       
        # Load sound effects
        self.shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
        self.coin_sound = pygame.mixer.Sound("assets/coin.wav")
        self.game_over_sound = pygame.mixer.Sound("assets/game_over.wav")
        
        font_path = os.path.join("assets", "PressStart2P.ttf")
        self.font_small = pygame.font.Font(font_path, 18)
        self.font_large = pygame.font.Font(font_path, 32)
 
        self.background = self.create_random_background(
            app.WIDTH, app.HEIGHT, self.assets["floor_tiles"]
        )
       
        self.running = True
        self.game_over = False
        self.bullet_colour = (255, 255, 255)  # Default bullet color (white)
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = 60
        self.enemies_per_spawn = 1

        self.coins = []
 
        self.reset_game()
       
        self.in_level_up_menu = False
        self.upgrade_options = []
        
        #for shake screen
        self.shake_duration = 0  # How long the screen shake lasts
        self.shake_intensity = 0  # How strong the shake is
        #swoooshhh
        self.swoosh_sound = pygame.mixer.Sound("assets/swoosh.wav")  # Load swoosh sound

        self.kill_count = 0  # Track the number of enemies killed
 
    def reset_game(self):
        self.player = Player(app.WIDTH // 2, app.HEIGHT // 2, self.assets)
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemies_per_spawn = 1

        self.coins = []
        self.game_over = False
        #added shit
       
 
    def create_random_background(self, width, height, floor_tiles):
        bg = pygame.Surface((width, height))
        tile_w = floor_tiles[0].get_width()
        tile_h = floor_tiles[0].get_height()
 
        for y in range(0, height, tile_h):
            for x in range(0, width, tile_w):
                tile = random.choice(floor_tiles)
                bg.blit(tile, (x, y))
 
        return bg
   
    def run(self):
        while self.running:
            self.clock.tick(app.FPS)
            self.handle_events()
 
            if not self.game_over and not self.in_level_up_menu:
                self.update()
           
            self.draw()
 
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            # Handle quitting the game
            if event.type == pygame.QUIT:
                self.running = False

            # Handle key presses
            elif event.type == pygame.KEYDOWN:
                # Game Over state
                if self.game_over:
                    if event.key == pygame.K_r:  # Restart the game
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:  # Quit the game
                        self.running = False

                # Level-up menu
                elif self.in_level_up_menu:
                    if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:  # Handle upgrade selection
                        index = event.key - pygame.K_1  # Map K_1, K_2, K_3 to indices 0, 1, 2
                        if 0 <= index < len(self.upgrade_options):
                            upgrade = self.upgrade_options[index]
                            print(f"Applying upgrade: {upgrade}")  # Debug
                            self.apply_upgrade(self.player, upgrade)
                            self.in_level_up_menu = False  # Exit level-up menu

                # Normal gameplay
                elif not self.game_over:
                    if event.key == pygame.K_q and self.player.dash_cooldown == 0:  # Dash with Q
                        self.player.start_dash()
                        self.swoosh_sound.play()  # Play swoosh sound
                    elif event.key == pygame.K_SPACE:  # Shoot with SPACE
                        print("Spacebar pressed!")  # Debug
                        nearest_enemy = self.find_nearest_enemy()
                        if nearest_enemy:
                            print("Nearest enemy found!")  # Debug
                            self.player.shoot_toward_enemy(nearest_enemy)
                            self.shoot_sound.play()  # Play shooting sound

            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    print("Left mouse button clicked!")  # Debug
                    self.player.shoot_toward_mouse(event.pos)
    def update(self):
        self.player.handle_input()
        self.player.update()
 
        for enemy in self.enemies:
            enemy.update(self.player)
 
        self.check_player_enemy_collisions()
        self.check_bullet_enemy_collisions()
        self.check_player_coin_collisions()
 
        if self.player.health <= 0:
            if not self.game_over:  # Ensure the sound plays only once
                self.game_over_sound.play()
            self.game_over = True
            return
        self.spawn_enemies()
        self.check_for_level_up()
 
    def draw(self):
            # Apply screen shake offset
        shake_x = shake_y = 0
        if self.shake_duration > 0:
            shake_x = random.randint(-self.shake_intensity, self.shake_intensity)
            shake_y = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_duration -= 1  # Decrease shake duration

        # Draw everything with the shake offset
        self.screen.blit(self.background, (shake_x, shake_y))

        for coin in self.coins:
            coin.draw(self.screen)

        if not self.game_over:
            self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        hp = max(0, min(self.player.health, 5))
        health_img = self.assets["health"][hp]
        self.screen.blit(health_img, (10, 10))

        xp_text_surf = self.font_small.render(f"XP: {self.player.xp}", True, (255, 255, 255))
        self.screen.blit(xp_text_surf, (10, 70))

        next_level_xp = self.player.level * self.player.level * 5
        xp_to_next = max(0, next_level_xp - self.player.xp)
        xp_next_surf = self.font_small.render(f"Next Lvl XP: {xp_to_next}", True, (255, 255, 255))
        self.screen.blit(xp_next_surf, (10, 100))

        if self.game_over:
            self.draw_game_over_screen()

        if self.in_level_up_menu:
            self.draw_upgrade_menu()

        # Display dash cooldown
        if self.player.dash_cooldown > 0:
            cooldown_text = f"Dash Cooldown: {self.player.dash_cooldown // app.FPS}s"
        else:
            cooldown_text = "Dash Ready!"
        cooldown_surf = self.font_small.render(cooldown_text, True, (255, 255, 255))
        self.screen.blit(cooldown_surf, (10, 160))
        pygame.display.flip()
 
    def spawn_enemies(self):
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_interval:
            self.enemy_spawn_timer = 0
 
            for _ in range(self.enemies_per_spawn):
                side = random.choice(["top", "bottom", "left", "right"])
                if side == "top":
                    x = random.randint(0, app.WIDTH)
                    y = -app.SPAWN_MARGIN
                elif side == "bottom":
                    x = random.randint(0, app.WIDTH)
                    y = app.HEIGHT + app.SPAWN_MARGIN
                elif side == "left":
                    x = -app.SPAWN_MARGIN
                    y = random.randint(0, app.HEIGHT)
                else:
                    x = app.WIDTH + app.SPAWN_MARGIN
                    y = random.randint(0, app.HEIGHT)
 
                enemy_type = random.choice(list(self.assets["enemies"].keys()))
                enemy = Enemy(x, y, enemy_type, self.assets["enemies"])
                self.enemies.append(enemy)
 
    def check_player_enemy_collisions(self):
        collided = False
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect):
                collided = True
                break
 
        if collided:
            self.player.take_damage(1)
            px, py = self.player.x, self.player.y
            for enemy in self.enemies:
                enemy.set_knockback(px, py, app.PUSHBACK_DISTANCE)
            
             # Trigger screen shake
            self.shake_duration = 15  # Shake for 10 frames
            self.shake_intensity = 10  # Shake intensity
    
    def draw_game_over_screen(self):
        #Dark Overlay
        overlay = pygame.Surface((app.WIDTH, app.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
 
        #Game Over Text
        game_over_surf = self.font_large.render("Game Over. Try Again?", True, (255, 0, 0))
        game_over_rect = game_over_surf.get_rect(center=(app.WIDTH // 2, app.HEIGHT // 2 - 50))
        self.screen.blit(game_over_surf, game_over_rect)
 
        #Prompt to restart or quit
        prompt_surf = self.font_small.render("Press R to Play Again  or ESC to Quit", True, (255, 255, 255))
        prompt_rect = prompt_surf.get_rect(center=(app.WIDTH // 2, app.HEIGHT // 2 + 20))
        self.screen.blit(prompt_surf, prompt_rect)
 
    def find_nearest_enemy(self):
        if not self.enemies:
            print("No enemies found!")  # Debug
            return None
        nearest = None
        min_dist = float('inf')
        px, py = self.player.x, self.player.y
        for enemy in self.enemies:
            dist = math.sqrt((enemy.x - px)**2 + (enemy.y - py)**2)
            if dist < min_dist:
                min_dist = dist
                nearest = enemy
        print(f"Nearest enemy found at ({nearest.x}, {nearest.y})")  # Debug
        return nearest
   
    def check_bullet_enemy_collisions(self):
        bullets_to_remove = []  # Temporary list to track bullets to remove
        for bullet in self.player.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    if bullet not in bullets_to_remove:  # Avoid duplicate removals
                        bullets_to_remove.append(bullet)
                    # Create a new coin at a random position
                    new_coin = Coin(random.randint(0, app.WIDTH - 32), random.randint(0, app.HEIGHT - 32))
                    self.coins.append(new_coin)
                    self.enemies.remove(enemy)
                    self.kill_count += 1  # Increment kill count
                    print(f"Enemies killed: {self.kill_count}")  # Debug

        # Remove bullets after the loop
        for bullet in bullets_to_remove:
            if bullet in self.player.bullets:  # Ensure the bullet is still in the list
                self.player.bullets.remove(bullet)
                
    def start_stopwatch(self):
        self.start_time = pygame.time.get_ticks()

    def get_elapsed_time(self):
        elapsed_time_ms = pygame.time.get_ticks() - self.start_time
        elapsed_seconds = elapsed_time_ms // 1000
        return elapsed_seconds

    def draw_stopwatch(self):
        elapsed_time = self.get_elapsed_time()
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_text = f"Time: {minutes:02}:{seconds:02}"
        time_surf = self.font_small.render(time_text, True, (255, 255, 255))
        self.screen.blit(time_surf, (10, 130))
    def check_player_coin_collisions(self):
        coins_collected = []
        for coin in self.coins:
            if coin.rect.colliderect(self.player.rect):
                coins_collected.append(coin)
                self.coin_sound.play() # Play coin sound
                # Calculate XP ltiplier based on the number of coins collected
                coin_count = len(coins_collected)
                if coin_count >= 100:
                    xp_multiplier = 10
                else:
                    xp_multiplier = (coin_count // 10) + 1
                self.player.add_xp(xp_multiplier)

        for c in coins_collected:
            if c in self.coins:
                self.coins.remove(c)
                
                
    def pick_random_upgrades(self, num):
        possible_upgrades = [
            {"name": "Bigger Bullet",  "desc": "Bullet size +5"},
            {"name": "Faster Bullet",  "desc": "Bullet speed +2"},
            {"name": "Extra Bullet",   "desc": "Fire additional bullet"},
            {"name": "Shorter Cooldown", "desc": "Shoot more frequently"},
            {"name": "Player Faster", "desc": "+ 0.5 speed"}
    ]
        return random.sample(possible_upgrades, k=num)
    
    def apply_upgrade(self, player, upgrade):
        name = upgrade["name"]
        if name == "Bigger Bullet":
            player.bullet_size += 10
        elif name == "Faster Bullet":
            player.bullet_speed += 5
        elif name == "Extra Bullet":
            player.bullet_count += 1
        elif name == "Player Faster":
            player.speed += 0.5
        elif name == "Shorter Cooldown":
            player.shoot_cooldown = max(1, int(player.shoot_cooldown * 0.8))
            
    def draw_upgrade_menu(self):
        # Dark overlay behind the menu
        overlay = pygame.Surface((app.WIDTH, app.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        # Title
        title_surf = self.font_large.render("Choose an Upgrade!", True, (255, 255, 0))
        title_rect = title_surf.get_rect(center=(app.WIDTH // 2, app.HEIGHT // 3 - 50))
        self.screen.blit(title_surf, title_rect)

        # Options
        for i, upgrade in enumerate(self.upgrade_options):
            text_str = f"{i+1}. {upgrade['name']} - {upgrade['desc']}"
            option_surf = self.font_small.render(text_str, True, (255, 255, 255))
            line_y = app.HEIGHT // 3 + i * 40
            option_rect = option_surf.get_rect(center=(app.WIDTH // 2, line_y))
            self.screen.blit(option_surf, option_rect)
            
    def check_for_level_up(self):
        xp_needed = self.player.level * self.player.level * 5
        if self.player.xp >= xp_needed:
            # Leveled up
            self.player.level += 1
            self.in_level_up_menu = True
            self.upgrade_options = self.pick_random_upgrades(3)

            # Increase enemy spawns each time we level up
            self.enemies_per_spawn += 1


