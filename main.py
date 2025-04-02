from game import Game
from music_manager import MusicManager
import pygame
import cv2


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((800, 600))  # Replace with your desired screen dimensions


    # Initialize the music manager
    music_manager = MusicManager(
        playlist=[
            "assets/track1.mp3",  # Replace with your file paths
            "assets/track2.mp3",
            "assets/track3.mp3",
        ],
        volume=10
    )
    music_manager.play_music()

    # Start the game
    game = Game()
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.USEREVENT:  # Track finished
                music_manager.play_random_track()
    

        # Run the game logic
        game.run()

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
