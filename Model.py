import numpy.random as random

class Agent():
    def __init__(self):
        self.counter = 100
        self.action = None
        pass

    def random_action(self):
        if(self.counter > 30):
            self.action = (random.choice(["w","$"],1,[0.90,0.1])[0], random.randint(0,31), random.randint(13,17))
            self.counter = 0

        self.counter += 1
        return self.action

