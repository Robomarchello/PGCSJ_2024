from src.engine.app import App
from src.states import Game, Menu
import asyncio
from src.engine.constants import ASSETS_PATH
from src.engine.asset_manager import AssetManager

if __name__ == '__main__':
    AssetManager.load_assets(ASSETS_PATH)

    asyncio.run(App(Game()).loop())

