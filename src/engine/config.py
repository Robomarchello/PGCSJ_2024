import pygame
from pathlib import Path

# constants
TITLE = 'Mediocre Game with Golf-Like Gameplay in Space!'
FPS = 480
SPEED_FACTOR = 60
GRAVITY_CONST = 60

# configuration
PLATFORM = __import__("sys").platform

BASE_SCREENSIZE = (1365, 768)
SCREENSIZE = SCREEN_W, SCREEN_H = (1365, 768)
SCREEN_AREA = pygame.Rect(0, 0, SCREEN_W, SCREEN_H)

VOLUME = 0.6

ABS_DIR = str(Path.cwd()).replace('\\', '/')
ASSETS_PATH = 'src/assets/'
LEVELS_PATH = 'src/levels/'
FONTS_JSON_PATH = 'src/assets/other/fonts.json'
SAVE_PATH = 'src/assets/other/save.json'

# Debug font path and size
DEBUG_FONT = ABS_DIR + '/src/assets/other/debug_font.ttf'
DEBUG_SIZE = 16
DEBUG_TEXT_SPACING = 5
DEBUG_VEL = 5
DEBUG_BUTTON = True