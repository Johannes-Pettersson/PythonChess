import pygame

class Board():
    def __init__(self, parent_screen, x=0, y=0, width=0, height=0, light_color="#EFDAB4", dark_color="#B38860") -> None:
        self.parent_screen = parent_screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.light_color = light_color
        self.dark_color = dark_color

    def draw(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.parent_screen, self.light_color, pygame.Rect(self.x + (j * self.width/8), self.y + (i * self.height/8), self.width/8, self.height/8))
                else:
                    pygame.draw.rect(self.parent_screen, self.dark_color, pygame.Rect(self.x + (j * self.width/8), self.y + (i * self.height/8), self.width/8, self.height/8))
