import os
import json
from pathlib import Path
from .constants import SAVE_PATH, LEVELS_PATH, PLATFORM


class SaveManager:
    data = {
        'levels_completed': []
    }

    if PLATFORM == "emscripten":
        from platform import window

    @classmethod
    def get_save(cls):
        '''Retrieve or initialize game save data'''
        if cls._save_exists():
            cls._load_data()
        else:
            cls._initialize_save()
            cls.save_data()

    @classmethod
    def _save_exists(cls):
        if PLATFORM == 'emscripten':
            return cls.window.localStorage.getItem('game_data') is not None
        return Path(SAVE_PATH).is_file()

    @classmethod
    def _initialize_save(cls):
        level_count = cls._get_level_count()

        cls.data['levels_completed'] = [False] * level_count
        cls.data['levels_completed'][0] = True

    @classmethod
    def _load_data(cls):
        '''load game save from storage'''
        if PLATFORM == 'emscripten':
            cls.data = json.loads(cls.window.localStorage.getItem('game_data'))
        else:
            with open(SAVE_PATH, 'r') as file:
                cls.data = json.load(file)

    @classmethod
    def save_data(cls):
        '''Save game data to storage'''
        if PLATFORM == 'emscripten':
            cls.window.localStorage.setItem('game_data', json.dumps(cls.data))
        else:
            with open(SAVE_PATH, 'w') as file:
                json.dump(cls.data, file)

    @classmethod
    def erase_data(cls):
        '''Reset game data to the start'''
        cls._initialize_save()
        cls.save_data()

    @classmethod
    def _get_level_count(cls):
        count = 0
        for path in os.listdir(LEVELS_PATH):
            if path.endswith('.json'):
                count += 1
        
        return count