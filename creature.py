import random

class Creature():

    def __init__(self,color:list[int],metabolism:float,is_producer:bool=False,is_carnivore:bool=False) -> None:
        self.color = color
        self.metabolism = metabolism
        self.is_producer = is_producer
        self.is_carnivore = is_carnivore
        self.evade_chance = 0.0
        self.food_store = 1.0
        self.movement_ability = 0.0
        self.reasoning = 0.0
        self.disease = None

    def mutate(self):
        for i in range(3):
            color_choice = random.randint(0,2)
            self.color[color_choice] += random.randint(-150,150)
            if self.color[color_choice] >255:
                self.color[color_choice] = 255
            elif self.color[color_choice]<0:
                self.color[color_choice] = 0
        self.metabolism = random.random()/2
        self.evade_chance = random.random()
        self.movement_ability = random.random()
        self.reasoning = random.random()
        if self.is_producer:
            if random.random() < 0.02:
                self.is_producer = False
        elif self. is_carnivore:
            if random.random() <0.02:
                self.is_carnivore = False
        else:
            chance = random.random()
            if chance < 0.01:
                self.is_producer = True
            if chance > 0.01:
                self.is_carnivore = True

