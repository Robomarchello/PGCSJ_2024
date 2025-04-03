from src.engine.app import App
from src.states import Menu, Game, LoadState
import asyncio

if __name__ == '__main__':
    asyncio.run(App(LoadState(next_state=Menu)).loop())