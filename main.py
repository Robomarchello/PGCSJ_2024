from src.engine.app import App
from src.states import Game, LoadAssets
import asyncio

if __name__ == '__main__':
    asyncio.run(App(LoadAssets(next_state=Game)).loop())