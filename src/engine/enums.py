from enum import Enum


class FinishPointState(Enum):
    IDLE = 1
    TOUCHING = 2
    COMPLETED = 3
    REACTED = 4