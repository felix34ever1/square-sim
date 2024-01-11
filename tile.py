import creature

class Tile:

    def __init__(self,value=0,climate_coefficient = 1.0) -> None:
        self.value = value
        self.next_value = 0
        self.creature:creature.Creature = None
        self.food = 1.0
        self.is_blocker = False
        self.climate_coefficient = climate_coefficient