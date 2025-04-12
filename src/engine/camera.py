import pygame
from pygame import Vector2

from src.engine.utils import Debug
from src.engine.constants import *
from src.engine.utils import get_shake


class Camera:
    # for every object, separate the physics position and player's view
    displacement = Vector2()
    scale_factor = 0.5
    pos = Vector2() 
    offset = Vector2(SCREEN_W // 2, SCREEN_H // 2)
    rect = pygame.Rect(*pos, *SCREENSIZE)
    bounds: pygame.Rect = None

    focus: Vector2 | None = None

    shake_timer = 0
    shake_strength = 0

    @classmethod
    def shake(cls, time, strength):
        cls.shake_timer = time
        cls.shake_strength = strength

    @classmethod
    def origin_lock(cls):
        cls.focus = None
        cls.secondary_focus = None

        # cls.pos *= 0
        # cls.offset *= 0

    @classmethod
    def debug_draw(cls):
        Debug.add_line(
            (0, SCREEN_H / 2), (SCREEN_W, SCREEN_H / 2)
        )
        Debug.add_line(
            (SCREEN_W / 2, 0), (SCREEN_W / 2, SCREEN_H)
        )

        Debug.add_point(cls.offset)

        Debug.add_text('scale: ' + str(cls.scale_factor))

    @classmethod
    def update(cls, delta):
        if cls.focus is not None:
            difference = cls.focus - cls.displacement
            cls.displacement += difference * 0.1 * delta * SPEED_FACTOR
            cls.pos = cls.displacement - cls.offset
    
        if cls.bounds is not None:
            cls.rect.topleft = cls.pos
            cls.rect.clamp_ip(cls.bounds)
            cls.pos.update(cls.rect.topleft)

        if cls.shake_timer > 0:
            cls.shake_timer -= delta
            cls.pos += get_shake(cls.shake_strength)

    @classmethod
    def displace_position(cls, position: Vector2):
        '''
        1. get distance from origin
        2. mult distance by zoom factor
        3. add origin back'''
        camera_pos = Vector2()
        camera_pos.x = (position.x - cls.displacement.x) * cls.scale_factor
        camera_pos.y = (position.y - cls.displacement.y) * cls.scale_factor

        camera_pos += cls.offset
        return camera_pos

    @classmethod
    def displace_rect(cls, rect: Vector2):
        cam_rect = rect.scale_by(cls.scale_factor)
        cam_rect.topleft = cls.displace_position(Vector2(rect.topleft))
        return cam_rect

    @classmethod
    def handle_event(cls, event):
        # put some controls here
        if event.type == pygame.MOUSEWHEEL:
            cls.scale_factor += 0.01 * event.y
            cls.scale_factor = round(cls.scale_factor, 3)
