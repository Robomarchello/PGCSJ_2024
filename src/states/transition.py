import pygame
from pygame.locals import BLEND_SUB
from src.engine.constants import SCREENSIZE


class TransitionFade():
    def __init__(self, duration, function, *args):
        self.surface = pygame.Surface(SCREENSIZE)

        self.duration = duration
        self.half_duration = duration / 2
        
        self.timer = self.half_duration

        self.function = function()
        self.args = args

        self.run_action = False
        self.switched = False

    def draw(self, surface):
        surface.blit(self.surface, (0, 0), special_flags=BLEND_SUB)

    def update(self, delta):
        self.timer -= delta

        if self.timer < 0:
            if not self.run_action:
                self.timer = self.half_duration
                self.function(*self.args)
                self.run_action = True
