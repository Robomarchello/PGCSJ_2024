import random
import math
import json
from time import perf_counter
from typing import List, Tuple, Any
import pygame
from pygame.locals import KEYDOWN, K_g
from src.engine.config import *
from src.engine.asset_manager import AssetManager

def clamp(value, min_, max_):
    return min(max(min_, value), max_)

def get_shake(strength):
    shake = (
        random.uniform(-strength, strength),
        random.uniform(-strength, strength)
    )
    return shake

def collide_circles(position1, radius1, position2, radius2):
    difference = (
        position2[0] - position1[0],
        position2[1] - position1[1]
    )
    length = math.sqrt(difference[0] ** 2 + difference[1] ** 2)

    if length < radius1 + radius2:
        return True
    else:
        return False

def draw_dashed_line(surface, start, end, dash_len, blank_len, color, width=1):
    diff = pygame.Vector2(
        end[0] - start[0],
        end[1] - start[1]
    )
    direction = diff.normalize()
    count = diff.length() // (dash_len + blank_len)

    dash_vec = direction * dash_len
    blank_vec = direction * blank_len

    last_pos = pygame.Vector2(start)
    for _ in range(int(count)):
        other_pos = last_pos + dash_vec
        pygame.draw.line(surface, color, last_pos, other_pos, width)

        last_pos += dash_vec + blank_vec

    pygame.draw.line(surface, color, last_pos, end, width)

def draw_dashed_rect(surface, rect, dash_len, blank_len, color, width=1):
    corners = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]
    for start, end in zip(corners, corners[1:] + [corners[0]]):
        draw_dashed_line(surface, start, end, dash_len, blank_len, color, width)

def to_range(value):
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, list):
        return value
    return [value, value]

def ellipse_random(rect):
    angle = random.uniform(0, 6.28)
    length_w = random.uniform(0, rect.width / 2)
    length_h = random.uniform(0, rect.height / 2)
    position = (
        math.cos(angle) * length_w + rect.centerx,
        -math.sin(angle) * length_h + rect.centery
    )

    return position

def rect_random(rect):
    position = (
        random.randint(0, rect.width) + rect.x,
        random.randint(0, rect.height) + rect.y
    )

    return position

def calculate_gradient(colors, intervals, steps) -> List:
    '''
    Something like cozyfractal have done https://github.com/ddorn
    Precalculate colors of a gradient
    '''
    assert len(colors) >= 2

    colors = colors[::-1] # quick but spaghetti fix

    if intervals[0] != 0.0 or intervals[-1] != 1.0:
        raise ValueError("Intervals must start at 0.0 and end at 1.0")

    colors = [pygame.Color(color) for color in colors]
    #intervals = sorted(intervals)

    gradient = []
    color1_i = 0
    color2_i = 1
    interval_size = intervals[color2_i] - intervals[color1_i]
    for step in range(steps):
        full_progress = step / steps
        lerp_progress = (full_progress - intervals[color1_i]) / interval_size
        lerp_progress = clamp(lerp_progress, 0.0, 1.0)

        crnt_color = colors[color1_i].lerp(colors[color2_i], lerp_progress)
        gradient.append(crnt_color)

        if full_progress > intervals[color2_i]:
            color1_i += 1
            color2_i += 1

    return gradient


class Debug:
    points = []
    lines = []
    texts = []

    konami = [1073741906, 1073741906, 1073741905, 1073741905, 1073741904, 1073741903, 1073741904, 1073741903, 98, 97]
    keys_pressed = []

    enabled = False

    font: pygame.Font = AssetManager.load_font(DEBUG_FONT, DEBUG_SIZE)

    @classmethod
    def draw_queue(cls, screen):
        if not cls.enabled:
            cls.points = []
            cls.lines = []
            cls.texts = []
        
        for point in cls.points:
            pygame.draw.circle(screen, (255, 0, 0), point, 4)

        for line in cls.lines:
            pygame.draw.line(screen, (255, 0, 0), line[0], line[1], 2)
        
        offset = 10
        for text in cls.texts:
            render = cls.font.render(text, False, (255, 0, 0))
            position = (10, offset)
            screen.blit(render, position)

            offset += render.get_height() + DEBUG_TEXT_SPACING

        cls.points = []
        cls.lines = []
        cls.texts = []

    @classmethod
    def add_point(cls, position: Tuple[int, int]) -> None:
        cls.points.append(position)

    @classmethod
    def add_vector(cls, start: Tuple[int, int], vector) -> None:
        end = (
            start[0] + vector[0],
            start[1] + vector[1])
        
        cls.lines.append((start, end))

    @classmethod
    def add_line(cls, position1: Tuple[int, int], position2: Tuple[int, int]) -> None:
        cls.lines.append((position1, position2))

    @classmethod
    def add_text(cls, text: Any) -> None:
        cls.texts.append(str(text))

    @classmethod
    def time_func(cls, function, *args):
        start = perf_counter()
        output = function(*args)
        end = perf_counter()
        
        cls.texts.append(
            f'{function.__name__}: {round(end - start, 2)} s'
        )

        return output

    @classmethod
    def handle_event(cls, event):
        if event.type == KEYDOWN:
            cls.keys_pressed.append(event.key)
            if len(cls.keys_pressed) > len(cls.konami):
                cls.keys_pressed.pop(0)
            
            if cls.keys_pressed == cls.konami or event.key == K_g:
                cls.enabled = not cls.enabled