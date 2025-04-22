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

        super().__init__(self.rect)

    def draw(self, surface):
        surface.blit(self.render, self.rect.topleft)

    def update(self, delta):
        self._get_offset_rect()

    def set_text(self, text):
        self.render = self.font.render(text, self.antialias, self.color)

        self._rect = self.render.get_rect()
        for attr, value in self.anchors.items():
            setattr(self._rect, attr, value)

        self.rect = self._rect.copy()