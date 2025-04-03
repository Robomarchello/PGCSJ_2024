from typing import List
import pygame
from src.engine.base import Base
from .button import Button
from .label import Label


class GUInterface(Base):
    def __init__(self):
        self.buttons: List[Button] = []
        self.labels: List[Label] = []

        # All ui elements inherit element class. Could to that
        # self.elements = [] 

    def draw(self, surface):
        for button in self.buttons:
            button.draw(surface)

        for label in self.labels:
            label.draw(surface)

    def update(self, delta):
        for button in self.buttons:
            button.update(delta)

        for label in self.labels:
            label.update(delta)

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)

        for label in self.labels:
            label.handle_event(event)

    def set_offset_all(self, x, y):
        for button in self.buttons:
            button.set_offset(x, y)

        for label in self.labels:
            label.set_offset(x, y)

    def add_button(self, button: Button):
        self.buttons.append(button)

    def add_label(
            self,
            font: pygame.Font,
            text: str,
            color: pygame.Color,
            antialias: bool = False,
            anchors: dict = {}    
        ):
        label = Label(font, text, color, antialias, anchors)
        self.labels.append(label)
        return label