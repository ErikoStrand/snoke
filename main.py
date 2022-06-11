import pygame, sys
from grid import Grid
from snake import snake
from button import button
import numpy as np
import pickle
# pygame init
WIDTH, HEIGHT = 850, 750
grid = Grid(15, WIDTH, HEIGHT)      
grid.create_grid()
head = snake(grid.grid[0][0])
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
# values
BACKGROUND = (76, 76, 76)
SNAKE_COLOR = (68, 113, 230)
DEACTIVE = (200, 200, 200)
ACTIVE = (150, 150, 150)
SNAKE_BODY = []
MOVE_SNAKE = pygame.USEREVENT
SAVE_TIMER = pygame.USEREVENT + 2
PLAY_TIME = pygame.USEREVENT + 1
STATS_FONT = pygame.font.Font("PokemonGB.ttf", 30)
# toggles
MAIN_MENU = True
RUNNING = False
RETRY = False
STATS = False
# work
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_icon(grid.apple)
pygame.display.set_caption("Snoke")
pygame.time.set_timer(MOVE_SNAKE, 200)
pygame.time.set_timer(SAVE_TIMER, 2500)
pygame.time.set_timer(PLAY_TIME, 1000)
# buttons
RETRY_BUTTON = button("Retry?", 50, WIDTH/2 - 100/2, HEIGHT/2.3, 100, 25)
RETURN_BUTTON = button("Return", 50, WIDTH/2 - 100/2, HEIGHT/2.1, 100, 25)
TITLE = button("Snoke", 70, WIDTH/2 - 150, 100, 300, 50)
START_BUTTON = button("Start", 30, WIDTH/2 - 100/2, HEIGHT/3, 100, 50)
STATS_BUTTON = button("Stats", 30, WIDTH/2 - 100/2, HEIGHT/2.5, 100, 50)
BACK_BUTTON = button("Back", 20, 10, 10, 50, 25)

#STATS_VALUES = {0: ["Apples: ", 0, ""], 1: ["Highscore: ", 0, ""], 2: ["Distance: ", 0, " m"], 3: ["Timeplayed: ", 0, " s"]}

#with open("STATS_VALUES.dat", "wb") as f:
    #pickle.dump(STATS_VALUES, f)
     
with open("STATS_VALUES.dat", "rb") as f:
    STATS_VALUES = pickle.load(f)
    print(STATS_VALUES)
     
def draw_text(text, font_size, color, x, y):
    font = pygame.font.Font("PokemonGB.ttf", font_size)
    a, b = pygame.font.Font.size(font, str(text))
    draw = font.render(str(text), False, color)
    display.blit(draw, (x - a/2, y))
    
def draw_stats():
    for i in range(len(list(STATS_VALUES))): 
        a, b = pygame.font.Font.size(STATS_FONT, str(STATS_VALUES[i][0]) + str(int(STATS_VALUES[i][1])) + str(STATS_VALUES[i][2]))
        draw = STATS_FONT.render(str(STATS_VALUES[i][0] + str(int(STATS_VALUES[i][1])) + str(STATS_VALUES[i][2])), False, (150, 150, 150))
        display.blit(draw, (WIDTH/2 - a/2, 75 * i + 75))       
          
