import pygame
from src.engine.constants import SPEED_FACTOR
from src.engine.sprite import Sprite
from src.engine.utils import collide_circles
from src.engine.asset_manager import AssetManager
from src.engine.objects import Object
from src.engine.enums import FinishPointState


class FinishPoint(Object):
    def __init__(self, position, radius, player):
        super().__init__(position)

        self.radius = radius
        self.player = player

        self.rotation = 0.0

        self.complete_timer = 1.0
        self.timer = self.complete_timer

        self.state = FinishPointState.IDLE

        # images
        self.image = AssetManager.images['planet'].convert()
        self.image.set_colorkey((255, 0, 0))

        self.sprite = Sprite(self.image, ['center'])

        # sounds
        self.last_change = False
        self.sound = AssetManager.sounds['finished']

    def _change_state(self, new_state):
        '''Handles state transitions.'''
        if self.state != new_state:
            self.state = new_state
            if new_state == FinishPointState.TOUCHING:
                self.sound.play()
                self.player.freeze = True

    def update(self, delta):
        self.sprite.update(self.position)

        collision = collide_circles(
            self.position, self.radius,
            self.player.position, self.player.radius
        )
        if self.state == FinishPointState.IDLE:
            if collision and not self.player.exploded:
                self._change_state(FinishPointState.TOUCHING)

        elif self.state == FinishPointState.TOUCHING:
            pull_force = self.pulling_force(self.player.position)
            self.player.position += pull_force * delta * SPEED_FACTOR
            self.timer -= delta

            if self.timer < 0.0:
                self._change_state(FinishPointState.COMPLETED)

        self.rotation -= delta

    def draw(self, surface):
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        self.sprite.update_image(rotated_image)

        self.sprite.draw(surface)
        # image_rect = rotated_image.get_rect(center=self.cam_pos)
        # surface.blit(rotated_image, image_rect.topleft)

    def pulling_force(self, position: pygame.Vector2): 
        difference = self.position - position
        
        return difference * 0.1

    def serialize(self):
        return {
            'type': 'FinishPoint',
            'position': tuple(self.position),
            'radius': self.radius
        }

    @classmethod
    def deserialize(cls, data: dict, player):
        return cls(
            position=data['position'],
            radius=data['radius'],
            player=player
            )