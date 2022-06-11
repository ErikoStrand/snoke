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
            if len(self.keys) <= 1:
                if event.key == pygame.K_RIGHT:
                    if len(self.keys) < 1 and self.direction != 2:
                        self.keys.append(1)
                    elif len(self.keys) > 0:
                        if 1 != self.keys[0]:
                            self.keys.append(1)                    
                if event.key == pygame.K_LEFT:                
                    if len(self.keys) < 1 and self.direction != 1:
                        self.keys.append(2)
                    elif len(self.keys) > 0:
                        if 2 != self.keys[0]:
                            self.keys.append(2)                       
                if event.key == pygame.K_DOWN:                  
                    if len(self.keys) < 1 and self.direction != 3:
                        self.keys.append(4)
                    elif len(self.keys) > 0:
                        if 4 != self.keys[0]:
                            self.keys.append(4)
                if event.key == pygame.K_UP:
                    if len(self.keys) < 1 and self.direction != 4:
                        self.keys.append(3)
                    elif len(self.keys) > 0:
                        if 3 != self.keys[0]:
                            self.keys.append(3)
            
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)