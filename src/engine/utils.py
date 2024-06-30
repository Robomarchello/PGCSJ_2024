from time import perf_counter
from typing import List, Tuple, Any
import pygame
from pygame.locals import KEYDOWN, K_d
from .constants import *
from .asset_manager import AssetManager

DEBUG_TEXT_OFFSET = 20


class Debug:
    points = []
    lines = []
    texts = []

    visible = True

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
            pygame.draw.line(screen, (255, 0, 0), line[0])
        
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
            if event.key == K_d:
                if cls.visible:
                    cls.visible = False
                else:
                    cls.visible = True 



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