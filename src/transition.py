from engine.state_machine import State


class Transition(State):
    def __init__(self, 
                 state_1, state_2, 
                 duration
                 ):
        super().__init__()

        self.state_1 = state_1
        self.state_2 = state_2
        
        self.duration = duration
        
        self.timer = self.duration
        self.changed = False

        self.switch_state = False

    def draw(self, screen):
        color = (self.fadeout / 3) * 255

    def update(self, delta):
        if not self.changed:
            self.timer -= delta

            if self.timer < 0:
                self.changed = True
                self.timer = self.out_duration
        
        else:
            self.timer -= delta

            if self.timer < 0:
                self.finished = True
                self.manager.next_state = self.state_2()

        

    def on_start():
        # timer = 0
        pass

    def on_exit():
        pass


class TransitionFade(Transition):
    def __init__(self):
        super.__init__()
    
    def draw(self, screen):
        if not self.changed:
            progress = self.timer / self.in_duration
        else:
            progress = self.timer / self.out_duration