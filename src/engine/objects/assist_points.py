import pygame
from src.engine.constants import SPEED_FACTOR
from src.engine.utils import collide_circles
from src.engine.camera import Camera
from src.engine.asset_manager import AssetManager



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


class FinishPoint:
    def __init__(self, position, radius, player):
        self.position = pygame.Vector2(position)
        self.radius = radius

        self.player = player

        self.image = AssetManager.images['planet'].convert_alpha()

        self.rotation_timer = 0.0
        self.angle = 0

        self.touched = False

        self.complete_timer = 1.0
        self.timer = self.complete_timer
        self.completed = False
        self.reacted = False
        
    @property
    def cam_pos(self):
        return Camera.displace_position(self.position) 

    def update(self, delta):
        collision = collide_circles(
            self.position, self.radius,
            self.player.position, self.player.radius
        )
        if collision and not self.completed:
            self.player.freeze = True
            self.touched = True

            pull_force = self.pulling_force(self.player.position)
            self.player.position += pull_force * delta * SPEED_FACTOR

        if self.touched:
            self.timer -= delta

            if self.timer < 0.0:
                self.completed = True

        self.rotation_timer += -delta
        self.angle = self.rotation_timer

    def pulling_force(self, position): 
        difference = pygame.Vector2(
            self.position[0] - position[0],
            self.position[1] - position[1]
        )
        return difference * 0.1

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        image_rect = rotated_image.get_rect(center=self.cam_pos)
        surface.blit(rotated_image, image_rect.topleft)