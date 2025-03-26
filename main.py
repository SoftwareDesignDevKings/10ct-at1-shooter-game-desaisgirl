from game import Game
from music_manager import MusicManager
import pygame
import cv2


def play_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Display the video frame
        cv2.imshow("Video", frame)

        # Exit the video if the user presses the 'q' key
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((800, 600))  # Replace with your desired screen dimensions

    # Load the background image
    background = pygame.image.load("assets/background.png").convert()
    bg_y = 0  # Initial vertical position of the background
    scroll_speed = 2  # Speed of the background scrolling

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

        # Check if the player has killed 10 enemies
        if game.kill_count >= 5:
            print("10 enemies killed! Pausing game and playing video.")  # Debug
            game.running = False  # Pause the game
            play_video("assets/victory.mp4")  # Replace with your video file path
            game.kill_count = 0  # Reset kill count
            game.running = True  # Resume the game

        # Draw the scrolling background
        screen.blit(background, (0, bg_y))
        screen.blit(background, (0, bg_y - background.get_height()))
        bg_y += scroll_speed
        if bg_y >= background.get_height():
            bg_y = 0

        # Run the game logic
        game.run()

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
