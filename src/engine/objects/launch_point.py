import pygame
from src.engine.constants import SPEED_FACTOR
from src.engine.utils import collide_circles
from src.engine.camera import Camera


class LaunchPoint:
    def __init__(self, position, radius, player, controller):
        self.position = position
        self.radius = radius

        self.player = player
        self.controller = controller
        
        self.used = False

    @property
    def cam_pos(self):
        return Camera.displace_position(self.position)

    def update(self, delta):
        collision = collide_circles(
            self.position, self.radius,
            self.player.position, self.player.radius
        )
        if collision and not self.used:
            self.player.freeze = True
            self.controller.shot = True

            self.controller.launch_point = self

            pull_force = self.pulling_force(self.player.position)
            self.player.position += pull_force * delta * SPEED_FACTOR

    def pulling_force(self, position): 
        difference = pygame.Vector2(
            self.position[0] - position[0],
            self.position[1] - position[1]
        )
        return difference * 0.18

    def draw(self, surface):
        pygame.draw.circle(surface, 'grey', self.cam_pos, self.radius)
