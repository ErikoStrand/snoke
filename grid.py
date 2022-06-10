import pygame
import numpy as np
class Grid:
    def __init__(self, col: int, width: int, height: int):
        self.width = width
        self.height = height
        self.y = col + 2
        self.x = col 
        self.board = np.zeros((self.x, self.y))
        self.square_size = self.width/self.y
        self.grid = np.zeros((self.x, self.y), pygame.Rect)
        self.apple = pygame.image.load("apple.png")
        self.apple = pygame.transform.scale(self.apple, (self.square_size - 10, self.square_size - 10))
        self.apple_locations = []
        print(self.x, self.y, self.square_size)
        print(self.width/self.y, self.height/self.x)
        print(self.board, "\n", self.grid)
        
    def create_grid(self):
        for x in range(self.x):
            for y in range(self.y):
            # left top width height
                self.grid[x][y] = (pygame.Rect(self.square_size * y, self.square_size * x, self.square_size, self.square_size))
                #print(self.square_size * x, self.square_size * y)
        print(self.x, self.y)        
        #print(len(self.grid))       
        #print(self.board)
        #print(self.grid)           
    def draw_grid(self, display):
        switch = True
        grid_color1 = (170,215,81)
        grid_color2 = (162,209,73)
        for x in range(self.x):
            for y in range(self.y):
                if not switch:
                    pygame.draw.rect(display, grid_color1, self.grid[x][y])
                    switch = not switch
                elif switch:
                    pygame.draw.rect(display, grid_color2, self.grid[x][y])
                    switch = not switch
                
    def random_apple(self):
        x = np.random.randint(0, self.x)
        y = np.random.randint(0, self.y)
        #print(x, y)
        if self.board[x][y] == 0:
            self.board[x][y] = 2
            self.apple_locations.append([x, y])
            #print(self.board)
            
    def draw_apples(self, display):
        for x in range(self.x):
            for y in range(self.y):
                if self.board[x][y] == 2:
                    display.blit(self.apple, (self.grid[x][y].left + 5, self.grid[x][y].top + 5))