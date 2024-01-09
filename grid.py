import tile
import pygame
import random
import copy
class Grid():

    def __init__(self,width:int,height:int,WINDOW:pygame.surface.Surface) -> None:
        self.width = width
        self.height = height
        self.WINDOW = WINDOW
        self.grid_array:list[list] = []
        for i in range(width):
            self.grid_array.append([])
            for j in range(height):
                self.grid_array[i].append(tile.Tile(0))
            
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

    def display(self):
        for i in range(0,len(self.grid_array)):
            for j in range(0,len(self.grid_array[i])):
                object = self.grid_array[i][j]
                if type(object)==tile.Tile:
                    new_rect = pygame.rect.Rect(i*32,j*32,32,32)
                    #new_rect.topleft = (i*32,j*32)
                    #new_rect.size = (32,32)
                    if object.value == 0:
                        green_hue = int(255*object.food)
                        self.WINDOW.fill((0,green_hue,0),new_rect)
                    elif object.value == 1:
                        creature_color = tuple(object.creature.color)
                        self.WINDOW.fill(creature_color,new_rect)
    

    
    def update_tiles(self):
    # Update dead tiles
        for i in range(0,len(self.grid_array)):
            for j in range(0,len(self.grid_array[i])):
                object = self.grid_array[i][j]
                if type(object)==tile.Tile:
                    if object.value == 0:
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
                                                
                        if total > 2 and total < 4: # Dead cell becomes alive
                            inheritor_creature = creature_list[random.randint(0,len(creature_list)-1)]
                            if random.random() < inheritor_creature.metabolism*2:
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
                        object.food-=object.creature.metabolism
                        object.food-=0.025*total
                        if object.creature.is_producer:
                            clear_tiles = 9 - total 
                            food_produced = clear_tiles*object.creature.metabolism/8
                            for neighbour in self.check_neighbours(i,j):
                                if type(neighbour) == tile.Tile:
                                    neighbour.food+=food_produced
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