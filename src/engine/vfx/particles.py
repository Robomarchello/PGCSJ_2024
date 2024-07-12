import pygame
import math
import random
from src.engine.constants import SPEED_FACTOR
from src.engine.camera import Camera
from src.engine.utils import Debug


class Particle:
    def __init__(self, position, angle, speed, life, rotation,
                  rotation_change, color1, color2, texture):
        self.position = position
        self.velocity = pygame.Vector2(
            speed * math.cos(math.radians(angle)),
            -speed * math.sin(math.radians(angle))
        )
        self.acceleration = pygame.Vector2(0, 0)

        self.life = life
        self.crnt_life = life

        self.texture_rotation = rotation
        self.rotation_change = rotation_change

        self.color1 = color1
        self.color2 = color2
        self.crnt_color = color1

        self.texture = texture
        self.texture_rect = texture.get_rect()

    @property
    def cam_pos(self):
        return Camera.displace_position(self.position)