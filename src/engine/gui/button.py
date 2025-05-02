from typing import Callable
import pygame
from pygame.locals import MOUSEBUTTONDOWN
from src.engine.asset_manager import AssetManager
from .ui_element import UIElement
from .nine_slice import NineSlice


class BaseButton(UIElement):
    def __init__(
        self,
        rect: pygame.Rect,
        base: NineSlice,
        base_hover: NineSlice,
        func: Callable,
        func_args=(),
        anchors: dict = {},
        # is toggle
    ):
        super().__init__(rect)
        self.base = base
        self.base_hover = base_hover
        self.func = func
        self.func_args = func_args
        self.anchors = anchors
        self.rect_to_anchors()

        if self.base is not None:
            self.base_surf = self.base.as_surface(rect)
            self.base_hover_surf = self.base_hover.as_surface(rect)

        self.hovered = False
        self.last_hover = False
        self.hover_sound = AssetManager.sounds['hover_sound']

        self.scale = 1.0

    def _draw_base(self, surface):
        if self.base is not None:
            if self.hovered:
                surface.blit(self.base_hover_surf, self.rect.topleft)
            else:
                surface.blit(self.base_surf, self.rect.topleft)

    def update(self, delta):
        self._get_offset_rect()

        if not self.enabled:
            return

        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        if not self.last_hover and self.hovered:
            self.hover_sound.play()

        self.last_hover = self.hovered

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            self.func(*self.func_args)


class TextButton(BaseButton):
    def __init__(
        self,
        rect: pygame.Rect,
        base: NineSlice,
        base_hover: NineSlice,
        font: pygame.Font,
        text: str,
        text_color: pygame.Color,
        func: Callable,
        func_args=(),
        anchors: dict = {},
    ):
        super().__init__(rect, base, base_hover, func, func_args, anchors)
        self.font = font
        self.text = text
        self.text_color = text_color

    def draw(self, surface):
        self._draw_base(surface)
        self._draw_text(surface)

    def _draw_text(self, surface):
        render = self.font.render(self.text, False, self.text_color)
        if self.scale != 1.0:
            render = pygame.transform.scale_by(render, self.scale)
        rect = render.get_rect(center=self.rect.center)

        surface.blit(render, rect.topleft)


class IconButton(BaseButton):
    def __init__(
        self,
        rect: pygame.Rect,
        base: NineSlice,
        base_hover: NineSlice,
        icon: pygame.Surface,
        func: Callable,
        func_args=(),
        anchors: dict = {},
    ):
        super().__init__(rect, base, base_hover, func, func_args, anchors)
        self.icon = icon
        self.icon_rect = self.icon.get_rect(center=self.rect.center)

    def draw(self, surface):
        self._draw_base(surface)
        self._draw_icon(surface)

    def _draw_icon(self, surface):
        surface.blit(self.icon, self.icon_rect.topleft)

    def _get_offset_rect(self):
        super()._get_offset_rect()
        self.icon_rect = self.icon.get_rect(center=self.rect.center)
