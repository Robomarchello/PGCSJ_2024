from dataclasses import dataclass
import pygame
from src.engine.camera import Camera


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

    def serialize(self):
        return {
            'rect': self.rect,
            'hitrect': self.hitrect,
            'normal': self.normal,
            'color': self.color,
        }
    
    @classmethod
    def deserialize(cls, data):
        return cls(
            rect=data['rect'],
            hitrect=data['hitrect'],
            normal=data['normal'],
            color=data['color']
        )


class PortalPair:
    def __init__(self, portal_1, portal_2):
        self.portal_1: Portal = portal_1
        self.portal_2: Portal = portal_2

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
    
    def serialize(self):
        return {
            'portal_1': self.portal_1.serialize(),
            'portal_2': self.portal_2.serialize()
        }

    @classmethod
    def deserialize(cls, data):
        return cls(
            Portal.deserialize(data['portal1']),
            Portal.deserialize(data['portal2'])
        )