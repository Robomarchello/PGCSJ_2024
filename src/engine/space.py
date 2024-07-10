import random
from dataclasses import dataclass
import pygame
from src.engine.constants import SCREENSIZE
from src.engine.camera import Camera


@dataclass
class Star:
    position: pygame.Vector2
    texture: pygame.Surface
    move_factor: float
    life_time: float

    @property
    def cam_pos(self):
        pos = self.position - (Camera.displacement - Camera.offset) * self.move_factor
        return pos


class SpaceBackground:
    def __init__(self, stars_num, star_textures): # add layers, or that just like speed factor
        self.stars_num = stars_num

        self.stars = []
        self.star_size = star_textures.get_size()
        for _ in range(self.stars_num):
            position = (
                random.randint(0, SCREENSIZE[0]),
                random.randint(0, SCREENSIZE[1])
                )
            
            move_factor = random.uniform(0.5, 1)
            star_texture = pygame.transform.scale_by(
                star_textures, move_factor
            )
            life_time = random.randint(300, 600)

            star = Star(position, star_texture, move_factor, life_time)
            self.stars.append(star)

    def draw(self, surface):
        size = self.star_size
        for star in self.stars:
            position = (
                star.cam_pos[0] % (SCREENSIZE[0] + size[0]) - size[0],
                star.cam_pos[1] % (SCREENSIZE[1] + size[1]) - size[1],
            )
            surface.blit(star.texture, position)

    def update(self, delta):
        pass