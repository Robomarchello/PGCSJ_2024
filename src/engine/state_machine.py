import pygame
from pygame.locals import *
from .constants import SCREENSIZE


class StateMachine:
    def __init__(self, initial_state):
        self.active_state = initial_state
        self.active_state.on_start()
        self.active_state.manager = self
        self.next_state = None

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
    
    def draw(self, screen):
        self.active_state.draw()

        screen.blit(self.active_state.surface, (0, 0))

    def change_state(self, new_state:'State', transition):
        pass
    

class State:
    def __init__(self):
        self.surface = pygame.Surface(SCREENSIZE)
        self.manager: StateMachine | None = None

    def draw(self, screen):
        pass

    def update(self, delta=1):
        pass

    def on_start(self):
        raise NotImplementedError()
    
    def on_exit(self):
        raise NotImplementedError()

    def handle_event(self, event):
        pass


if __name__ == '__main__':
    class MyState1(State):
        def __init__(self):
            super().__init__()

        def on_start(self):
            print('nig')

        def on_exit(self):
            print('gin')

        def draw(self):
            self.surface.fill(pygame.Color('blue'))

    class MyState(State):
        def __init__(self):
            super().__init__()

            self.duration = 60

        def on_start(self):
            print('nig')

        def on_exit(self):
            print('heil')

        def draw(self):
            self.surface.fill(pygame.Color('red'))

        def update(self):
            self.duration -= 1
            if self.duration < 0:
                self.manager.next_state = MyState1()
                print('manager')


    state_machine = StateMachine(MyState())
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((512, 512))
    while True:
        clock.tick(60)        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                raise SystemExit
        
        state_machine.draw(screen)
        state_machine.update()

        pygame.display.update()