while MAIN_MENU:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if START_BUTTON.update(event, display, ACTIVE, False):
            head = snake(grid.grid[0][0])
            head.direction = 0
            MAIN_MENU = False
            RUNNING = True
            grid.random_apple(5)
        if STATS_BUTTON.update(event, display, ACTIVE, False):
            MAIN_MENU = False
            STATS = True    
    display.fill(BACKGROUND)
    TITLE.draw_button(display, DEACTIVE, DEACTIVE, False)
    START_BUTTON.draw_button(display, DEACTIVE, DEACTIVE, False)
    STATS_BUTTON.draw_button(display, DEACTIVE, DEACTIVE, False)
    pygame.display.flip()
    
    while STATS:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        if BACK_BUTTON.update(event, display, ACTIVE, False):
            MAIN_MENU = True
            STATS = False
                    
        display.fill(BACKGROUND)
        BACK_BUTTON.draw_button(display, DEACTIVE, DEACTIVE, False)
        draw_stats()     
           
        pygame.display.flip()
    while RUNNING:
        dt = clock.tick(120) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOVE_SNAKE and not RETRY:
                print(grid.board)
                if len(head.keys) >= 1:
                    head.direction = head.keys[0]   
                    head.keys.pop(0)
                if head.direction == 1:
                    head.x += grid.square_size
                elif head.direction == 2:
                    head.x -= grid.square_size
                elif head.direction == 3:
                    head.y -= grid.square_size
                elif head.direction == 4:
                    head.y += grid.square_size
                if head.direction != 0:
                    STATS_VALUES[2][1] += 1
                    if len(head.locations) < head.length:
                        head.locations.append(head.rect)
                        #print(head.locations)
                        head.locationsdirection.append(head.direction)
                        if len(head.locations) == head.length:
                            head.locationsdirection.pop(0)
                            head.locations.pop(0)
                            
            if event.type == SAVE_TIMER:
                with open("STATS_VALUES.dat", "wb") as f:
                    pickle.dump(STATS_VALUES, f)   
                                 
            if event.type == PLAY_TIME:
                STATS_VALUES[3][1] += 1 
                         
            if RETRY_BUTTON.update(event, display, ACTIVE, False) and RETRY:
                grid.board = np.zeros((grid.x, grid.y))
                head = snake(grid.grid[0][0])
                head.direction = 0
                RETRY = False
                grid.apple_locations = []
                grid.random_apple(5)
                
            if RETURN_BUTTON.update(event, display, ACTIVE, False) and RETRY:
                RETRY = False
                RUNNING = False
                MAIN_MENU = True
                                  
        display.fill(BACKGROUND)
        # update
        head.update(dt, event)
        # making it so the grid.board knows where the snake is
        for count, body in enumerate(head.locations):
            for x in range(grid.x):
                for y in range(grid.y):
                    if grid.grid[x][y] == body:
                        grid.board[x][y] = 1
                    if count == 0:
                        if grid.grid[x][y] != body:
                            if grid.board[x][y] != 2:
                                grid.board[x][y] = 0
                                
        # checking snake collisions.                        
        for body in head.locations:
            if head.rect.colliderect(body):
                head.direction = 0
                RETRY = True
        if head.x < 0 or head.x > WIDTH - 50 or head.y < 0 or head.y > HEIGHT - 50:
            head.direction = 0
            RETRY = True            
        # apple
        for locations in range(len(grid.apple_locations)):
            if locations < len(grid.apple_locations):
                if head.rect.colliderect(grid.grid[grid.apple_locations[locations][0]][grid.apple_locations[locations][1]]):
                    grid.board[grid.apple_locations[locations][0]][grid.apple_locations[locations][1]] = 0
                    head.length += 1
                    STATS_VALUES[0][1] += 1
                    grid.apple_locations.pop(locations)
                    grid.random_apple(1)
               
        #drawing details
        grid.draw_grid(display)
        grid.draw_apples(display)
        
        # snake body and head
        pygame.draw.rect(display, SNAKE_COLOR, (head.rect.left, head.rect.top, head.rect.width, head.rect.height))
        for body in range(len(head.locations)):
            # 2 side 4 up down width height
            heads = list(head.locations[body])
            head_dir = head.locationsdirection[body]
            head_dir_prev = head.locationsdirection[body - 1]
            if head_dir != head_dir_prev and body != 0:
                if head_dir == 4 and head_dir_prev == 2 or head_dir == 1 and head_dir_prev == 3:
                    # left top width height
                    pygame.draw.rect(display, SNAKE_COLOR, (heads[0] + 5, heads[1] + 5, heads[2] - 5, heads[3] - 10))
                    pygame.draw.rect(display, SNAKE_COLOR, (heads[0] + 5, heads[1] + 5, heads[2] - 10, heads[3] - 5))
                if head_dir == 4 and head_dir_prev == 1 or head_dir == 2 and head_dir_prev == 3:
                    pygame.draw.rect(display, SNAKE_COLOR, (heads[0], heads[1] + 5, heads[2] - 5, heads[3] - 10))
                    pygame.draw.rect(display, SNAKE_COLOR, (heads[0] + 5, heads[1] + 5, heads[2] - 10, heads[3] - 5))
                if head_dir == 3 and head_dir_prev == 1 or head_dir == 2 and head_dir_prev == 4:
                    pygame.draw.rect(display, SNAKE_COLOR, (heads[0] + 5, heads[1], heads[2] - 10, heads[3] - 5))
                    pygame.draw.rect(display, SNAKE_COLOR, (heads[0], heads[1] + 5, heads[2] - 5, heads[3] - 10))
                if head_dir == 3 and head_dir_prev == 2 or head_dir == 1 and head_dir_prev == 4:
                    pygame.draw.rect(display, SNAKE_COLOR, (heads[0] + 5, heads[1], heads[2] - 10, heads[3] - 5))
                    pygame.draw.rect(display, SNAKE_COLOR, (heads[0] + 5, heads[1] + 5, heads[2] - 5, heads[3] - 10))
                
            elif head.locationsdirection[body] == 2 or head.locationsdirection[body] == 1:
                pygame.draw.rect(display, SNAKE_COLOR, (heads[0], heads[1] + 5, heads[2], heads[3] - 10))
            elif head.locationsdirection[body] == 4 or head.locationsdirection[body] == 3:   
                pygame.draw.rect(display, SNAKE_COLOR, (heads[0] + 5, heads[1], heads[2] - 10, heads[3]))
                
        # drawing the menu if the player has died   
        if not head.direction and RETRY:
            if head.length > STATS_VALUES[1][1]:
                STATS_VALUES[1][1] = head.length
                
            draw_text("GAME OVER", 40, (50, 50, 50), WIDTH/2, HEIGHT/3)
            RETRY_BUTTON.draw_button(display, (255, 255, 255), DEACTIVE, False)
            RETURN_BUTTON.draw_button(display, (255, 255, 255), DEACTIVE, False)
            
        # updaterar skärmen.
        pygame.display.flip()
        