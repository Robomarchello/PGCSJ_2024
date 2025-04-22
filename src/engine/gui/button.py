from typing import Callable
import pygame
from pygame.locals import MOUSEBUTTONDOWN
from src.engine.asset_manager import AssetManager
from .ui_element import UIElement


class Button(UIElement):
    def __init__(
        self, 
        rect: pygame.Rect, 
        font: pygame.Font, 
        text: str, 
        text_color: pygame.Color, 
        btn_color: pygame.Color, 
        hover_color: pygame.Color, 
        func: Callable,
        *args
    ):
        super().__init__(rect)

        self.font = font
        self.text = text

        self.btn_color = btn_color
        self.hover_color = hover_color
        self.text_color  = text_color
        
        self.func = func
        self.args = args

        self.hovered = False
        self.last_hover = False

        self.hover_sound = AssetManager.sounds['hover_sound']

    def draw(self, surface):
        self._draw_base(surface)
        self._draw_text(surface)

    def _draw_base(self, surface):
        color = self.hover_color if self.hovered else self.btn_color
        pygame.draw.rect(surface, color, self.rect, width=5, border_radius=10)

    def _draw_text(self, surface):
        render = self.font.render(self.text, False, self.text_color)
        rect = render.get_rect(center=self.rect.center)

        surface.blit(render, rect.topleft)

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
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.hovered:
                    self.func(*self.args)