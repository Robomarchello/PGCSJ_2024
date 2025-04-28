import pygame
from src.engine.base import Base


class UIElement(Base):
    def __init__(self, rect):
        self._rect = rect
        self.rect = self._rect.copy()
        self.offset = pygame.Vector2()

        self.enabled = True

    def set_offset(self, x, y):
        self.offset.update(x, y)

    def _get_offset_rect(self):
        '''Needed to be able to move the buttons around, like in level selection menu.'''
        self.rect = self._rect.copy()

        self.rect.x += self.offset.x
        self.rect.y += self.offset.y

    def rect_to_anchors(self):
        for attr, value in self.anchors.items():
            setattr(self._rect, attr, value)

    def handle_event(self, event):
        pass