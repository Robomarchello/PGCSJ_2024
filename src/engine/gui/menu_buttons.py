import pygame
from src.engine.constants import SCREENSIZE, SCREEN_AREA
from src.engine.asset_manager import AssetManager
from .button import Button


class PlayButton(Button):
    def __init__(self, func):
        rect = pygame.Rect(
            0, 0,
            SCREENSIZE[0] * 0.4,
            SCREENSIZE[1] * 0.15,
        )
        rect.centerx = SCREEN_AREA.centerx
        rect.top = 250

        font = AssetManager.fonts['font_36']
        text = 'Play'

        button_color = (105, 105, 105)
        hover_color = (0, 255, 0)
        text_color = (255, 255, 255)

        super().__init__(rect, font, text, text_color, button_color, hover_color, func)


class LevelSelectionButton(Button):
    def __init__(self, func):
        rect = pygame.Rect(
            0, 0,
            SCREENSIZE[0] * 0.4,
            SCREENSIZE[1] * 0.15,
        )
        rect.centerx = SCREEN_AREA.centerx
        rect.top = 400

        font = AssetManager.fonts['font_36']
        text = 'Level Selection'

        button_color = (105, 105, 105)
        hover_color = (0, 255, 0)
        text_color = (255, 255, 255)

        super().__init__(rect, font, text, text_color, button_color, hover_color, func)


class SettingsButton(Button):
    def __init__(self, func):
        rect = pygame.Rect(
            0, 0,
            SCREENSIZE[0] * 0.4,
            SCREENSIZE[1] * 0.15,
        )
        rect.centerx = SCREEN_AREA.centerx
        rect.top = 550

        font = AssetManager.fonts['font_36']
        text = 'Settings'

        button_color = (105, 105, 105)
        hover_color = (0, 255, 0)
        text_color = (255, 255, 255)

        super().__init__(rect, font, text, text_color, button_color, hover_color, func)


class ExitButton(Button):
    def __init__(self, func):
        rect = pygame.Rect(
            25, 25,
            100,
            100,
        )

        font = AssetManager.fonts['font_36']
        text = ':('

        button_color = (105, 105, 105)
        hover_color = (255, 0, 0)
        text_color = (255, 0, 0)

        super().__init__(rect, font, text, text_color, button_color, hover_color, func)
