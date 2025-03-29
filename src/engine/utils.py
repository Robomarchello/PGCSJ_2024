import random
import math
import json
from time import perf_counter
from typing import List, Tuple, Any
import pygame
from pygame.locals import KEYDOWN, K_g
from src.engine.constants import *
from src.engine.asset_manager import AssetManager

def clamp(value, min_, max_):
    return min(max(min_, value), max_)

def get_shake(strength):
    shake = (
        random.uniform(-strength, strength),
        random.uniform(-strength, strength)
    )
    return shake

def load_spritesheet(image, sprite_size) -> List[pygame.Surface]:
    image_size = image.get_size()

    sprites = []
    sprite = pygame.Surface(sprite_size)
    for y in range(0, image_size[1], sprite_size[1]):
        for x in range(0, image_size[0], sprite_size[0]):
            sprite.fill((0, 0, 0))
            sprite.blit(image, (-x, -y))
            sprites.append(sprite.copy())

    return sprites

def json_spritesheet(image, file_path):
    sprites = []
    with open(file_path, 'r') as file:
        rects = json.load(file)

    for rect in rects:
        surface = pygame.Surface(rect.size)
        surface.blit(image, (-rect.x, -rect.y))

        sprites.append(surface.copy())

    return sprites

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

            offset += render.height + DEBUG_TEXT_SPACING

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