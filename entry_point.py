import pygame
from src.engine.app import App
from src.states import Game

if __name__ == '__main__':
    App(Game()).loop()