import random
import pygame
from src.engine.constants import SCREENSIZE, SCREEN_W, SCREEN_H
from src.engine.camera import Camera
from src.engine.asset_manager import AssetManager


class SpaceBackground:
    def __init__(self, stars_num): # add layers, or that just like speed factor
        self.stars_num = stars_num
        
        self.texture_pos = pygame.Vector2(0, 0)
        self.space_texture = AssetManager.images['background_space_scaled']

        self.move_factor = 0.7
        self.stars_layer = AssetManager.images['background_stars_scaled']
        self.stars_layer.set_colorkey((255, 0, 0))

    def draw(self, surface):
        size = self.space_texture.get_size()
        
        # Determine the number of tiles needed to cover the screen
        num_tiles_x = (SCREEN_W // size[0]) + 2
        num_tiles_y = (SCREEN_H // size[1]) + 2
        
        texture_pos = Camera.displace_position(self.texture_pos)
        
        # Calculate the starting positions
        start_x = texture_pos[0] % size[0] - size[0]
        start_y = texture_pos[1] % size[1] - size[1]
        
        # Draw the textures in a grid
        for x in range(num_tiles_x):
            for y in range(num_tiles_y):
                position = (start_x + x * size[0], start_y + y * size[1])
                surface.blit(self.space_texture, position)

        star_pos = self.texture_pos - (Camera.displacement - Camera.offset) * self.move_factor

        # Calculate the starting positions
        start_x = star_pos[0] % size[0] - size[0]
        start_y = star_pos[1] % size[1] - size[1]
        
        # Draw the textures in a grid
        for x in range(num_tiles_x):
            for y in range(num_tiles_y):
                position = (start_x + x * size[0], start_y + y * size[1])
                surface.blit(self.stars_layer, position)

    def update(self, delta):
        pass