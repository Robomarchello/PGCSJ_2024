import pygame
from src.engine.camera import Camera


class ForceZone:
    def __init__(self, force, rect, timer=0.0):
        self.force = force
        self.rect: pygame.Rect = pygame.Rect(rect)

        self.timer = timer
        self.crnt_timer = timer

    @property
    def cam_rect(self):
        return Camera.displace_rect(self.rect)

    def draw(self, surface):
        pygame.draw.rect(surface, 'orange', self.cam_rect, 5)

    def update(self, delta):
        pass

    def serialize(self):
        return {
            'type': 'ForceZone',
            'force': self.force,
            'rect': tuple(self.rect),
            'timer': self.timer
        }

    @classmethod
    def deserialize(cls, data: dict):
        return cls(
            position=data['position'],
            force=data['force'],
            rect=data['rect'],
            timer=data['timer'],
            )