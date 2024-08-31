from coordinate import Coordinate
from globals import IMAGES_PATH
import pygame

class MoveIndication():
    def __init__(self, taken=False) -> None:
        self.taken = taken

    def draw(self, screen, coordinate: Coordinate):
        if self.taken:
            image = pygame.image.load(f"{IMAGES_PATH}taken.png")
        else:
            image = pygame.image.load(f"{IMAGES_PATH}nottaken.png")

        image = pygame.transform.smoothscale(image, (screen.get_width()/8, screen.get_height()/8))
        screen.blit(image, (coordinate.col * (screen.get_width()/8), coordinate.row * screen.get_height()/8))