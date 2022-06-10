import pygame
class snake:
    def __init__(self, rect):
        self.x = rect.left
        self.y = rect.top
        self.width = rect.width
        self.height = rect.height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 1
        self.locations = []
        self.locationsdirection = []
        self.keys = []
        self.click = True
        self.length = 2
    def update(self, dt, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and self.click:
                if self.direction != 2:
                    self.direction = 1
            if event.key == pygame.K_LEFT and self.click:
                if self.direction != 1:
                    self.direction = 2
            if event.key == pygame.K_DOWN and self.click:
                if self.direction != 3:
                    self.direction = 4
            if event.key == pygame.K_UP and self.click:
                if self.direction != 4:
                    self.direction = 3
                        
        if event.type == pygame.KEYUP:
            self.click = True
            
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)