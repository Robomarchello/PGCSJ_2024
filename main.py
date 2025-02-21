import asyncio
from src.engine.constants import ASSETS_PATH
from src.engine.asset_manager import AssetManager
AssetManager.load_assets(ASSETS_PATH)
from src.engine.app import App
from src.states import Game, Menu

if __name__ == '__main__':
    
    asyncio.run(App(Game()).loop())

