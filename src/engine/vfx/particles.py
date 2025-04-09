import math
from typing import Tuple
from dataclasses import dataclass
import pygame
from pygame.locals import *
from src.engine.camera import Camera
from src.engine.constants import SPEED_FACTOR


@dataclass
class ParticleTemplate:
    angle_range: float | Tuple[float]
    speed_range: float | Tuple[float]
    life_range: float | Tuple[float]
    scale_range: float | Tuple[float]

    texture: pygame.Surface
    gradient: Tuple[pygame.Color]

    texture_rot_range: float | Tuple[float]

    velocity_change: float = 1.0
    scale_change: float = 1.0


class Particle:
    def __init__(
            self,
            position,
            angle,
            speed,
            life,
            scale,
            texture,
            gradient,
            texture_rot_speed,
            velocity_change=1.0,
            scale_change=1.0
        ):
        self.position = position
        self.velocity = pygame.Vector2(
            speed * math.cos(math.radians(angle)),
            -speed * math.sin(math.radians(angle))
        )
        self.acceleration = pygame.Vector2()
        
        self.life = life
        self.age = life

        self.scale = scale
        self.texture = texture
        self.texture_rotation = angle
        self.texture_rot_speed = texture_rot_speed

        self.gradient = gradient
        self.update_color()

        self.velocity_change = velocity_change
        self.scale_change = scale_change

        self.texture_rect = texture.get_rect()

    @property
    def cam_pos(self):
        return Camera.displace_position(self.position)

    def motion_logic(self, delta):
        self.velocity += self.acceleration * delta * SPEED_FACTOR
        self.position += self.velocity * delta * SPEED_FACTOR

        self.acceleration *= 0
    
    def update_param_change(self, delta):
        self.scale += self.scale * (self.scale_change - 1) * delta * SPEED_FACTOR
        self.velocity += self.velocity * (self.velocity_change - 1) * delta * SPEED_FACTOR

    def update_color(self):
        progress = min(self.age / self.life, 0.9999)  # ensure index is in bounds
        index = int(progress * len(self.gradient))
        self.color = self.gradient[index]