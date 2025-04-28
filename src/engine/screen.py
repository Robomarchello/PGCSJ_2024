import pygame
from pygame.locals import *
from src.engine.asset_manager import AssetManager


class Screen:
    FLAGS = [RESIZABLE]

    draw_surface: pygame.Surface
    window_size: tuple[int, int]

    def __init__(self, screen_size, title):
        self.original_size = screen_size
        self.window_size = screen_size
        self.draw_surface = pygame.display.set_mode(self.window_size, *self.FLAGS)
        pygame.display.set_caption(title)
        pygame.display.set_icon(AssetManager.images['logo'])