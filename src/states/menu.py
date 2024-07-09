import pygame
from pygame.locals import KEYDOWN, K_r
from src.engine import State, Debug, AssetManager
from src.engine.constants import *


class Menu(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('exit')

    def draw(self):
        self.surface.fill((0, 0, 0))

    def update(self, delta):
        pass

    def handle_event(self, event):
        pass


class NewNextState(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        self.image = AssetManager.images['fff']

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('*exit*')

    def draw(self):
        self.surface.fill((0, 0, 255))

        self.surface.blit(self.image, (0, 0))

        Debug.add_text(self.manager.clock.get_fps())

    def update(self, delta):
        pass

    def handle_event(self, event):
        pass
