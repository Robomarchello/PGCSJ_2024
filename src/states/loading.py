import pygame
from pygame.locals import *
from src.engine import State
from src.engine.config import SCREENSIZE, ASSETS_PATH
from src.engine.asset_manager import AssetManager
from src.engine.save_manager import SaveManager


class LoadState(State):
    '''
    This makes sure that display will initialize before using any of the image assets in the game. 
    Needed for usage of pygame.image.convert().
    '''
    def __init__(self, next_state: State):
        super().__init__()
        self.surface = pygame.Surface(SCREENSIZE)

        self.next_state = next_state

    def on_start(self):
        SaveManager.get_save()
        AssetManager.load_assets(ASSETS_PATH)

    def on_exit(self):
        pass

    def update(self, delta):
        self.manager.next_state = self.next_state()