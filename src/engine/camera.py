import pygame
from pygame import Vector2

from src.engine.utils import Debug
from src.engine.config import *
from src.engine.utils import get_shake, clamp


class CameraShake:
    timer = 0
    strength = 0

    @classmethod
    def start(cls, duration, strength):
        cls.timer = duration
        cls.strength = strength

    @classmethod
    def update(cls, delta):
        if cls.timer > 0:
            cls.timer -= delta
            return get_shake(cls.strength)
        return Vector2()


class CameraZoom:
    scale_modes = [1.5, 0.7, 1]
    scale = 1.0
    target_scale = 1.0
    reference_scale = (SCREEN_W / BASE_SCREENSIZE[0] + SCREEN_H / BASE_SCREENSIZE[1]) / 2

    extra_space = False

    @classmethod
    def update(cls, delta):
        if cls.extra_space:
            cls.scale += (cls.target_scale - cls.scale - 0.1) * 0.1 * delta * SPEED_FACTOR
        else:
            cls.scale += (cls.target_scale - cls.scale) * 0.1 * delta * SPEED_FACTOR
        return round(cls.scale * cls.reference_scale, 3)

    @classmethod
    def handle_event(cls, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                new_target = cls.scale_modes.pop(0)
                cls.target_scale = new_target
                cls.scale_modes.append(new_target)

        if event.type == pygame.MOUSEWHEEL:
            cls.target_scale += 0.05 * event.y
            cls.target_scale = clamp(cls.target_scale, 0.1, 5)


class Camera:
    # for every object, separate the physics position and player's view
    displacement = Vector2()
    scale_factor = 1.0
    pos = Vector2() 
    offset = Vector2(SCREEN_W // 2, SCREEN_H // 2)
    rect = pygame.Rect(*pos, *SCREENSIZE)
    bounds: pygame.Rect = None

    focus: Vector2 | None = None

    camera_zoom = CameraZoom

    @classmethod
    def shake(cls, duration, strength):
        CameraShake.start(duration, strength)

    @classmethod
    def set_target_scale(cls, scale):
        CameraZoom.target_scale = scale

    @classmethod
    def set_scale(cls, scale):
        CameraZoom.target_scale = scale
        CameraZoom.scale = scale

    def restart(cls):
        cls.displacement = Vector2()
        cls.scale_factor = 1.0
        cls.set_scale(cls.scale_factor)

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

        cls.pos += CameraShake.update(delta)
        cls.scale_factor = CameraZoom.update(delta)

    @classmethod
    def displace_position(cls, position):
        '''
        1. get distance from origin
        2. mult distance by zoom factor
        3. add origin back'''
        camera_pos = Vector2()
        camera_pos.x = (position[0] - cls.displacement[0]) * cls.scale_factor
        camera_pos.y = (position[1] - cls.displacement[1]) * cls.scale_factor

        camera_pos += cls.offset
        return camera_pos

    @classmethod
    def displace_rect(cls, rect: Vector2):
        cam_rect = rect.scale_by(cls.scale_factor)
        cam_rect.topleft = cls.displace_position(rect.topleft)
        return cam_rect

    @classmethod
    def handle_event(cls, event):
        CameraZoom.handle_event(event)