import pygame
from pygame.locals import MOUSEBUTTONDOWN


class Button:
    def __init__(
        self, 
        rect, 
        font, 
        text, 
        text_color, 
        btn_color, 
        func,
        texture=None
    ):
        self.rect = rect
        
        self.font = font
        self.text = text

        self.btn_color = btn_color
        self.text_color  = text_color
        self.func = func

        self.hovered = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.btn_color, self.rect, width=5)

        # draw text
        render = self.font.render(self.text, False, self.text_color)
        rect = render.get_rect(center=self.rect.center)

        surface.blit(render, rect.topleft)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.hovered:
                    self.func()
