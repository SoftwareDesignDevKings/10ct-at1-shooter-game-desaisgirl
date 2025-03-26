import pygame
import random

class MusicManager:
    def __init__(self, playlist=None, volume=0.5):
        pygame.mixer.init()
        self.playlist = playlist or []  # List of music tracks
        self.current_track = None  # No track is playing initially
        self.volume = volume

    def play_music(self):
        if not self.playlist:
            return

        # Randomize the starting track
        self.current_track = random.randint(0, len(self.playlist) - 1)

        # Load and play the randomized track
        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()

        # Set up an event to detect when the track ends
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def play_next_track(self):
        if not self.playlist:
            return

        # Move to the next track in the playlist
        self.current_track = (self.current_track + 1) % len(self.playlist)

        # Load and play the next track
        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()