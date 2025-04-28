import pygame
from src.engine.base import Base
from src.engine.sprite import Sprite
from src.engine.asset_manager import AssetManager


class Decoration(Base):
    def __init__(self, position, image_key):
        self.position = pygame.Vector2(position)
        self.image_key = image_key
        image = AssetManager.images[self.image_key].convert_alpha()
        self.sprite = Sprite(image, static=True)

    def draw(self, surface):
        self.sprite.draw(surface)

    def update(self, delta):
        self.sprite.update(self.position)

    def serialize(self):
        return {
            'type': 'Decoration',
            'position': tuple(self.position),
            'image_key': self.image_key
        }
    
    @classmethod
    def deserialize(cls, data: dict):
        return cls(
            position=data['position'],
            image_key=data['image_key']
            )