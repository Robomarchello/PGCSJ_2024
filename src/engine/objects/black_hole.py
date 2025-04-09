import math
import pygame
from src.engine.constants import GRAVITY_CONST
from src.engine.asset_manager import AssetManager
from src.engine.vfx.game_particles import BlackHoleEmitter
from src.engine.objects import Object


class BlackHole(Object):
    def __init__(self, position, mass):
        super().__init__(position, mass=mass)

        self.radius = 30 + abs(mass) * 0.15 # baaad
        self.color = pygame.Color(255, 255, 255)

        self.texture = self._determine_texture()
        self.texture_rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)

        self.emitter = BlackHoleEmitter(self.position, self.radius, self.mass)

        self.pulsing_timer = 0.0
        self.pulsing = 1 + math.cos(self.pulsing_timer) * 0.1

    def draw(self, surface):
        scaled_rect = self.texture_rect.copy()
        scaled_rect.scale_by_ip(self.pulsing)
        scaled_rect.center = self.cam_pos

        scaled_texture = pygame.transform.scale(self.texture, scaled_rect.size)  

        self.emitter.draw(surface)
        surface.blit(scaled_texture, scaled_rect.topleft)

    def _determine_texture(self):
        if self.mass > 0:
            if self.radius <= 64:
                return AssetManager.images['smol_blek_hole'].convert_alpha()
            else:
                return AssetManager.images['black_hole'].convert_alpha()
                
        elif self.mass < 0:
            if self.radius <= 64:
                return AssetManager.images['smol_white_hole'].convert_alpha()
            else:
                return AssetManager.images['white_hole'].convert_alpha()

    def update(self, delta):
        self.pulsing_timer += delta * 3 # meh constant

        self.pulsing = 1 + math.cos(self.pulsing_timer) * 0.1

        self.emitter.update_rect(self.position)
        self.emitter.update(delta)

    def calculate_attraction(self, obj: Object):
        '''Calculate gravitation force between two objects'''
        diff = self.position - obj.position
        if diff == (0, 0):
            return pygame.Vector2()
        direction = diff.normalize()
        distance = diff.magnitude()
        gravity_force = (GRAVITY_CONST * obj.mass * self.mass) / distance ** 2
        
        return direction * gravity_force
    
    def serialize(self):
        return {
            'type': 'BlackHole',
            'position': tuple(self.position),
            'mass': self.mass,
        }

    @classmethod
    def deserialize(cls, data: dict):
        return cls(
            position=data['position'],
            mass=data['mass'],
            )
