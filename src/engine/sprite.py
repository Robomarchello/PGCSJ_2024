import pygame
from src.engine.camera import Camera
from src.engine.base import Base


class Sprite(Base):
    prescale = [0.5, 2]
    def __init__(self, image, rect_anchors=['topleft'], static=False):
        self._original_image = image

        self.texture_scale = 1.0
        self.scale_factor = 1.0

        self.position = pygame.Vector2()
        self.rect_anchors = rect_anchors
        
        self.image_scaled = {}
        if static:
            self._scale_cache()
        self._scale_image()

        self.static = static
        self.visible = True

    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect.topleft)

    def update(self, position):
        # scale only then if there is change in scale factor
        scale = Camera.scale_factor
        if self.scale_factor != scale:
            self.scale_factor = scale

            self._scale_image()

        if not self.static:
            self._scale_image()

        # updating position
        self.position.update(position)
        camera_pos = Camera.displace_position(self.position)
        pos_rect = pygame.Rect(*camera_pos, 0, 0)
        for attr in self.rect_anchors:
            setattr(self.rect, attr, getattr(pos_rect, attr))

    def update_image(self, image):
        self._original_image = image
        if self.static:
            self._scale_image()

    def _scale_image(self):
        if self.scale_factor in self.image_scaled.keys():
            self.image = self.image_scaled[self.scale_factor]
        else:
            image_scale = self.texture_scale * self.scale_factor
            self.image = pygame.transform.scale_by(self._original_image, image_scale)
        
        self.rect = self.image.get_rect()
    
    def _scale_cache(self):
        '''Precalculate image scale factors'''
        for scale_factor in self.prescale:
            self.image_scaled[scale_factor] = pygame.transform.scale_by(self._original_image, self.scale_factor)
