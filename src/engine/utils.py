from time import perf_counter
from typing import List, Tuple, Any
import json
import math
import pygame
import random
from pygame.locals import KEYDOWN, K_g
from .constants import *
from .asset_manager import AssetManager


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


def get_shake(strength):
    shake = (
        random.uniform(-strength, strength),
        random.uniform(-strength, strength)
    )
    return shake

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

    if length - radius1 - radius2 < 0:
        return True
    else:
        return False
    

def draw_dashed_line(surface, pos1, pos2, dash_len, blank_len, color, width=1):
    diff = pygame.Vector2(
        pos2[0] - pos1[0],
        pos2[1] - pos1[1]
    )
    direction = diff.normalize()
    length = diff.length()
    count = length // (dash_len + blank_len)

    dash_vec = direction * dash_len
    blank_vec = direction * blank_len

    last_pos = pygame.Vector2(pos1)
    for _ in range(int(count)):
        other_pos = last_pos + dash_vec

        pygame.draw.line(surface, color, last_pos, other_pos, width)

        last_pos += dash_vec + blank_vec

    pygame.draw.line(surface, color, last_pos, pos2, width)


class Debug:
    points = []
    lines = []
    texts = []

    konami = [1073741906, 1073741906, 1073741905, 1073741905, 1073741904, 1073741903, 1073741904, 1073741903, 98, 97]
    keys_pressed = []

    visible = False

    font: pygame.Font = AssetManager.load_font(DEBUG_FONT, DEBUG_SIZE)

    @classmethod
    def draw_queue(cls, screen):
        if not cls.visible:
            cls.points = []
            cls.lines = []
            cls.texts = []
        
        for point in cls.points:
            pygame.draw.circle(screen, (255, 0, 0), point, 4)

        for line in cls.lines:
            pygame.draw.line(screen, (255, 0, 0), line[0], line[1], 2)
        
        offset = 0
        for text in cls.texts:
            render = cls.font.render(text, False, (255, 0, 0))
            position = (10, offset * DEBUG_TEXT_OFFSET + 10)
            screen.blit(render, position)

            offset += 1

        cls.points = []
        cls.lines = []
        cls.texts = []

    @classmethod
    def add_point(cls, position: Tuple[int, int]) -> None:
        cls.points.append(position)

    @classmethod
    def add_vector(cls, position: Tuple[int, int], vector) -> None:
        position2 = (
            position[0] + vector[0],
            position[1] + vector[1])
        
        cls.lines.append((position, position2))

    @classmethod
    def add_line(cls, 
                position1: Tuple[int, int], 
                position2: Tuple[int, int]
                ) -> None:
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
            
            if cls.keys_pressed == cls.konami:
                if cls.visible:
                    cls.visible = False
                else:
                    cls.visible = True 