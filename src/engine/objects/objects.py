from dataclasses import dataclass
import pygame
from src.engine.constants import GRAVITY_CONST, SPEED_FACTOR
from src.engine.camera import Camera
from src.engine.asset_manager import AssetManager


__all__ = ['BlackHole', 'OrbitingBlackHole', 
           'ForceZone', 'GravityInvertor',
           'Portal', 'PortalPair'
           ]


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

    @property
    def cam_pos(self):
        return Camera.displace_position(self.position)

    def draw(self, surface):
        self.texture_rect.center = self.cam_pos
        
        if self.mass > 0:
            if self.radius <= 64:
                scaled_texture = pygame.transform.scale(
                    self.small_black_hole, self.texture_rect.size
                )
            else:
                scaled_texture = pygame.transform.scale(
                    self.black_hole_texture, self.texture_rect.size
                )
                
            #surface.blit(scaled_texture, self.texture_rect.topleft)
        elif self.mass < 0:
            if self.radius <= 64:
                scaled_texture = pygame.transform.scale(
                    self.small_white_hole, self.texture_rect.size
                )
            else:
                scaled_texture = pygame.transform.scale(
                    self.white_hole_texture, self.texture_rect.size
                )
            
        surface.blit(scaled_texture, self.texture_rect.topleft)

        
        #scaled_texture = pygame.transform.scale(self.small_black_hole, self.texture_rect.size)
        #surface.blit(scaled_texture, self.texture_rect.topleft)

    def calculate_attraction(self, position_other, mass_other):
        diff = self.position - position_other
        if diff == (0, 0):
            return pygame.Vector2()
        direction = diff.normalize()
        distance = diff.magnitude()
        gravity_force = (GRAVITY_CONST * mass_other * self.mass) / distance ** 2
        
        return direction * gravity_force


class OrbitingBlackHole(BlackHole):
    def __init__(self, origin, position, mass, rot_speed):
        super().__init__(position, mass)

        self.origin = pygame.Vector2(origin)
        self.rot_speed = rot_speed

    # def draw additional circle

    def update(self, delta):
        vec = self.position - self.origin
        vec.rotate_ip(self.rot_speed * delta * SPEED_FACTOR)

        new_position = vec + self.origin
        self.position = new_position

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


@dataclass
class Portal:
    rect: pygame.Rect
    hitrect: pygame.Rect
    normal: pygame.Vector2    
    color: pygame.Color

    def draw(self, surface):
        cam_rect = self.rect.copy()
        cam_rect.x -= Camera.pos[0]
        cam_rect.x -= Camera.pos[1]
        # temporary thing?
        cam_hit_rect = self.rect.copy()
        cam_hit_rect.x -= Camera.pos[0]
        cam_hit_rect.x -= Camera.pos[1]
        pygame.draw.rect(surface, self.color, cam_rect)
        pygame.draw.rect(surface, 'white', cam_hit_rect)


class PortalPair:
    def __init__(self, portal_1, portal_2):
        self.portal_1 = portal_1
        self.portal_2 = portal_2

    def update(self, delta):
        pass

    def draw(self, surface):
        self.portal_1.draw(surface)
        self.portal_2.draw(surface)

    def on_collision(self, rect, velocity):
        if velocity == (0, 0):
            return False
        
        rect_after = rect.copy()
        vel_after = velocity.copy()
        vel_normal = vel_after.normalize()
        
        dot_check = vel_normal.dot(self.portal_1.normal)
        if self.portal_1.hitrect.colliderect(rect) and dot_check > 0.0:
            portal_angle = self.portal_1.normal.angle_to(self.portal_2.normal)
            rect_after.center = self.portal_2.rect.center
            vel_after.rotate_ip(portal_angle)
            
            return rect_after, vel_after

        dot_check = vel_normal.dot(self.portal_2.normal) 
        if self.portal_2.hitrect.colliderect(rect) and dot_check < 0.0:
            portal_angle = self.portal_2.normal.angle_to(self.portal_1.normal)
            rect_after.center = self.portal_1.rect.center
            vel_after.rotate_ip(portal_angle)

            return rect_after, vel_after

        return False
    

class GravityInvertor:
    def __init__(self, position, timer, object_handler):
        self.position = position

        self.timer = timer
        self.crnt_timer = timer
        self.object_handler = object_handler
        
    def draw(self, surface):
        pass

    def update(self, delta):
        self.crnt_timer -= delta
        if self.crnt_timer < 0:
            self.crnt_timer = self.timer

            # *invert here* (which is probably is *-1 object's or player's mass )