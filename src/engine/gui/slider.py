import pygame
from .ui_element import UIElement


class Slider(UIElement):
    def __init__(
        self,
        length,
        start_value,
        value_range,
        anchors={'topleft': (0, 0)},
        step=0.01,
        on_change=None
    ):
        rect = pygame.Rect(0, 0, length, 40)
        self.anchors = anchors
        super().__init__(rect)
        self.rect_to_anchors()

        self.track_rect = pygame.Rect(0, 0, length, 6)
        self.track_rect.center = self.rect.center

        self.value_range = value_range
        self.step = step
        self.on_change = on_change

        self.dragging = False

        self.value = self._snap_value(start_value)
        self.indicator_rect = pygame.Rect(0, 0, 20, 40)
        self._update_indicator_pos()

    def _snap_value(self, value):
        """Snap value to nearest step."""
        v_min, v_max = self.value_range
        value = max(min(value, v_max), v_min)
        steps = round((value - v_min) / self.step)
        return v_min + steps * self.step

    def _update_indicator_pos(self):
        """Update indicator x position based on current value."""
        rel = (self.value - self.value_range[0]) / (self.value_range[1] - self.value_range[0])
        self.indicator_rect.centerx = self.track_rect.left + rel * self.track_rect.width
        self.indicator_rect.centery = self.track_rect.centery

    def _set_value_from_mouse(self, mouse_x):
        """Set slider value based on mouse x position."""
        rel = (mouse_x - self.track_rect.left) / self.track_rect.width
        rel = max(0.0, min(1.0, rel))  # clamp
        value = self.value_range[0] + rel * (self.value_range[1] - self.value_range[0])
        snapped_value = self._snap_value(value)

        if snapped_value != self.value:
            self.value = snapped_value
            self._update_indicator_pos()
            if self.on_change:
                self.on_change(self.value)

    def draw(self, surface):
        # Track
        pygame.draw.rect(surface, (220, 220, 220), self.track_rect)
        # Indicator
        pygame.draw.rect(surface, (220, 220, 220), self.indicator_rect)

    def update(self, delta):
        self._get_offset_rect()
        self.track_rect.center = self.rect.center
        if not self.dragging:
            self._update_indicator_pos()

    def handle_event(self, event):
        if not self.enabled:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.indicator_rect.collidepoint(event.pos):
                self.dragging = True
            elif self.track_rect.collidepoint(event.pos):
                self.dragging = True
                self._set_value_from_mouse(event.pos[0])

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self._set_value_from_mouse(event.pos[0])