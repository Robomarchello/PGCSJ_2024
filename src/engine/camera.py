import pygame
from pygame import Vector2
from src.engine.utils import Debug
from src.engine.constants import *
from src.engine.utils import get_shake


class Camera:
    # for every object, separate the physics position and player's view
    # I think zooming would be cool, takes time though
    displacement = Vector2()
    pos = Vector2() 
    offset = Vector2(SCREEN_W // 2, SCREEN_H // 2)
    rect = pygame.Rect(*pos, *SCREENSIZE)
    bounds: pygame.Rect = None

    focus: Vector2 | None = None

    shake_timer = 0
    shake_strength = 0
    
    player = None
    secondary_focus: Vector2 | None = None
    
    @classmethod
    def initialize(cls, player):
        cls.player = player

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

    @classmethod
    def update(cls, delta):
        if cls.focus is not None:
            difference = cls.focus - cls.displacement
            cls.displacement += difference * 0.1 * delta * SPEED_FACTOR
            cls.pos = cls.displacement - cls.offset
        else:
            pass
    
        if cls.secondary_focus is not None:
            diff = pygame.Vector2(
                cls.player.position.x - cls.secondary_focus[0],
                cls.player.position.y - cls.secondary_focus[1]
                )
            diff_len = min(diff.length(), 400)
            diff_norm = diff.normalize()
            displacement = diff_norm * diff_len
            cls.offset[0] = SCREEN_W // 2 + displacement[0] * 0.5
            cls.offset[1] = SCREEN_H // 2 + displacement[1] * 0.3

        if cls.bounds is not None:
            cls.rect.topleft = cls.pos
            cls.rect.clamp_ip(cls.bounds)
            cls.pos.update(cls.rect.topleft)

        if cls.shake_timer > 0:
            cls.shake_timer -= delta
            
            cls.pos += get_shake(cls.shake_strength)

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

