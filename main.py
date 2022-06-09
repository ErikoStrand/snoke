from turtle import width
import pygame, sys
from grid import Grid
from snake import snake
import numpy as np
# values
BACKGROUND = (255, 255, 255)
SNAKE_COLOR = (100, 100, 100)
WIDTH, HEIGHT = 850, 750
SNAKE_BODY = []
MOVE_SNAKE = pygame.USEREVENT
# toggles
MAIN_MENU = True
RUNNING = False

# pygame init
pygame.init()
pygame.font.init()
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.time.set_timer(MOVE_SNAKE, 250)
# grid
grid = Grid(15, WIDTH, HEIGHT)      
grid.create_grid()
head = snake(grid.grid[0][0])
grid.random_apple()
    
while MAIN_MENU:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            head = snake(grid.grid[0][0])
            MAIN_MENU = False
            RUNNING = True
            
    display.fill(BACKGROUND)
    pygame.display.flip()
    while RUNNING:
        dt = clock.tick(120) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOVE_SNAKE:
                if head.direction == 1:
                    head.x += grid.square_size
                elif head.direction == 2:
                    head.x -= grid.square_size
                elif head.direction == 3:
                    head.y -= grid.square_size
                elif head.direction == 4:
                    head.y += grid.square_size
                if len(head.locations) < head.length:
                    head.locations.append(head.rect)
                    if len(head.locations) == head.length:
                        head.locations.pop(0)
                    print(head.locations)      
        display.fill(BACKGROUND)
        # update
        head.update(dt, event)
        
        for body in range(len(head.locations)):
            if head.rect.colliderect(head.locations[body]):
                MAIN_MENU = True
                RUNNING = False
        if head.x < 0 or head.x > WIDTH or head.y < 0 or head.y > HEIGHT:
            MAIN_MENU = True
            RUNNING = False       
        if head.rect.colliderect(grid.grid[grid.apple_locations[0][0]][grid.apple_locations[0][1]]):
            grid.board[grid.apple_locations[0][0]][grid.apple_locations[0][1]] = 0
            grid.apple_locations.clear()
            grid.random_apple()
            head.length += 1
            print(head.length)
            
        #draw
        #print(grid.board)
        grid.draw_grid(display)
        grid.draw_apples(display)
        pygame.draw.rect(display, SNAKE_COLOR, (head.rect.left + 5, head.rect.top + 5, head.rect.width - 10, head.rect.height - 10))
        for body in range(len(head.locations)):
            pygame.draw.rect(display, SNAKE_COLOR, (head.locations[body]))
        pygame.display.flip()
        
        # byt till rows and collumns.