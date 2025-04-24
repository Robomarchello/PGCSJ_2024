import pygame
from pygame.locals import *
from src.engine.base import Base
from src.engine.gui import GUInterface, TextButton
from src.engine.asset_manager import AssetManager
from src.engine.gui import NineSlice
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

        self.clickable_area = pygame.Rect(0, 0, c.SCREEN_W * 0.8, c.SCREEN_H)
        self.clickable_area.center = self.position

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

    def update(self, delta):
        super().update(delta)
        self._update_clickable_area()
    
    def _update_clickable_area(self):
        self.clickable_area.center = self.position + self.interface.offset

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                raise SystemExit
            else:
                self.manager.to_game()

        if event.type == MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            if self.clickable_area.collidepoint(mp):
                self.manager.to_game()


class SettingsMenu(BaseSubMenu):
    def __init__(self, manager):
        position = pygame.Vector2(
            c.SCREEN_W / 2 - c.SCREEN_W - 200, 
            c.SCREEN_H / 2
        )
        super().__init__(position, manager)

        self.ui_body = pygame.Rect(0, 0, c.SCREEN_W * 0.7, c.SCREEN_H * 0.8)
        self._update_ui_body()
        self.body_slice = NineSlice(AssetManager.images['body_slice'])
        self.body_slice_surf = self.body_slice.as_surface(self.ui_body)
        
        # title
        self.interface.add_label(
            font=AssetManager.fonts['font_48'],
            text='Settings',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'centerx': self.position.x,
                'top': 50 * self.reference_scale
            }
        )
        # Back to play menu button
        to_play_button = ToPlayMenuButton(
            func=self.manager.to_play_menu, 
            anchors= {'right': self.rect.right, 'centery': c.SCREEN_H / 2}
        )
        self.interface.add_button(to_play_button)

        padding_left = 50 * self.reference_scale
        padding_top = 40 * self.reference_scale
        # fullscreen option
        self.interface.add_label(
            font=AssetManager.fonts['font_42'],
            text='Fullscreen',
            color=pygame.Color('white'),
            antialias=False,
            anchors={
                'left': self.ui_body.left + padding_left,
                'top': self.ui_body.top + padding_top
            }
        )
        fullscreen_button = None

    def draw(self, surface):
        surface.blit(self.body_slice_surf, self.ui_body.topleft)
        super().draw(surface)
        # pygame.draw.rect(surface, (255, 0, 0), self.ui_body, width=1)

    def update(self, delta):
        self._update_ui_body()
        super().update(delta)

    def _update_ui_body(self):
        self.ui_body.bottom = self.rect.bottom - 20 * self.reference_scale + self.interface.offset.y
        self.ui_body.centerx = self.position.x + self.interface.offset.x

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.manager.to_play_menu()