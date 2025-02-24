import pygame
from src.engine.constants import SPEED_FACTOR
from src.engine.asset_manager import AssetManager
from src.engine.objects.object import Object


class Asteroid(Object):
    def __init__(self, position, velocity, mass, radius):
        super().__init__(position, velocity, mass)
        self.force = pygame.Vector2() # fix this? inconsistent with everything

        self.texture = AssetManager.images['asteroid']
        self.texture_rect = self.texture.get_rect()

        self.radius = radius

        self.orientation = 0.0

    def update(self, delta):
        self.acceleration += self.force / self.mass
        self.velocity += self.acceleration * delta * SPEED_FACTOR
        self.position += self.velocity * delta * SPEED_FACTOR

        self.acceleration *= 0
        self.force *= 0
    
    def draw(self, surface):
        pygame.draw.circle(surface, 'grey', self.cam_pos, self.radius)

        self.texture_rect.center = self.cam_pos
        surface.blit(self.texture, self.texture_rect.topleft)