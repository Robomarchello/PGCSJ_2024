import pygame
from src.engine.base import Base
from src.states.transition import TransitionClose


class StateMachine(Base):
    def __init__(self, initial_state):
        self.active_state = initial_state
        self.active_state.on_start()
        self.active_state.manager = self
        self.next_state = None

        self.transition = TransitionClose(2)

    def update(self, delta):
        if self.active_state is None:          
            return None
        
        if self.next_state is not None:
            self.active_state.on_exit()
            self.active_state.manager = None

            self.active_state = self.next_state
            self.active_state.on_start()
            self.active_state.manager = self

            self.next_state = None
        
        self.active_state.update(delta)
        self.transition.update(delta)
    
    def draw(self, surface):
        self.active_state.draw(surface)
        self.transition.draw(surface)

    def change_state(self, new_state:'State'):
        def set_next_state():
            self.next_state = new_state
        self.transition.function = set_next_state
        self.transition.start(0.7)


class State(Base):
    def __init__(self):
        self.manager: StateMachine | None = None

    def draw(self, surface):
        pass

    def update(self, delta=1):
        pass

    def on_start(self):
        raise NotImplementedError()
    
    def on_exit(self):
        raise NotImplementedError()
    
    def on_resize(self, size):
        self.surface = pygame.Surface(size)

    def handle_event(self, event):
        pass
