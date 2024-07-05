import pygame
from pygame import Vector2
from src.engine.utils import Debug
from src.engine.constants import *


# TODO: take player's velocity, launch_direction into account, allow freecam
class Camera:
    # for every object, separate the physics position and player's view
    # I think zooming is possible, but will cause a lot of problems
    pos = Vector2() 
    offset = Vector2(200, SCREEN_H // 2) # SCREEN_W // 2
    rect = pygame.Rect(*pos, *SCREENSIZE)
    bounds: pygame.Rect

    focus: Vector2 | None = None
    # for target_pos, perhaps a secondary focus?
    secondary_focus: Vector2 | None = None

    @classmethod
    def debug_draw(cls):
        Debug.add_line(
            (0, SCREEN_H / 2), (SCREEN_W, SCREEN_H / 2)
        )
        Debug.add_line(
            (SCREEN_W / 2, 0), (SCREEN_W / 2, SCREEN_H)
        )

    @classmethod
    def update(cls, delta):
        #cls.focus = None
        if cls.focus is not None:
            difference = cls.focus - (cls.pos + cls.offset)
            cls.pos += difference * 0.1 * delta * SPEED_FACTOR
        else:
            pass

    @classmethod
    def displace_position(cls, position: Vector2):
        return position - cls.pos

    @classmethod
    def displace_rect(cls, rect: Vector2):
        cam_rect = rect.copy()
        cam_rect.x -= cls.pos.x
        cam_rect.y -= cls.pos.y
        return cam_rect

    @classmethod
    def handle_event(cls, event):
        # put some controls here
        pass

