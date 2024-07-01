import pygame
from pygame import Vector2
from utils import Debug
import constants as c


class Camera:
    # for every object, separate the physics position and player's view
    # I think zooming is possible, but will cause a lot of problems
    position = Vector2()
    rect = pygame.Rect(*position, *c.SCREENSIZE)

    focus: Vector2 | None

    def set_focus(self):
        pass

    def update(self):
        # update camera
        '''
        if focus is None:
            ...
        else:
            ...
        '''
        pass

    def handle_event(self, event):
        # put some controls here
        pass

