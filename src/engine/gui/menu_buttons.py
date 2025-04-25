import pygame
from pygame.locals import *
import src.engine.config as c
from src.engine.asset_manager import AssetManager
from .button import TextButton, IconButton
from .nine_slice import NineSlice


# --- main menu ---
class ToSettingsButton(IconButton):
    def __init__(self, func):
        rect = pygame.Rect(0, 0, 80, c.SCREEN_H / 3)

        self.anchors = {
            'left': 0,
            'centery': c.SCREEN_H / 2
        }

        icon = AssetManager.images['settings_icon']
        base_slice = NineSlice(AssetManager.images['button_slice'])
        base_hovered_slice = NineSlice(AssetManager.images['button_slice_hover'])

        super().__init__(rect, base_slice, base_hovered_slice, icon, func, (), self.anchors)


class ToPlayMenuButton(IconButton):
    def __init__(self, func, anchors):
        rect = pygame.Rect(0, 0, 80, c.SCREEN_H / 3)

        self.anchors = anchors

        icon = AssetManager.images['play_icon']
        base_slice = NineSlice(AssetManager.images['button_slice'])
        base_hovered_slice = NineSlice(AssetManager.images['button_slice_hover'])

        super().__init__(rect, base_slice, base_hovered_slice, icon, func, (), self.anchors)


class ToLevelSelectionButton(IconButton):
    def __init__(self, func):
        rect = pygame.Rect(0, 0, 80, c.SCREEN_H / 3)

        self.anchors = {
            'right': c.SCREEN_W,
            'centery': c.SCREEN_H / 2
        }

        icon = AssetManager.images['levels_icon']
        base_slice = NineSlice(AssetManager.images['button_slice'])
        base_hovered_slice = NineSlice(AssetManager.images['button_slice_hover'])

        super().__init__(rect, base_slice, base_hovered_slice, icon, func, (), self.anchors)


class FullscreenButton(IconButton):
    def __init__(self, func, anchors):
        rect = pygame.Rect(0, 0, 80, c.SCREEN_H / 3)

        self.anchors = anchors

        icon = AssetManager.images['play_icon']
        base_slice = NineSlice(AssetManager.images['button_slice'])
        base_hovered_slice = NineSlice(AssetManager.images['button_slice_hover'])

        super().__init__(rect, base_slice, base_hovered_slice, icon, func, (), self.anchors)


class NewLevelButton(TextButton):
    def __init__(self, level, position, func):
        rect = pygame.Rect(
            *position,
            c.SCREENSIZE[0] * 0.13,
            c.SCREENSIZE[1] * 0.13,
        )
        font = AssetManager.fonts['font_42']
        
        self.unlocked_color = (0, 200, 0)
        self.locked_color = (200, 200, 200)
        self.text_color = self.unlocked_color

        self.level = level
        text = str(level)

        border_slice = NineSlice(AssetManager.images['button_slice_border'])
        self.border_slice = border_slice.as_surface(rect)
        self.border_locked = NineSlice(AssetManager.images['border_locked']).as_surface(rect)
        self.border_completed = NineSlice(AssetManager.images['border_allowed']).as_surface(rect)

        # rect, base, base_hover, font, text, text_color, func, func_args, anchors
        super().__init__(rect, border_slice, border_slice, font, text, self.text_color, func)

        self.lock_img = AssetManager.images['lock'].convert_alpha()
        self.lock_rect = self.lock_img.get_rect()

        self.completed = False

    def draw(self, surface):
        self._draw_base(surface)

        if not self.completed:
            self.lock_rect.center = self.rect.center
            surface.blit(self.lock_img, self.lock_rect.topleft)
        else:
            self._draw_text(surface)

    def _draw_base(self, surface):
        if not self.hovered:
            surface.blit(self.border_slice, self.rect.topleft)
        else:
            if self.completed:
                surface.blit(self.border_completed, self.rect.topleft)
            else:
                surface.blit(self.border_locked, self.rect.topleft)

    def _draw_text(self, surface):
        self.text_color = self.unlocked_color if self.completed else self.locked_color
        super()._draw_text(surface)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.hovered:
                    self.func(self.level, self.completed)