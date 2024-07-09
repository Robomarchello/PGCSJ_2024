from src.engine.app import App
from src.states import Game, Menu

if __name__ == '__main__':
    App(Game()).loop()
