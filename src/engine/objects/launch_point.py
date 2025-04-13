import pygame
from src.engine.constants import SPEED_FACTOR
from src.engine.utils import collide_circles
from src.engine.objects import Object
from src.engine.camera import Camera


class LaunchPoint(Object):
    def __init__(self, position, radius, player, controller):
        super().__init__(position)

        self.radius = radius

        self.player = player
        self.controller = controller
        
        self.used = False

    def update(self, delta):
        collision = collide_circles(
            self.position, self.radius,
            self.player.position, self.player.radius
        )
        if collision and not self.used:
            self.player.freeze = True

            self.controller.launch_point = self

            pull_force = self.pulling_force(self.player.position)
            self.player.position += pull_force * delta * SPEED_FACTOR

    def pulling_force(self, position: pygame.Vector2): 
        difference = self.position - position
        
        return difference * 0.18

    def draw(self, surface):
        pygame.draw.circle(surface, 'grey', self.cam_pos, self.radius * Camera.scale_factor)

    def serialize(self):
        return {
            'type': 'LaunchPoint',
            'position': tuple(self.position),
            'radius': self.radius,
        }

    @classmethod
    def deserialize(cls, data: dict, player, controller):
        return cls(
            position=data['position'],
            radius=data['radius'],
            player=player,
            controller=controller
            )