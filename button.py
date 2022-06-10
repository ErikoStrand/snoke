import pygame
class button:
    def __init__(self, text, font_size, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.heigth = height
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        while 1:
            font =  pygame.font.Font("PokemonGB.ttf", self.font_size)
            x, y = pygame.font.Font.size(font, self.text)
            if x > self.width:
                self.font_size -= 1
            if x <= self.width:
                break

    def draw_button(self, display, text_color, button_color, background):
        font = pygame.font.Font("PokemonGB.ttf", self.font_size)
        draw = font.render(self.text, False, text_color)
        if background:
            pygame.draw.rect(display, button_color, self.rect)
        display.blit(draw, (self.x + 3, self.y + self.heigth/2.7))        

    def update(self, event, display, active, background):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if background:
                    pygame.draw.rect(display, active, self.rect)
                elif not background:
                    self.draw_button(display, active, active, False)
                pygame.display.flip()
                pygame.time.wait(200)
                return True