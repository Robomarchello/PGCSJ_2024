from typing import List
import pygame
from src.engine.base import Base
from src.engine.gui.ui_image import UIImage
from .button import BaseButton
from .label import Label
from .slider import Slider


class GUInterface(Base):
    def __init__(self):
        self.buttons: List[BaseButton] = []
        self.labels: List[Label] = []
        self.sliders: List[Slider] = []
        self.images: List[UIImage] = []

        self.offset = pygame.Vector2()

    def draw(self, surface):
        for image in self.images:
            image.draw(surface)
        for button in self.buttons:
            button.draw(surface)
        for label in self.labels:
            label.draw(surface)
        for slider in self.sliders:
            slider.draw(surface)

    def update(self, delta):
        for image in self.images:
            image.update(delta)
        for button in self.buttons:
            button.update(delta)
        for label in self.labels:
            label.update(delta)
        for slider in self.sliders:
            slider.update(delta)

    def handle_event(self, event):
        for button in self.buttons:
            button.handle_event(event)
        for label in self.labels:
            label.handle_event(event)
        for slider in self.sliders:
            slider.handle_event(event)
        # UIImage is passive, no event handling needed

    def set_offset(self, x, y):
        """Shift positions of all elements by offset."""
        self.offset.update(x, y)

        for image in self.images:
            image.set_offset(x, y)
        for button in self.buttons:
            button.set_offset(x, y)
        for label in self.labels:
            label.set_offset(x, y)
        for slider in self.sliders:
            slider.set_offset(x, y)

    def update_anchors(self):
        for image in self.images:
            image.rect_to_anchors()
        for button in self.buttons:
            button.rect_to_anchors()
        for label in self.labels:
            label.rect_to_anchors()
        for slider in self.sliders:
            slider.rect_to_anchors()

    def set_scale(self, scale):
        for button in self.buttons:
            button.scale = scale
        for label in self.labels:
            label.scale = scale
        # Sliders don't have explicit scale handling yet, so skip for now

    def set_img_scale(self, scale):
        for image in self.images:
            image.scale = scale

    def set_enabled(self, enabled: bool):
        for image in self.images:
            image.enabled = enabled
        for button in self.buttons:
            button.enabled = enabled
        for label in self.labels:
            label.enabled = enabled
        for slider in self.sliders:
            slider.enabled = enabled

    def add_button(self, button: BaseButton):
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

    def add_image(self, image: UIImage):
        self.images.append(image)

    def add_slider(
        self,
        length: int,
        start_value: float,
        value_range: tuple,
        anchors: dict = {},
        step: float = 0.01,
        on_change=None
    ):
        slider = Slider(length, start_value, value_range, anchors, step, on_change)
        self.sliders.append(slider)
        return slider