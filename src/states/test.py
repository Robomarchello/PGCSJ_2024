import pygame
from src.engine import StateMachine, State, Debug, AssetManager, load_spritesheet
from src.engine.constants import *


class MyState(State):
    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

    def on_start(self):
        print('start')
    
    def on_exit(self):
        print('*exit*')

    def draw(self):
        self.surface.fill((255, 255, 255))

        Debug.add_text(self.manager.clock.get_fps())

    def update(self, delta):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.manager.next_state = NewNextState()


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
