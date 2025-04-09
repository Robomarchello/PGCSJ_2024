from enum import Enum


class FinishPointState(Enum):
    IDLE = 1
    TOUCHING = 2
    COMPLETED = 3
    REACTED = 4


class TransitionState(Enum):
    INACTIVE = 1
    FADE_IN = 2
    EXECUTING = 3
    FADE_OUT = 4


class EmitterShape(Enum):
    RECT = 'rect'
    ELLIPSE = 'ellipse'