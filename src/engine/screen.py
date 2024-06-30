import pygame
from pygame.locals import *


class Screen:
    FLAGS = []

    draw_surface: pygame.Surface
    window_size: tuple[int, int]

    def __init__(self, screen_size):
        self.window_size = screen_size
        self.window = pygame.display.set_mode(self.window_size, *self.FLAGS)

        self.draw_surface = self.window.copy()

    def update_window(self):
        pass

    def on_resize(self):
        pass


class ResizableScreen(Screen):
    FLAGS = [pygame.RESIZABLE]

    def __init__(self, original_size: tuple[int, int]):
        self.original_size = original_size
        self.fixed_rect = pygame.Rect((0, 0), self.original_size)

        self.fit_rect = None
        self.on_resize(original_size)
        super().__init__(self.original_size)

    def update_window(self):
        #draw draw_surface to the window
        scaled = pygame.transform.scale(
            self.draw_surface, self.fit_rect.size
        )
        self.window.blit(scaled, self.fit_rect.topleft)

    def on_resize(self, new_size):
        window_rect = pygame.Rect((0, 0), new_size)

        self.fit_rect = self.fixed_rect.copy() 
        self.fit_rect = self.fit_rect.fit(window_rect)
        
