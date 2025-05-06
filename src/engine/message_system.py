from typing import List
import pygame
from pygame.locals import *
from src.engine.asset_manager import AssetManager
from src.engine.base import Base
import src.engine.config as c
from enum import Enum, auto


class MessageState(Enum):
    INTRO = auto()
    HOLD = auto()
    OUTRO = auto()
    DONE = auto()


class Message:
    # as a percentage
    INTRO_TIME = 0.3  
    OUTRO_TIME = 0.15
    SPEED_LIMIT = 80

    def __init__(self, start_pos, text, duration, font):
        self.font = font
        self.text = text
        self.render = self.font.render(self.text, True, (255, 255, 255))

        self.target_pos = pygame.Vector2(start_pos)
        self.position = self.target_pos.copy()

        self.rect = self.render.get_rect()

        self.intro_duration = duration * self.INTRO_TIME
        self.hold_duration = duration * (1 - self.INTRO_TIME - self.OUTRO_TIME)
        self.outro_duration = duration * self.OUTRO_TIME
        
        self.duration = self.intro_duration
        self.timer = self.duration

        # states: intro, holding, outro, completed (or whatever is better)
        self.state = MessageState.INTRO

        # spring
        # f = -kx
        self.velocity = pygame.Vector2()
        self.damping = 0.85
        self.stiffness = 5

    def draw(self, surface):
        surface.blit(self.render, self.rect)

    def update(self, delta):
        self.timer -= delta

        if self.timer < 0:
            if self.state == MessageState.INTRO:
                self._change_state(MessageState.HOLD)
            elif self.state == MessageState.HOLD:
                self._change_state(MessageState.OUTRO)
            elif self.state == MessageState.OUTRO:
                self._change_state(MessageState.DONE)

        diff = self.target_pos - self.position
        self.velocity += diff * self.stiffness * delta
        self.velocity -= (self.velocity * (1 - self.damping)) * delta * c.SPEED_FACTOR

        self.position += self.velocity * delta * c.SPEED_FACTOR

        length = self.velocity.length()
        if length > self.SPEED_LIMIT:
            self.velocity = self.velocity.normalize() * self.SPEED_LIMIT

        self.rect.center = self.position

    def _change_state(self, new_state):
        '''Handles switching states.'''
        if self.state != new_state:
            self.state = new_state

            if new_state == MessageState.INTRO:
                self.timer = self.intro_duration
            if new_state == MessageState.HOLD:
                self.timer = self.hold_duration
            if new_state == MessageState.OUTRO:
                self.timer = self.outro_duration


class MessageHandler(Base):
    MESSAGE_LIMIT = 100
    FONT_SIZE = 24
    messages: List[Message] = []
    font = None
    
    @classmethod
    def init_font(cls):
        cls.font = AssetManager.fonts[f'font_{cls.FONT_SIZE}']

    @classmethod
    def post(cls, text, duration=2.0, sound=None):
        if len(cls.messages) < cls.MESSAGE_LIMIT:
            msg = Message((-500, 0), text, duration, cls.font)
            cls.messages.append(msg)
        
            if sound:
                sound.play()

    @classmethod
    def update(cls, delta):
        intro_count = 0
        for msg in cls.messages:
            msg.update(delta)
            if msg.state == MessageState.INTRO or msg.state == MessageState.HOLD:
                msg.target_pos = (c.SCREEN_W / 2, 40 + intro_count * 50)
                intro_count += 1
            if msg.state == MessageState.OUTRO:
                msg.target_pos = (c.SCREEN_W + msg.rect.width, 40)
            if msg.state == MessageState.DONE:
                cls.messages.remove(msg)

    @classmethod
    def draw(cls, surface):
        for msg in cls.messages:
            msg.draw(surface)