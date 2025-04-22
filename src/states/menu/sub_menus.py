import pygame
from pygame.locals import *
from src.engine.base import Base
from src.engine.gui import GUInterface, Button
from src.engine.asset_manager import AssetManager
from src.engine.gui.menu_buttons import ToLevelSelectionButton, ToPlayMenuButton, ToSettingsButton
import src.engine.config as c


class BaseSubMenu(Base):
    def __init__(self, position: pygame.Vector2, manager):
        self.reference_scale = (c.SCREEN_W / c.BASE_SCREENSIZE[0] + c.SCREEN_H / c.BASE_SCREENSIZE[1]) / 2
        self.position = position
        self.rect = pygame.Rect(0, 0, *c.SCREENSIZE)
        self.rect.center = self.position
        
        self.interface = GUInterface()

        self.manager = manager

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


class PlayMenu(BaseSubMenu):
    def __init__(self, manager):
        position = pygame.Vector2(c.SCREEN_AREA.center)
        super().__init__(position, manager)

        self.interface.add_label(
            font=AssetManager.fonts['font_48'],
            text='Mediocre Game with Golf-Like',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': c.SCREEN_W / 2,
                'top': 50 * self.reference_scale
            }
        )
        self.interface.add_label(
            font=AssetManager.fonts['font_48'],
            text='Gameplay In Space!',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': c.SCREEN_W / 2,
                'top': 110 * self.reference_scale
            }
        )
        self.interface.add_label(
            font=AssetManager.fonts['font_42'],
            text='Click anywhere to play',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': c.SCREEN_W / 2,
                'top': c.SCREEN_H - 120 * self.reference_scale
            }
        )
        # buttons are added in Menu class
        self.interface.add_button(ToSettingsButton(self.manager.to_settings))
        self.interface.add_button(ToLevelSelectionButton(self.manager.to_level_selection))

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                raise SystemExit


class SettingsMenu(BaseSubMenu):
    def __init__(self, manager):
        position = pygame.Vector2(
            c.SCREEN_W / 2 - c.SCREEN_W - 200, 
            c.SCREEN_H / 2
        )
        super().__init__(position, manager)
        self._position = self.position.copy()
        self.scroll = pygame.Vector2()

        self.interface.add_label(
            font=AssetManager.fonts['font_24'],
            text='SETTINGS HELL YEAH',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': self._position.x,
                'top': 50
            }
        )
        anchors = {
            'right': self.rect.right,
            'centery': c.SCREEN_H / 2
        }
        self.interface.add_button(ToPlayMenuButton(self.manager.to_play_menu, anchors))

    def update(self, delta):
        super().update(delta)
        self.position = self._position + self.scroll

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == MOUSEWHEEL:
            self.scroll.y += -event.y * 25
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.manager.to_play_menu()


class LevelSelectionMenu(BaseSubMenu):
    def __init__(self, manager):
        position = pygame.Vector2(
            c.SCREEN_W / 2 + c.SCREEN_W + 200, 
            c.SCREEN_H / 2
        )
        super().__init__(position, manager)
        self._position = self.position.copy()
        self.scroll = pygame.Vector2()

        self.interface.add_label(
            font=AssetManager.fonts['font_24'],
            text='LEVEL SELECTION HELL YEAH',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': self._position.x,
                'top': 50
            }
        )
        anchors = {
            'left': self.rect.left,
            'centery': c.SCREEN_H / 2
        }
        self.interface.add_button(ToPlayMenuButton(self.manager.to_play_menu, anchors))

    def update(self, delta):
        super().update(delta)
        self.position = self._position + self.scroll

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == MOUSEWHEEL:
            self.scroll.y += -event.y * 25
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.manager.to_play_menu()