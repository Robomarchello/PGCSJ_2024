import os
import pygame
from src.engine import State, AssetManager
from src.engine.constants import *


class LoadingScreen(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        self.load_count = self.files_in_dir(
            [
                'D:/Python/2024/pygame/engine/src/assets/images'
            ])
        self.progress = 0

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('*exit*')

    def draw(self):
        self.surface.fill((0, 0, 255))

    def update(self, delta):
        pass

    def handle_event(self, event):
        pass

    def files_in_dir(self, directories):
        count = 0

        for directory in directories:
            for name in os.listdir(directory):
                if os.path.isfile(name):
                    count += 1

        return count