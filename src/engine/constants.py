import pygame
from pathlib import Path


TITLE = 'Game Title'
SCREENSIZE = SCREEN_W, SCREEN_H = (960, 768)
SCREEN_AREA = pygame.Rect(0, 0, SCREEN_W, SCREEN_H)
FPS = 480

# to compencate small delta time values
SPEED_FACTOR = 60
GRAVITY_CONST = 40

ABS_DIR = str(Path.cwd()).replace('\\', '/')
ASSETS_PATH = 'src/assets/'

BLACK = (0, 0, 0)

# Debug font path and size
DEBUG_FONT = ABS_DIR + '/src/assets/other/font.ttf'
DEBUG_SIZE = 16
DEBUG_VEL = 5