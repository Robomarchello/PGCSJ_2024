import pygame
from src.engine.config import SPEED_FACTOR
from src.engine.objects import BlackHole


class OrbitingBlackHole(BlackHole):
    def __init__(self, origin, position, mass, rot_speed):
        super().__init__(position, mass)

        self.origin = pygame.Vector2(origin)
        self.rot_speed = rot_speed

    # def draw additional circle

    def update(self, delta):
        super().update(delta)
        vec = self.position - self.origin
        vec.rotate_ip(self.rot_speed * delta * SPEED_FACTOR)

        new_position = vec + self.origin
        self.position = new_position

    def serialize(self):
        return {
            'type': 'OrbitingBlackHole',
            'origin': tuple(self.origin),
            'position': tuple(self.position),
            'mass': self.mass,
            'rot_speed': self.rot_speed
        }
    
    @classmethod
    def deserialize(cls, data: dict):
        return cls(
            origin=data['origin'],
            position=data['position'],
            mass=data['mass'],
            rot_speed=data['rot_speed']
            )