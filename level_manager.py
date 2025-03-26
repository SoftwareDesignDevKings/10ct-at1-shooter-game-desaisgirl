import pygame

class LevelManager:
    def __init__(self, screen):
        self.screen = screen
        self.level = 1  # Start at level 1
        self.bg_y = 0  # Initial vertical position of the background
        self.scroll_speed = 2  # Speed of the background scrolling
        self.enemies_to_kill = 5  # Enemies required to advance to the next level
        self.backgrounds = {
            1: "assets/background.png",  # Background for level 1
            2: "assets/background_level2.png",  # Background for level 2
            3: "assets/background_level3.png"  # Background for level 3
        }
        self.background = pygame.image.load(self.backgrounds[self.level]).convert()

    def draw_scrolling_background(self):
        # Draw the background twice to create a scrolling effect
        self.screen.blit(self.background, (0, self.bg_y))
        self.screen.blit(self.background, (0, self.bg_y - self.background.get_height()))

        # Update the vertical position of the background
        self.bg_y += self.scroll_speed
        if self.bg_y >= self.background.get_height():
            self.bg_y = 0

    def check_level_up(self, kill_count):
        if kill_count >= self.enemies_to_kill:
            self.level += 1  # Advance to the next level
            self.enemies_to_kill += 5  # Increase the number of enemies required for the next level
            self.scroll_speed += 1  # Increase scroll speed for difficulty
            print(f"Level Up! Now on Level {self.level}")  # Debug

            # Change the background for the new level
            if self.level in self.backgrounds:
                self.background = pygame.image.load(self.backgrounds[self.level]).convert()