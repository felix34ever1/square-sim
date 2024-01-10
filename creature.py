import random

class Creature():

    def __init__(self,color:list[int],metabolism:float,is_producer:bool=False,is_carnivore:bool=False) -> None:
        self.color = color
        self.metabolism = metabolism
        self.is_producer = is_producer
        self.is_carnivore = is_carnivore
        self.evade_chance = 0.0
        self.food_store = 1.0

    def mutate(self):
        color_choice = random.randint(0,2)
        self.color[color_choice] += random.randint(-75,75)
        if self.color[color_choice] >255:
            self.color[color_choice] = 255
        elif self.color[color_choice]<0:
            self.color[color_choice] = 0
        self.metabolism = random.random()/2
        self.evade_chance = random.random()