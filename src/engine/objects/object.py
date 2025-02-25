import pygame
from src.engine.camera import Camera
from src.engine.base import Base


# base class for all objects
class Object(Base):
    def __init__(self, position, velocity=0, mass=1):
        self.position = pygame.Vector2(position) # real position
        self.velocity = pygame.Vector2(velocity)
        self.acceleration = pygame.Vector2()
        # self.force = pygame.Vector2() then a = f/m

        self.mass = mass

        self.sprite = None #Sprite(image) when implemented

    @property
    def cam_pos(self):
        return self.position - Camera.pos