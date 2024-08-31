import pygame
from enum import Enum
from coordinate import Coordinate
from globals import IMAGES_PATH

class PieceType(Enum):
    KING = "k"
    QUEEN = "q"
    BISHOP = "b"
    KNIGHT = "n"
    PAWN = "p"
    ROOK = "r"

class PieceColor(Enum):
    BLACK = "b"
    WHITE = "w"

class Piece():
    def __init__(self, piece_type: PieceType, piece_color: PieceColor) -> None:
        self.piece_type = piece_type
        self.piece_color = piece_color
        if self.piece_color is PieceColor.WHITE:
            self.literal = self.piece_type.value.upper()
        else:
            self.literal = self.piece_type.value

    def draw(self, screen, coordinate: Coordinate):
        image = pygame.image.load(f"{IMAGES_PATH}{self.piece_color.value}{self.piece_type.value}.png")
        image = pygame.transform.smoothscale(image, (screen.get_width()/8, screen.get_height()/8))
        screen.blit(image, (coordinate.col * (screen.get_width()/8), coordinate.row * screen.get_height()/8))

    def applyLiteral(self, literal: str):
        if literal.upper() == literal:
            self.piece_color = PieceColor.WHITE
        else:
            self.piece_color = PieceColor.BLACK
        
        self.piece_type = PieceType(literal.lower())

        self.literal = literal