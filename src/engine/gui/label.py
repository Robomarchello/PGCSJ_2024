import pygame
from .ui_element import UIElement


class Label(UIElement):
    def __init__(
            self,
            font: pygame.Font,
            text: str,
            color: pygame.Color,
            antialias: bool = False,
            anchors: dict = {}
    ):
        # could use str.format
        self.font = font
        self.text = text
        self.color = color
        self.antialias = antialias
        self.anchors = anchors

        self.set_text(self.text)

        self.scale = 1.0

        super().__init__(self.rect)

    def draw(self, surface):
        render = pygame.transform.scale_by(self.render, self.scale)
        rect = self.rect.scale_by(self.scale)
        
        surface.blit(render, rect.topleft)

    def update(self, delta):
        self._get_offset_rect()

    def set_text(self, text):
        self.render = self.font.render(text, self.antialias, self.color)

        self._rect = self.render.get_rect()
        self.rect_to_achors()

        self.rect = self._rect.copy()