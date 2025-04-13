import pygame
from src.engine.base import Base


class Label(Base):
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

    def draw(self, surface):
        surface.blit(self.render, self.rect.topleft)

    def update(self, delta):
        self._get_offset_rect()

    def handle_event(self, event):
        pass

    def set_text(self, text):
        self.render = self.font.render(text, self.antialias, self.color)

        self.offset = pygame.Vector2()
        self._rect = self.render.get_rect()

        for attr, value in self.anchors.items():
            setattr(self._rect, attr, value)

        self.rect = self._rect.copy()

    def set_offset(self, x, y):
        self.offset.update(x, y)

    def _get_offset_rect(self):
        '''Needed to be able to move the label around, like in level selection menu.'''
        self.rect = self._rect.copy()

        self.rect.x += self.offset.x
        self.rect.y += self.offset.y