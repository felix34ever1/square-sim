import random

class Disease():

    def __init__(self) -> None:
        self.deadly = 0.0
        self.leech = 0.0
        self.color = [0,0,0]
    
    def mutate(self):
        self.deadly = random.random()
        self.leech = random.random()
        self.color = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]