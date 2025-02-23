class GravityInvertor:
    def __init__(self, position, timer, object_handler):
        self.position = position

        self.timer = timer
        self.crnt_timer = timer
        self.object_handler = object_handler
        
    def draw(self, surface):
        pass

    def update(self, delta):
        self.crnt_timer -= delta
        if self.crnt_timer < 0:
            self.crnt_timer = self.timer