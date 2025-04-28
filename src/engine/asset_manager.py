"""
Idea:
logic here can be changed, 
to ensure that assets will load at any time.
Right now i don't like that I have to call load_assets() before everything 
I saw someone use lru_cache which is kinda smart.
Something similar can be done.
Now I think there are more convinient ways indeed
"""
from typing import Dict
import json
import os
from pathlib import Path
import pygame
from src.engine.config import FONTS_JSON_PATH

pygame.init()
pygame.mixer.init()


class AssetManager():
    images = {}
    sounds = {}
    fonts: Dict[str, pygame.Font] = {}
    data = {}

    volume = 1.0
    music_volume = 1.0

    @classmethod
    def load_assets(cls, assets_path):
        '''Load assets folder: images, sounds, fonts'''
        cls.images = cls.load_images(assets_path + 'images')
        cls.sounds = cls.load_sounds(assets_path + 'sfx')
        AssetManager.load_fonts_json(FONTS_JSON_PATH)

    @classmethod
    def load_image(cls, file_path) -> pygame.Surface:
        '''Load single image'''
        image = pygame.image.load(file_path).convert_alpha()
        name = Path(file_path).stem
        cls.images[name] = image

        return image
    
    @classmethod
    def load_sound(cls, file_path) -> pygame.mixer.Sound:
        '''load single sound'''
        sound = pygame.mixer.Sound(file_path)
        name = Path(file_path).stem
        cls.sounds[name] = sound

        return sound

    @classmethod
    def load_font(cls, file_path, size) -> pygame.Font:
        '''load single font'''
        name = Path(file_path).stem
        key = f'{name}_{size}'
        
        # if font loaded - ignore
        if cls.fonts.get(key):
            return
        
        font = pygame.font.Font(file_path, size)
        cls.fonts[key] = font

        return font

    @classmethod
    def load_fonts_json(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            
            for font in data['fonts']:
                path = font['path']
                size = font['size']

                cls.load_font(path, size)

    @classmethod
    def load_images(cls, path):
        images = {}
        for name in os.listdir(path):
            file_path = path + '/' + name

            if name.endswith(('.png', '.jpg')):
                image = pygame.image.load(file_path)
                if pygame.display.get_active():
                    image = image.convert_alpha()
                name = Path(file_path).stem
                images[name] = image

        return images
    
    @classmethod
    def load_sounds(cls, path):
        sounds = {}
        for name in os.listdir(path):
            filepath = path + '/' + name

            if name.endswith(('.ogg', '.wav')):
                sound = pygame.mixer.Sound(filepath)
                key = Path(filepath).stem
                sounds[key] = sound 

        return sounds

    @classmethod
    def set_volume(cls, master_volume):
        for sound in cls.sounds:
            cls.sounds[sound].set_volume(master_volume)

    @classmethod
    def set_music_volume(cls, volume):
        pygame.mixer.music.set_volume(volume)

    
if __name__ == '__main__':
    AssetManager()

    AssetManager.load_assets('src/assets')
    print(AssetManager.images)