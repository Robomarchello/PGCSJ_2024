import pygame
from src.engine.app import App
from src.states import MyState

if __name__ == '__main__':
    App(MyState()).loop()
