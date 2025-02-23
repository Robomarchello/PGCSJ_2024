import math
import pygame
from src.engine.constants import GRAVITY_CONST
from src.engine.camera import Camera
from src.engine.asset_manager import AssetManager
from src.engine.vfx.emitters import BlackHoleEmitter


class BlackHole:
    def __init__(self, position, mass):
        self.position = pygame.Vector2(position)
        self.mass = mass 

        self.radius = 30 + abs(mass) * 0.15
        self.color = pygame.Color(255, 255, 255)

        self.small_black_hole = AssetManager.images['smol_blek_hole']
        self.black_hole_texture = AssetManager.images['black_hole']

        self.small_white_hole = AssetManager.images['smol_white_hole']
        self.white_hole_texture = AssetManager.images['white_hole']

        self.texture_rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)

        self.emitter = BlackHoleEmitter(self.position, self.radius, self.mass)

        self.pulsing_timer = 0.0
        self.pulsing = 1 + math.cos(self.pulsing_timer) * 0.1

    @property
    def cam_pos(self):
        return Camera.displace_position(self.position)

    def draw(self, surface):
        scaled_rect = self.texture_rect.copy()
        scaled_rect.scale_by_ip(self.pulsing)
        scaled_rect.center = self.cam_pos
        
        if self.mass > 0:
            if self.radius <= 64:
                scaled_texture = pygame.transform.scale(
                    self.small_black_hole, scaled_rect.size
                )
            else:
                scaled_texture = pygame.transform.scale(
                    self.black_hole_texture, scaled_rect.size
                )
                
            #surface.blit(scaled_texture, scaled_rect.topleft)
        elif self.mass < 0:
            if self.radius <= 64:
                scaled_texture = pygame.transform.scale(
                    self.small_white_hole, scaled_rect.size
                )
            else:
                scaled_texture = pygame.transform.scale(
                    self.white_hole_texture, scaled_rect.size
                )
    
        self.emitter.draw(surface)
        surface.blit(scaled_texture, scaled_rect.topleft)

    def update(self, delta):
        self.pulsing_timer += delta * 3

        self.pulsing = 1 + math.cos(self.pulsing_timer) * 0.1

        self.emitter.update_rect(self.position)
        self.emitter.update(delta)

    def calculate_attraction(self, position_other, mass_other):
        diff = self.position - position_other
        if diff == (0, 0):
            return pygame.Vector2()
        direction = diff.normalize()
        distance = diff.magnitude()
        gravity_force = (GRAVITY_CONST * mass_other * self.mass) / distance ** 2
        
        return direction * gravity_force