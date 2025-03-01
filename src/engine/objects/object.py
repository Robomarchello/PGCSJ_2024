import pygame
from src.engine.camera import Camera
from src.engine.base import Base
from src.engine.constants import SPEED_FACTOR

# base class for all objects
class Object(Base):
    def __init__(self, position, velocity=0, mass=1):
        self.position = pygame.Vector2(position) # real position
        self.velocity = pygame.Vector2(velocity)
        self.acceleration = pygame.Vector2()
        self.force = pygame.Vector2()

        self.mass = mass

        self.sprite = None #Sprite(image) when implemented

    def motion_logic(self, delta):
        self.acceleration = self.force / self.mass
        
        self.velocity += self.acceleration * delta * SPEED_FACTOR
        self.position += self.velocity * delta * SPEED_FACTOR

        self.force *= 0

    @property
    def cam_pos(self):
        return self.position - Camera.pos