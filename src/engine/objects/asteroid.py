from src.engine.asset_manager import AssetManager
from src.engine.objects import Object
from src.engine.sprite import Sprite


class Asteroid(Object):
    def __init__(self, position, velocity, mass, radius):
        super().__init__(position, velocity, mass)
        self.texture = AssetManager.images['asteroid'].convert()
        self.texture.set_colorkey((255, 0, 0))

        self.sprite = Sprite(self.texture, ['center'], static=True)

        self.radius = radius

        self.orientation = 0.0

    def update(self, delta):
        self.motion_logic(delta)

    def draw(self, surface):
        self.sprite.update(self.position)

        self.sprite.draw(surface)

    def serialize(self):
        return {
            'type': 'Asteroid',
            'position': tuple(self.position),
            'velocity': tuple(self.velocity),
            'mass': self.mass,
            'radius': self.radius
        }
    
    @classmethod
    def deserialize(cls, data: dict):
        return cls(
            position=data['position'],
            velocity=data['velocity'],
            mass=data['mass'],
            radius=data['radius'],
            )
