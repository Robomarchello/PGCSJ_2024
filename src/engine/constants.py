import pygame
from pathlib import Path

TITLE = 'Mediocre Game with Golf-Like Gameplay in Space!'
SCREENSIZE = SCREEN_W, SCREEN_H = (1024, 768)
SCREEN_AREA = pygame.Rect(0, 0, SCREEN_W, SCREEN_H)
FPS = 480

# to compencate small delta time values
SPEED_FACTOR = 60
GRAVITY_CONST = 60

ABS_DIR = str(Path.cwd()).replace('\\', '/')
ASSETS_PATH = 'src/assets/'
LEVELS_PATH = 'src/levels/'
FONTS_JSON_PATH = 'src/assets/other/fonts.json'
SAVE_PATH = 'src/assets/other/save.json'

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

VOLUME = 0.6

# Debug font path and size
DEBUG_FONT = ABS_DIR + '/src/assets/other/debug_font.ttf'
DEBUG_SIZE = 16
DEBUG_TEXT_OFFSET = 22
DEBUG_VEL = 5

PLATFORM = __import__("sys").platform