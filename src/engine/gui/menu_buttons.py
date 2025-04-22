import pygame
from pygame.locals import *
import src.engine.config as c
from src.engine.asset_manager import AssetManager
from .button import Button, IconButton
from .nine_slice import NineSlice


# --- main menu ---
class ToSettingsButton(IconButton):
    def __init__(self, func):
        rect = pygame.Rect(0, 0, 80, c.SCREEN_H / 3)

        self.anchors = {
            'left': -10,
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
            'right': c.SCREEN_W + 10,
            'centery': c.SCREEN_H / 2
        }

        icon = AssetManager.images['levels_icon']
        base_slice = NineSlice(AssetManager.images['button_slice'])
        base_hovered_slice = NineSlice(AssetManager.images['button_slice_hover'])

        super().__init__(rect, base_slice, base_hovered_slice, icon, func, (), self.anchors)


class BackButton(Button):
    def __init__(self, func):
        rect = pygame.Rect(
            0, 
            0,
            SCREENSIZE[0] * 0.4,
            SCREENSIZE[1] * 0.13,
        )
        rect.centerx = SCREEN_AREA.centerx

        font = AssetManager.fonts['font_36']
        text = 'Back'

        button_color = (105, 105, 105)
        hover_color = (255, 0, 0)
        text_color = (255, 0, 0)

        super().__init__(rect, font, text, text_color, button_color, hover_color, func)

# --- level selection menu
class LevelButton(Button):
    def __init__(self, level, position, func):
        rect = pygame.Rect(
            *position,
            SCREENSIZE[0] * 0.13,
            SCREENSIZE[1] * 0.13,
        )
        font = AssetManager.fonts['font_36']

        button_color = (105, 105, 105)
        hover_color = (255, 0, 0)
        self.unlocked_color = (0, 200, 0)
        self.locked_color = (200, 200, 200)
        self.text_color = self.unlocked_color

        self.level = level
        text = str(level)

        super().__init__(rect, font, text, self.text_color, button_color, hover_color, func)

        self.lock_img = AssetManager.images['lock'].convert_alpha()
        self.lock_rect = self.lock_img.get_rect()

        self.completed = False

    def _draw_base(self, surface):
        super()._draw_base(surface)

        if not self.completed:
            self.lock_rect.center = self.rect.center
            surface.blit(self.lock_img, self.lock_rect.topleft)

    def _draw_text(self, surface):
        self.text_color = self.unlocked_color if self.completed else self.locked_color
        super()._draw_text(surface)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.hovered:
                    if self.completed:
                        self.func(self.level)
                    else:
                        self.func(None, True)


# --- settings menu ---
class ChangeVolButton(Button):
    def __init__(self, position, text, func, change_value):
        rect = pygame.Rect(
            *position,
            100,
            100,
        )
        self.change_value = change_value

        font = AssetManager.fonts['font_36']

        button_color = (105, 105, 105)
        hover_color = (0, 255, 0)
        text_color = (255, 255, 255)

        super().__init__(rect, font, text, text_color, button_color, hover_color, func, change_value)