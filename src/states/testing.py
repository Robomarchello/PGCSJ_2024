import pygame
from pygame.locals import *
from src.engine.state_machine import State
from src.engine import Debug
from src.engine.asset_manager import AssetManager
from src.engine.message_system import MessageHandler


class Testing(State):
    def __init__(self):
        super().__init__()

        MessageHandler.init_font()
        MessageHandler.post('bebra', duration=3)

    def draw(self, surface):
        surface.fill((0, 0, 0))

        MessageHandler.draw(surface)

    def update(self, delta):
        MessageHandler.update(delta)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            # MessageHandler.post('Decoding hint... Needs {Y} more tries.', duration=3)
            MessageHandler.post('СЛАВА ТРУДУ!', duration=3)

        # MessageHandler.handle_event(event)

    def on_start(self):
        pass
    
    def on_exit(self):
        pass