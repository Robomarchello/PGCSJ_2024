import pygame
from pygame.locals import *
from src.engine import State, Debug
from src.engine.asset_manager import AssetManager
from src.engine.config import SCREENSIZE, SCREEN_W, SCREEN_H
from src.engine.gui.nine_slice import NineSlice


class Testing(State):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 0, 0)

        self.nine_slice = NineSlice(AssetManager.images['button_slice'].convert_alpha())

    def on_start(self):
        pass
    
    def on_exit(self):
        pass

    def draw(self, surface):
        surface.fill((255, 255, 255))

        self.rect.center = (SCREEN_W / 2, SCREEN_H / 2)
        mp = pygame.mouse.get_pos()
        self.rect.width = abs(SCREEN_W / 2- mp[0]) * 2
        self.rect.height = abs(SCREEN_H / 2 - mp[1]) * 2

        surf = self.nine_slice.as_surface(self.rect)
        surface.blit(surf, (0, 0))
        
    def update(self, delta):
        pass

    def handle_event(self, event):
        pass