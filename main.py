import pygame
import grid
import tile
import creature
import random
import disease

pygame.init()

grid_size = (40,25)

WINDOW = pygame.display.set_mode((32*grid_size[0]+200,32*grid_size[1]))

grid = grid.Grid(grid_size[0],grid_size[1],WINDOW)

k = random.randint(1,4)
n = random.randint(1,4)

# Font
default_font = pygame.font.Font("cnc.ttf",20)

# Text

WHITE = (255,255,255)
creature_display_color = [0,0,0]
creature_display_rect = pygame.rect.Rect(grid_size[0]*32+84, 300,32,32)
metabolism_text = default_font.render(f"Me: ",False,WHITE)
evade_text = default_font.render(f"Ev: ",False,WHITE)
movement_text = default_font.render(f"Mov: ",False,WHITE)
reasoning_text = default_font.render(f"Rea: ",False,WHITE)
type_text = default_font.render(f"Prod: | Carn:",False,WHITE)
disease_text = default_font.render(f"Deadly: | Leech:",False, WHITE)

# HUD Images
edit_on = pygame.image.load("edit_on.png")
edit_off = pygame.image.load("edit_off.png")
edit_rect = edit_on.get_rect()
edit_rect.topleft = (32*grid_size[0]+84,32)


playing = True
editing = True
simulating = False
simulation_timer = pygame.time.Clock()
creature_metabolism = 0.1
creature_color = [255,255,255]
creature_is_producer = False
creature_is_carnivore = False
placing_blocker = False
simulation_ticks = 0
repopulation_ticks = 0
climate_ticks = 0 
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
                creature_is_carnivore = False

            if event.key == pygame.K_2:
                # Slow metabolism creature
                creature_metabolism = 0.02
                creature_color = [0,0,255]
                creature_is_producer = False
                creature_is_carnivore = False

            if event.key == pygame.K_3:
                # Fast metabolism creature
                creature_metabolism = 0.5
                creature_color = [255,0,0]
                creature_is_producer = False
                creature_is_carnivore = False

            if event.key == pygame.K_4:
                # Producer medium metabolism creature
                creature_metabolism = 0.4
                creature_color = [255,255,0]
                creature_is_producer = True
                creature_is_carnivore = False

            if event.key == pygame.K_5:
                # Carnivore!!!
                creature_metabolism = 0.3
                creature_color = [255,100,70]
                creature_is_producer = False
                creature_is_carnivore = True
            
            if event.key == pygame.K_b:
                # Blocker toggle
                placing_blocker = not placing_blocker

            if event.key == pygame.K_c:
                grid.clear()
        

    WINDOW.fill((0,0,0))
    grid.display()

    for i in range(grid_size[0]):
        pygame.draw.line(WINDOW,(0,0,0),[i*32,0],[i*32,grid_size[1]*32])
        for j in range(grid_size[1]):
            pygame.draw.line(WINDOW,(0,0,0),[0,j*32],[grid_size[0]*32,j*32])
            

    if editing:
        WINDOW.blit(edit_on,edit_rect)
        if pygame.mouse.get_pressed()[0]:# Place creature
            position = pygame.mouse.get_pos()
            grid_pos = (position[0]//32,position[1]//32)
            try:
                current_tile = grid.grid_array[grid_pos[0]][grid_pos[1]]
                if type(current_tile) == tile.Tile:
                    if placing_blocker: # Place blocker
                        current_tile.value = 0
                        current_tile.next_value = 0
                        current_tile.creature = None
                        current_tile.is_blocker = not current_tile.is_blocker
                    else: # Placing creature
                        if not current_tile.is_blocker:
                            current_tile.value = 1
                            current_tile.creature = creature.Creature(creature_color,creature_metabolism,creature_is_producer,creature_is_carnivore)
                            current_tile.creature.disease = disease.Disease()
                            current_tile.creature.disease.mutate()
            except:
                print("clicked out of bounds")
        if pygame.mouse.get_pressed()[2]:# Get creature stats
            position = pygame.mouse.get_pos()
            grid_pos = (position[0]//32,position[1]//32)
            current_tile = grid.grid_array[grid_pos[0]][grid_pos[1]]
            if type(current_tile) == tile.Tile:
                if current_tile.creature != None:
                    selected = current_tile.creature
                    creature_display_color = selected.color
                    metabolism_text = default_font.render(f"Me: {round(selected.metabolism,2)}",False,WHITE)
                    evade_text = default_font.render(f"Ev: {round(selected.evade_chance,2)}",False,WHITE)
                    movement_text = default_font.render(f"Mov: {round(selected.movement_ability,2)}",False,WHITE)
                    reasoning_text = default_font.render(f"Rea: {round(selected.reasoning,2)}",False,WHITE)
                    type_text = default_font.render(f"Prod:{selected.is_producer} |Carn:{selected.is_carnivore}",False,WHITE)
                    if selected.disease!=None:
                        disease_text = default_font.render(f"Deadly: {round(selected.disease.deadly,2)}| Leech:{round(selected.disease.leech,2)}",False, WHITE)

    if simulating:
        WINDOW.blit(edit_off,edit_rect)
        ticks_passed = simulation_timer.tick()
        simulation_ticks+=ticks_passed
        repopulation_ticks+=ticks_passed
        climate_ticks+=ticks_passed
        if simulation_ticks>100:
            simulation_ticks = 0
            grid.update_tiles()
        if repopulation_ticks>10000:
            repopulation_ticks=0
            grid.populate([random.randint(0,255),random.randint(0,255),random.randint(0,255)],0.1,False,False)
        #if climate_ticks>5000:
        #    grid.do_climate_change(1)
        #    climate_ticks=0

    pygame.draw.rect(WINDOW,creature_display_color,creature_display_rect)
    WINDOW.blit(metabolism_text,(grid_size[0]*32+10, 400))
    WINDOW.blit(evade_text,(grid_size[0]*32+10, 440))
    WINDOW.blit(movement_text,(grid_size[0]*32+10, 480))
    WINDOW.blit(reasoning_text,(grid_size[0]*32+10, 520))
    WINDOW.blit(type_text,(grid_size[0]*32+10, 560))
    WINDOW.blit(disease_text,(grid_size[0]*32+10,600))
        
        


    pygame.display.update()
    