import pygame
from src.engine.asset_manager import AssetManager
from src.engine.objects import Object


class Asteroid(Object):
    def __init__(self, position, velocity, mass, radius):
        super().__init__(position, velocity, mass)
        self.texture = AssetManager.images['asteroid']
        self.texture_rect = self.texture.get_rect()

        self.radius = radius

        self.orientation = 0.0

    def update(self, delta):
        self.motion_logic(delta)

    def draw(self, surface):
        pygame.draw.circle(surface, 'grey', self.cam_pos, self.radius)

        self.texture_rect.center = self.cam_pos
        surface.blit(self.texture, self.texture_rect.topleft)

    def serialize(self):
        return {
            'type': 'Asteroid',
            'position': tuple(self.position),
            'velocity': tuple(self.velocity),
            'mass': self.mass,
            'radius': self.radius
        }
    
    @classmethod
    def deserialize(cls, data: dict):
        return cls(
            position=data['position'],
            velocity=data['velocity'],
            mass=data['mass'],
            radius=data['radius'],
            )
