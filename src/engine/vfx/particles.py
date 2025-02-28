import pygame
import math
from src.engine.objects import Object


class Particle(Object):
    def __init__(self, position, angle, speed, life, rotation,
                  rotation_change, color1, color2, texture):
        velocity = pygame.Vector2(
            speed * math.cos(math.radians(angle)),
            speed * -math.sin(math.radians(angle))
        )

        super().__init__(position, velocity)

        self.life = life
        self.crnt_life = life

        self.texture_rotation = rotation
        self.rotation_change = rotation_change

        self.color1 = color1
        self.color2 = color2
        self.crnt_color = color1

        self.texture = texture
        self.texture_rect = texture.get_rect()