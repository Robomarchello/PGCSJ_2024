import pygame
from pygame.locals import *
from src.engine.constants import SCREENSIZE, SCREEN_AREA
from src.engine.asset_manager import AssetManager
from .button import Button


class PlayButton(Button):
    def __init__(self, func):
        rect = pygame.Rect(
            0, 0,
            SCREENSIZE[0] * 0.4,
            SCREENSIZE[1] * 0.13,
        )
        rect.centerx = SCREEN_AREA.centerx
        rect.top = 250 - 50

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
            SCREENSIZE[1] * 0.13,
        )
        rect.centerx = SCREEN_AREA.centerx
        rect.top = 400 - 60

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
            SCREENSIZE[1] * 0.13,
        )
        rect.centerx = SCREEN_AREA.centerx
        rect.top = 550 - 70

        font = AssetManager.fonts['font_36']
        text = 'Settings'

        button_color = (105, 105, 105)
        hover_color = (0, 255, 0)
        text_color = (255, 255, 255)

        super().__init__(rect, font, text, text_color, button_color, hover_color, func)


class ExitButton(Button):
    def __init__(self, func):
        rect = pygame.Rect(
            0, 0,
            SCREENSIZE[0] * 0.4,
            SCREENSIZE[1] * 0.13,
        )
        rect.centerx = SCREEN_AREA.centerx
        rect.top = 700 - 80

        font = AssetManager.fonts['font_36']
        text = 'Exit'

        button_color = (105, 105, 105)
        hover_color = (255, 0, 0)
        text_color = (255, 0, 0)

        super().__init__(rect, font, text, text_color, button_color, hover_color, func)


class BackButton(Button):
    def __init__(self, func):
        rect = pygame.Rect(
            0, 0,
            SCREENSIZE[0] * 0.4,
            SCREENSIZE[1] * 0.15,
        )
        rect.centerx = SCREEN_AREA.centerx
        rect.bottom = 738

        font = AssetManager.fonts['font_36']
        text = 'back'

        button_color = (105, 105, 105)
        hover_color = (255, 0, 0)
        text_color = (255, 0, 0)

        super().__init__(rect, font, text, text_color, button_color, hover_color, func)


class LevelButton(Button):
    def __init__(self, level, position, func):
        rect = pygame.Rect(
            0, 0,
            SCREENSIZE[0] * 0.13,
            SCREENSIZE[0] * 0.1,
        )
        self.offset = 0
        rect.topleft = position

        font = AssetManager.fonts['font_36']

        button_color = (105, 105, 105)
        hover_color = (255, 0, 0)
        self.text_color = (0, 200, 0)
        self.locked_color = (200, 200, 200)

        self.level = level
        text = str(level)

        self.lock_img = AssetManager.images['lock'].convert()
        self.lock_img.set_colorkey((0, 0, 0))
        self.lock_rect = self.lock_img.get_rect()

        self.finished = False

        super().__init__(rect, font, text, self.text_color, button_color, hover_color, func)

    def update_offset(self, x_offset, y_offset):
        self.offset = y_offset
        self.offset_rect = self.rect.copy()
        self.offset_rect.x -= x_offset
        self.offset_rect.y -= y_offset

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.offset_rect.collidepoint(mouse_pos)

    def draw(self, surface):
        if self.hovered:
            pygame.draw.rect(surface, self.hover_color, self.offset_rect, width=5, border_radius=10)
        else:
            pygame.draw.rect(surface, self.btn_color, self.offset_rect, width=5, border_radius=10)

        # draw text
        if not self.finished:
            render = self.font.render(self.text, False, self.locked_color)
        else:
            render = self.font.render(self.text, False, self.text_color)

        rect = render.get_rect(center=self.offset_rect.center)

        surface.blit(render, rect.topleft)

        if not self.finished:
            self.lock_rect.center = self.offset_rect.center
            surface.blit(self.lock_img, self.lock_rect.topleft)

        if self.last_hover == False and self.hovered == True:
            self.hover_sound.play()

        self.last_hover = self.hovered

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.hovered and self.finished:
                    self.func(self.level)
                else:
                    self.func(None, True)



class ChangeVolButton(Button):
    def __init__(self, text, func):
        rect = pygame.Rect(
            0, 0,
            SCREENSIZE[0] * 0.4,
            SCREENSIZE[1] * 0.15,
        )
        rect.centerx = SCREEN_AREA.centerx
        rect.top = 250

        font = AssetManager.fonts['font_36']

        button_color = (105, 105, 105)
        hover_color = (0, 255, 0)
        text_color = (255, 255, 255)

        super().__init__(rect, font, text, text_color, button_color, hover_color, func)
