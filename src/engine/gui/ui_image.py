import pygame
from src.engine.gui.ui_element import UIElement


class UIImage(UIElement):
    def __init__(
            self,
            image: pygame.Surface,
            anchors: dict = {},
    ):
        self._image = image
        img_rect = self._image.get_rect()

        self.anchors = anchors

        self.scale = 1.0
        self.last_scale = 0.0

        self.last_rotation = 0
        self.rotation = 0

        super().__init__(img_rect)

        self.update_scaled_image()

    def draw(self, surface):        
        surface.blit(self.image, self.rect.topleft)
    
    def update(self, delta):
        self.rect_to_anchors()
        self._get_offset_rect()
        self.update_scaled_image()

    def update_scaled_image(self):
        if self.last_rotation != self.rotation or self.scale != self.last_scale:
            image = self._image
            image = pygame.transform.rotate(image, self.rotation)
            image = pygame.transform.scale_by(image, self.scale)

            self.image = image
            self.last_rotation = self.rotation
            self.last_scale = self.scale

            self.rect = self.image.get_rect(center=self.rect.center)
            self._rect = self.rect.copy()