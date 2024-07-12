from typing import Dict
import json
import os
import pygame
from pathlib import Path
from .constants import *

pygame.init()
pygame.mixer.init()


class AssetManager():
    images = {}
    sounds = {}
    fonts: Dict[str, pygame.Font] = {}
    data = {}

    @classmethod
    def load_assets(cls, assets_path):
        cls.images = cls.load_images(assets_path + 'images')
        cls.sounds = cls.load_sounds(assets_path + 'sfx')

        cls.fonts = {}

    @classmethod
    def load_image(cls, file_path) -> pygame.Surface:
        image = pygame.image.load(file_path).convert_alpha()
        name = Path(file_path).stem
        cls.images[name] = image

        return image
    
    @classmethod
    def load_sound(cls, file_path) -> pygame.mixer.Sound:
        sound = pygame.mixer.Sound(file_path)
        name = Path(file_path).stem
        cls.sounds[name] = sound

        return sound

    @classmethod
    def load_font(cls, file_path, size) -> pygame.Font:
        name = Path(file_path).stem
        key = f'{name}_{size}'
        
        # font loaded, so ignore
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
                print(f"Font Path: {path}, Font Size: {size}")

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
                print(name, image)

        return images
    
    @classmethod
    def load_sounds(cls, path):
        sounds = {}
        for name in os.listdir(path):
            filepath = path + '/' + name

            if name.endswith(('.ogg', '.wav')):
                try:
                    sound = pygame.mixer.Sound(filepath)

                    key = Path(filepath).stem
                    sounds[key] = sound 
                    print(f'{name} loaded.')
                except Exception as e:
                    print(f'{e}, {filepath}')


        return sounds

    @classmethod
    def set_volume(cls, master_volume):
        for sound in cls.sounds:
            cls.sounds[sound].set_volume(master_volume)

    
if __name__ == '__main__':
    AssetManager()

    AssetManager.load_assets('src/assets')
    print(AssetManager.images)