
class TransitionFade():
    def __init__(self, duration):
        #self.state_1 = state_1
        #self.state_2 = state_2
        
        self.duration = duration
        self.half_duration = duration / 2
        
        self.timer = self.half_duration

        self.switch_state = False
        self.switched = False

    def draw(self, surface):
        pass

    def update(self, delta):
        pass