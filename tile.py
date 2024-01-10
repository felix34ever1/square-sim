import creature

class Tile:

    def __init__(self,value=0) -> None:
        self.value = value
        self.next_value = 0
        self.creature:creature.Creature = None
        self.food = 1.0
        self.is_blocker = False