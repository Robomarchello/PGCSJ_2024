from typing import Dict
import os
import pygame
from pathlib import Path
from .constants import *

pygame.init()


class AssetManager():
    images = {}
    sounds = {}
    fonts = {}
    data = {}

    @classmethod
    def load_assets(cls, assets_path):
        cls.images = cls.load_images(assets_path + '/images')
        cls.sounds = cls.load_images(assets_path + '/sfx')
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

        font = pygame.font.Font(file_path, size)

        cls.fonts[f'{name}_{size}'] = font

        return font


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
                sound = pygame.mixer.Sound(filepath)

                key = Path(filepath).stem
                sounds[key] = sound 
                print(f'{name} loaded.')

        return sounds

    @classmethod
    def set_volume(cls, master_volume):
        for sound in cls.sounds:
            cls.sounds[sound].set_volume(master_volume)

    
if __name__ == '__main__':
    AssetManager()

    AssetManager.load_assets('src/assets')
    print(AssetManager.images)