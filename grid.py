import tile
import pygame
import random
import copy
import creature
class Grid():

    def __init__(self,width:int,height:int,WINDOW:pygame.surface.Surface) -> None:
        self.width = width
        self.height = height
        self.WINDOW = WINDOW
        self.climate_change = 0
        self.grid_array:list[list] = []
        for i in range(width):
            self.grid_array.append([])
            for j in range(height):
                climate_coefficient = j*0.1
                if climate_coefficient>1:
                    climate_coefficient = 1
                if climate_coefficient<0:
                    climate_coefficient = 0
                self.grid_array[i].append(tile.Tile(0,climate_coefficient))

    def do_climate_change(self,increase_amount):
        self.climate_change+=increase_amount
        for i in range(len(self.grid_array)):
            for j in range(len(self.grid_array[i])):
                if j<=self.climate_change:
                    self.grid_array[i][j].climate_coefficient=0.0
                else:
                    new_cc = (j-self.climate_change)*0.1
                    if new_cc>1:
                        new_cc = 1
                    if new_cc<0:
                        new_cc = 0
                    self.grid_array[i][j].climate_coefficient=new_cc

                


    def check_neighbours(self,grid_x:int,grid_y:int)->list[tile.Tile]:
        neighbour_list = []
        if grid_x>0: # Left
            neighbour_list.append(self.grid_array[grid_x-1][grid_y])
        if grid_y>0: # Above
            neighbour_list.append(self.grid_array[grid_x][grid_y-1])
        if grid_x<len(self.grid_array)-1: # Right
            neighbour_list.append(self.grid_array[grid_x+1][grid_y])
        if grid_y<len(self.grid_array[grid_x])-1: # Below
            neighbour_list.append(self.grid_array[grid_x][grid_y+1])

        if grid_x>0 and grid_y>0: #Topleft
            neighbour_list.append(self.grid_array[grid_x-1][grid_y-1])
        if grid_x<len(self.grid_array)-1 and grid_y>0: #Topright
            neighbour_list.append(self.grid_array[grid_x+1][grid_y-1])
        if grid_x>0 and grid_y<len(self.grid_array[grid_x])-1: #bottomleft
            neighbour_list.append(self.grid_array[grid_x-1][grid_y+1])
        if grid_x<len(self.grid_array)-1 and grid_y<len(self.grid_array[grid_x])-1: #bottomright
            neighbour_list.append(self.grid_array[grid_x+1][grid_y+1])
        return(neighbour_list)

    def check_creature_neighbours(self,grid_x,grid_y)->list[tile.Tile]:
        tile_list = self.check_neighbours(grid_x,grid_y)
        creature_list = []
        for object in tile_list:
            if object.creature != None:
                creature_list.append(object)
        return creature_list
    
    def check_empty_neighbours(self,grid_x,grid_y)->list[tile.Tile]:
        tile_list = self.check_neighbours(grid_x,grid_y)
        empty_tile_list = []
        for object in tile_list:
            if object.creature == None:
                empty_tile_list.append(object)
        return empty_tile_list

    def display(self):
        for i in range(0,len(self.grid_array)):
            for j in range(0,len(self.grid_array[i])):
                object = self.grid_array[i][j]
                if type(object)==tile.Tile:
                    
                    #new_rect.topleft = (i*32,j*32)
                    #new_rect.size = (32,32)
                
                    new_rect = pygame.rect.Rect(i*32,j*32,32,32)
                    green_hue = int(255*object.food)
                    temperature_hue = int(255*(1 - object.climate_coefficient))
                    self.WINDOW.fill((0,green_hue,temperature_hue),new_rect)
                    if object.value == 1:
                        new_rect = pygame.rect.Rect(i*32+2,j*32+2,28,28)
                        creature_color = tuple(object.creature.color)
                        self.WINDOW.fill(creature_color,new_rect)
                    elif object.value == 0 and object.is_blocker: # A blocker
                        new_rect = pygame.rect.Rect(i*32,j*32,32,32)
                        self.WINDOW.fill((100,100,100),new_rect)
   
    def move_creature(self,grid_x,grid_y):
        object:tile.Tile = self.grid_array[grid_x][grid_y]
        viable_tiles = self.check_empty_neighbours(grid_x,grid_y)
        if len(viable_tiles)!=0:
            new_tile = viable_tiles[random.randint(0,len(viable_tiles)-1)]
            if type(new_tile) == tile.Tile:
                new_tile.creature = object.creature
                object.creature = None
                new_tile.value = 1
                new_tile.next_value = 1
                object.value = 0
                object.next_value = 0

    def populate(self,creature_color,creature_metabolism,creature_is_producer,creature_is_carnivore):
        grid_x = random.randint(0,self.width-1)
        grid_y = random.randint(0,self.height-1)
        if self.grid_array[grid_x][grid_y].creature == None:
            near_tiles = self.check_neighbours(grid_x,grid_y)
            for object in near_tiles:
                if object.creature == None:
                    self.grid_array[grid_x][grid_y].creature = creature.Creature(creature_color,creature_metabolism,creature_is_producer,creature_is_carnivore)
                    self.grid_array[grid_x][grid_y].value = 1
                    
                    object.creature = creature.Creature(creature_color,creature_metabolism,creature_is_producer,creature_is_carnivore)
                    object.value = 1

    def update_tiles(self):
    # Update dead tiles
        for i in range(0,len(self.grid_array)):
            for j in range(0,len(self.grid_array[i])):
                object = self.grid_array[i][j]
                if type(object)==tile.Tile:
                    if object.value == 0 and not object.is_blocker:
                        creature_list = []
                        total = 0 # Amount of cells surrounding it that are value 1
                        if i>0: # Left
                            total+=self.grid_array[i-1][j].value
                            if self.grid_array[i-1][j].creature != None:
                                creature_list.append(self.grid_array[i-1][j].creature)
                        if j>0: # Above
                            total+=self.grid_array[i][j-1].value
                            if self.grid_array[i][j-1].creature != None:
                                creature_list.append(self.grid_array[i][j-1].creature)
                        if i<len(self.grid_array)-1:
                            total+=self.grid_array[i+1][j].value
                            if self.grid_array[i+1][j].creature != None:
                                creature_list.append(self.grid_array[i+1][j].creature)
                        if j<len(self.grid_array[i])-1:
                            total+=self.grid_array[i][j+1].value
                            if self.grid_array[i][j+1].creature != None:
                                creature_list.append(self.grid_array[i][j+1].creature)

                        if i>0 and j>0: #Topleft
                            total+=self.grid_array[i-1][j-1].value
                            if self.grid_array[i-1][j-1].creature != None:
                                creature_list.append(self.grid_array[i-1][j-1].creature)
                        if i<len(self.grid_array)-1 and j>0: #Topright
                            total+=self.grid_array[i+1][j-1].value
                            if self.grid_array[i+1][j-1].creature != None:
                                creature_list.append(self.grid_array[i+1][j-1].creature)
                        if i>0 and j<len(self.grid_array[i])-1: #bottomleft
                            total+=self.grid_array[i-1][j+1].value
                            if self.grid_array[i-1][j+1].creature != None:
                                creature_list.append(self.grid_array[i-1][j+1].creature)
                        if i<len(self.grid_array)-1 and j<len(self.grid_array[i])-1: #bottomright
                            total+=self.grid_array[i+1][j+1].value
                            if self.grid_array[i+1][j+1].creature != None:
                                creature_list.append(self.grid_array[i+1][j+1].creature)
                                                
                        if total > 1: # Dead cell becomes alive
                            inheritor_creature = creature_list[random.randint(0,len(creature_list)-1)]
                            if inheritor_creature.is_carnivore:
                                inheritor_creature.food_store -= inheritor_creature.metabolism / 5
                            if random.random()*total < inheritor_creature.metabolism*2:
                                object.creature = copy.deepcopy(inheritor_creature)
                                if random.random() < 0.05:
                                    object.creature.mutate()
                                object.next_value = 1
                        else: # dead cell stays dead
                            object.next_value = 0
                        object.food-=0.01*total
                        object.food +=0.1
                        if object.food >1.0:
                            object.food =1.0
    
    # Update living tiles
        for i in range(0,len(self.grid_array)):
            for j in range(0,len(self.grid_array[i])):
                object = self.grid_array[i][j]
                if type(object)==tile.Tile:
                    if object.value == 1:
                        total = 0 # Amount of cells surrounding it that are value 1
                        if i>0: # Left
                            total+=self.grid_array[i-1][j].value
                        if j>0: # Above
                            total+=self.grid_array[i][j-1].value
                        if i<len(self.grid_array)-1:
                            total+=self.grid_array[i+1][j].value
                        if j<len(self.grid_array[i])-1:
                            total+=self.grid_array[i][j+1].value

                        if i>0 and j>0: #Topleft
                            total+=self.grid_array[i-1][j-1].value
                        if i<len(self.grid_array)-1 and j>0: #Topright
                            total+=self.grid_array[i+1][j-1].value
                        if i>0 and j<len(self.grid_array[i])-1: #bottomleft
                            total+=self.grid_array[i-1][j+1].value
                        if i<len(self.grid_array)-1 and j<len(self.grid_array[i])-1: #bottomright
                            total+=self.grid_array[i+1][j+1].value
                                                
                        object.next_value = 1
                        object.food-=1*(1-object.climate_coefficient)
                        if not object.creature.is_carnivore and not object.creature.is_producer: # Check if the population migrates
                                if random.random()<object.creature.movement_ability:
                                    self.move_creature(i,j)
                        if not object.creature.is_carnivore: # Non carnivore upkeep
                            object.food-=object.creature.metabolism
                            object.food-=0.025*total
                            object.food-=0.5*object.creature.evade_chance
                        else: # Carnivore/predator code
                            object.creature.food_store-=object.creature.metabolism
                            if object.creature.food_store<=0:
                                object.value = 0
                                object.next_value = 0
                                object.creature = None
                            else:
                                nearby_creatures = self.check_creature_neighbours(i,j)
                                if len(nearby_creatures) != 0:
                                    target_creature_tile = nearby_creatures[random.randint(0,len(nearby_creatures)-1)]
                                    if not target_creature_tile.creature.is_carnivore: # Carnivores for simplification cannot eat other carnivores
                                        if random.random() > target_creature_tile.creature.evade_chance:
                                            target_creature_tile.value = 0
                                            target_creature_tile.next_value = 0
                                            target_creature_tile.creature = None
                                            object.creature.food_store+=1

                        if object.creature != None: # Has to check incase a predator dies, as otherwise it'll check if None type has attributes
                            if object.creature.is_producer: # Producer code
                                clear_tiles = 9 - total 
                                food_produced = clear_tiles*object.creature.metabolism/8
                                for neighbour in self.check_neighbours(i,j):
                                    if type(neighbour) == tile.Tile:
                                        neighbour.food+=food_produced
                                        if neighbour.food > 1:
                                            neighbour.food = 1 
                                    object.food+=food_produced

                            if not object.creature.is_carnivore and not object.creature.is_producer: # Check if the creature needs to move
                                if object.food < object.creature.metabolism+0.025*total+0.5*object.creature.evade_chance:
                                    if random.random()<object.creature.reasoning:
                                        self.move_creature(i,j)

                        if object.food<0:
                            object.next_value = 0
                            object.creature = None
                            object.food = 0
                        object.food +=0.1
                        if object.food >1.0:
                            object.food =1.0       



        for i in range(0,len(self.grid_array)):
            for j in range(0,len(self.grid_array[i])):
                object = self.grid_array[i][j]
                if type(object)==tile.Tile:
                    object.value = object.next_value

    def clear(self):
        for row in self.grid_array:
            for element in row:
                element.value = 0
                element.next_value = 0
                element.creature = None