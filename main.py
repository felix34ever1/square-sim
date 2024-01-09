import pygame
import grid
import tile
import creature

pygame.init

grid_size = (30,20)

WINDOW = pygame.display.set_mode((32*grid_size[0],32*grid_size[1]))

grid = grid.Grid(30,20,WINDOW)


playing = True
editing = True
simulating = False
simulation_timer = pygame.time.Clock()
creature_metabolism = 0.1
creature_color = [255,255,255]
creature_is_producer = False
ticks_passed = 0
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                grid.update_tiles()
            if event.key == pygame.K_m:
                editing = not(editing)
                simulating = not(simulating)
            if event.key == pygame.K_1:
                # Normal creature
                creature_metabolism = 0.1
                creature_color = [255,255,255]
                creature_is_producer = False

            if event.key == pygame.K_2:
                # Slow metabolism creature
                creature_metabolism = 0.02
                creature_color = [0,0,255]
                creature_is_producer = False

            if event.key == pygame.K_3:
                # Fast metabolism creature
                creature_metabolism = 0.5
                creature_color = [255,0,0]
                creature_is_producer = False

            if event.key == pygame.K_4:
                # Producer medium metabolism creature
                creature_metabolism = 0.2
                creature_color = [255,255,0]
                creature_is_producer = True

            if event.key == pygame.K_c:
                grid.clear()
        

    WINDOW.fill((0,0,0))
    grid.display()

    for i in range(grid_size[0]):
        pygame.draw.line(WINDOW,(0,0,0),[i*32,0],[i*32,grid_size[1]*32])
        for j in range(grid_size[1]):
            pygame.draw.line(WINDOW,(0,0,0),[0,j*32],[grid_size[0]*32,j*32])
            

    if editing:
        if pygame.mouse.get_pressed()[0]:# Place creature
            position = pygame.mouse.get_pos()
            grid_pos = (position[0]//32,position[1]//32)
            current_tile = grid.grid_array[grid_pos[0]][grid_pos[1]]
            if type(current_tile) == tile.Tile:
                current_tile.value = 1
                current_tile.creature = creature.Creature(creature_color,creature_metabolism)
        if pygame.mouse.get_pressed()[2]:# Get creature metabolism
            position = pygame.mouse.get_pos()
            grid_pos = (position[0]//32,position[1]//32)
            current_tile = grid.grid_array[grid_pos[0]][grid_pos[1]]
            if type(current_tile) == tile.Tile:
                if current_tile.creature != None:
                    print(current_tile.creature.metabolism)
    if simulating:
        ticks_passed+=simulation_timer.tick()
        if ticks_passed>20:
            ticks_passed = 0
            grid.update_tiles()

        
        


    pygame.display.update()
    