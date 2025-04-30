import pygame
from pygame.locals import *
from src.engine.base import Base
from src.engine.gui import GUInterface, TextButton
from src.engine.asset_manager import AssetManager
from src.engine.gui import NineSlice, Slider
from src.engine.gui.menu_buttons import ToLevelSelectionButton, ToPlayMenuButton, ToSettingsButton
import src.engine.config as c


class BaseSubMenu(Base):
    def __init__(self, position: pygame.Vector2, manager):
        self.reference_scale = (c.SCREEN_W / c.BASE_SCREENSIZE[0] + c.SCREEN_H / c.BASE_SCREENSIZE[1]) / 2
        self.position = position
        self._rect = pygame.Rect(0, 0, *c.SCREENSIZE)
        self.rect = self._rect.copy()
        self.rect.center = self.position
        
        self.interface = GUInterface()

        self.manager: 'Menu' = manager # type: ignore

    def draw(self, surface):
        self.interface.draw(surface)

    def update(self, delta):
        self.interface.update(delta)
        self.interface.set_scale(min(1, self.reference_scale))

    def set_enabled(self, enabled: bool):
        self.interface.set_enabled(enabled)

    def set_offset(self, x, y):
        self.interface.set_offset(x, y)

    def handle_event(self, event):
        self.interface.handle_event(event)