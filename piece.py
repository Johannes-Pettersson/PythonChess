import pygame
from enum import Enum

IMAGES_PATH = "assets/"

class PieceType(Enum):
    KING = "k"
    QUEEN = "q"
    BISHOP = "b"
    KNIGHT = "n"
    PAWN = "p"

class PieceColor(Enum):
    BLACK = "b"
    WHITE = "w"

class Piece():
    def __init__(self, parent_screen, x, y, piece_type: PieceType, piece_color: PieceColor) -> None:
        self.parent_screen = parent_screen
        self.x = x
        self.y = y
        self.piece_type = piece_type
        self.piece_color = piece_color

    def draw(self):
        image = pygame.image.load(f"{IMAGES_PATH}{self.piece_color.value}{self.piece_type.value}.png")
        image = pygame.transform.smoothscale(image, (self.parent_screen.get_width()/8, self.parent_screen.get_height()/8))
        self.parent_screen.blit(image, (self.x, self.y))