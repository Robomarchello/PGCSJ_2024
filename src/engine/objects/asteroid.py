import pygame
from src.engine.constants import SPEED_FACTOR
from src.engine.camera import Camera
from src.engine.asset_manager import AssetManager


class Asteroid:
    def __init__(self, position, velocity, mass, radius):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.acceleration = pygame.Vector2()
        self.force = pygame.Vector2()

        self.texture = AssetManager.images['asteroid']
        self.texture_rect = self.texture.get_rect()

        self.mass = mass
        self.radius = radius

        self.orientation = 0.0

    @property
    def cam_pos(self):
        return Camera.displace_position(self.position)

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