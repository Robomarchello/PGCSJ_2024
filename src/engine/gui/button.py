import pygame
from pygame.locals import MOUSEBUTTONDOWN
from src.engine.asset_manager import AssetManager


class Button:
    def __init__(
        self, 
        rect, 
        font, 
        text, 
        text_color, 
        btn_color, 
        hover_color, 
        func,
        texture=None
    ):
        self.rect = rect
        
        self.font = font
        self.text = text

        self.btn_color = btn_color
        self.hover_color = hover_color
        self.text_color  = text_color
        self.func = func

        self.hovered = False
        self.hover_sound = AssetManager.sounds['hover_sound']
        self.last_hover = self.hovered

    def draw(self, surface):
        if self.hovered:
            pygame.draw.rect(surface, self.hover_color, self.rect, width=5, border_radius=10)
        else:
            pygame.draw.rect(surface, self.btn_color, self.rect, width=5, border_radius=10)

        # draw text
        render = self.font.render(self.text, False, self.text_color)
        rect = render.get_rect(center=self.rect.center)

        surface.blit(render, rect.topleft)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        if self.last_hover == False and self.hovered == True:
            self.hover_sound.play()

        self.last_hover = self.hovered

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.hovered:
                    self.func()
