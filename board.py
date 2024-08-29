import pygame
from piece import Piece, PieceColor, PieceType
from coordinate import Coordinate
from typing import Union

class CastleRights():
    def __init__(self, white_kingside=True, white_queenside=True, black_kingside=True, black_queenside=True, fen=None) -> None:
        self.white_kingside = white_kingside
        self.white_queenside = white_queenside
        self.black_kingside = black_kingside
        self.black_queenside = black_queenside

        if fen is not None:
            self.applyFEN(fen)

    def getFEN(self) -> str:
        fen = ""
        if self.white_kingside:
            fen += "K"
        if self.white_queenside:
            fen += "Q"
        if self.black_kingside:
            fen += "k"
        if self.black_queenside:
            fen += "q"
        if fen == "":
            fen = "-"

        return fen
    
    def applyFEN(self, fen: str):
        self.white_kingside = "K" in fen
        self.white_queenside = "Q" in fen
        self.black_kingside = "k" in fen
        self.black_queenside = "q" in fen


class BoardState():
    def __init__(self) -> None:
        self.pieces = [None] * 8
        for i in range(8):
            self.pieces[i] = [None] * 8

        self.whites_turn = True
        self.castle_rights = CastleRights()
        self.en_passant_targets: Union[Coordinate, None] = None
        self.halfmove_clock = 0
        self.fullmove_number = 0

    def getPiece(self, coordinate: Coordinate) -> Union[Piece, None]:
        return self.pieces[coordinate.row][coordinate.col]
    
    def setPiece(self, coordinate: Coordinate, piece):
        self.pieces[coordinate.row][coordinate.col] = piece

    def createFEN(self) -> str:
        fen = ""
        # First FEN Field
        for row in self.pieces:
            number_of_empty = 0
            for element in row:
                if element is None:
                    number_of_empty += 1
                else:
                    if number_of_empty > 0:
                        fen += str(number_of_empty)
                        number_of_empty = 0
                    fen += element.literal
            if number_of_empty > 0:
                fen += str(number_of_empty)
            fen += "/"

        fen = fen[:-1] + " "

        # Second FEN Field
        if self.whites_turn:
            fen += "w"
        else:
            fen += "b"

        fen += " "

        # Third FEN Field
        fen += self.castle_rights.getFEN()

        fen += " "

        # Fourth FEN Field
        fen += "-" if self.en_passant_targets is None else self.en_passant_targets.literal
        
        fen += " "

        # Fifth FEN Field
        fen += str(self.halfmove_clock)

        fen += " "
        
        # Sixth FEN Field
        fen += str(self.fullmove_number)
        
        return fen

    def applyFEN(self, fen: str):
        fen_fields = fen.split(" ")
        current_col = 0
        current_row = 0
        for character in fen_fields[0]:
            if character.isdigit():
                current_col += int(character)
            elif character == "/":
                current_row += 1
                current_col = 0
            else:
                piece = Piece(PieceType.KING, PieceColor.WHITE)
                piece.applyLiteral(character)
                self.pieces[current_row][current_col] = piece
                current_col += 1

        self.whites_turn = fen_fields[1] == "w"

        self.castle_rights.applyFEN(fen_fields[2])

        self.en_passant_targets = None if fen_fields[3] == "-" else Coordinate(literal=fen_fields[3])

        self.halfmove_clock = int(fen_fields[4])

        self.fullmove_number = int(fen_fields[5])         


class Board():
    def __init__(self, parent_screen, board_state: BoardState, x=0, y=0, width=0, height=0, light_color="#EFDAB4", dark_color="#B38860") -> None:
        self.parent_screen = parent_screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.light_color = light_color
        self.dark_color = dark_color
        self.board_state = board_state

    def draw(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.parent_screen, self.light_color, pygame.Rect(self.x + (j * self.width/8), self.y + (i * self.height/8), self.width/8, self.height/8))
                else:
                    pygame.draw.rect(self.parent_screen, self.dark_color, pygame.Rect(self.x + (j * self.width/8), self.y + (i * self.height/8), self.width/8, self.height/8))

                current_piece = self.board_state.getPiece(Coordinate(row=i, col=j))
                if current_piece is not None:
                    current_piece.draw(screen=self.parent_screen, coordinate=Coordinate(row=i, col=j))


