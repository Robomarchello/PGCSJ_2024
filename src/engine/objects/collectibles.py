import pygame
from src.engine.camera import Camera
from src.engine.asset_manager import AssetManager


class Collectible:
    def __init__(self, position, texture_key, texture_key_picked):
        self.position = pygame.Vector2(position)

        self.texture_key = texture_key
        self.texture_key_picked = texture_key_picked

        self.texture = AssetManager.images[texture_key]
        self.texture_picked = AssetManager.images[texture_key_picked]

        self.rect = self.texture.get_rect(center=self.position)
        self.radius = self.rect.width / 2

        self.picked_up = False

    @property
    def cam_pos(self):
        return Camera.displace_position(self.position)

    def draw(self, surface):
        cam_rect = self.rect.copy()
        cam_rect.center = self.cam_pos

        # make animation?
        if not self.picked_up:
            surface.blit(self.texture, cam_rect.topleft)
        else:
            surface.blit(self.texture_picked, cam_rect.topleft)
        #surface.blit(self.texture, self.rect.topleft)
