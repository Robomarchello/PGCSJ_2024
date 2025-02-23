import pygame
from src.engine.camera import Camera


class ForceZone:
    def __init__(self, force, rect, timer=0.0):
        self.force = force
        self.rect = pygame.Rect(rect)

        self.timer = timer
        self.crnt_timer = timer

    @property
    def cam_rect(self):
        return Camera.displace_rect(self.rect)

    def draw(self, surface):
        pygame.draw.rect(surface, 'orange', self.cam_rect, 5)

    def update(self, delta):
        pass