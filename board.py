import pygame
from piece import Piece, PieceColor, PieceType
from coordinate import Coordinate
from typing import Tuple, Union
from move_indication import MoveIndication

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

    def getValidMovesOfPiece(self, coordinate_of_piece: Coordinate) -> list:
        piece = self.getPiece(coordinate=coordinate_of_piece)

        valid_moves = []

        if piece.piece_type == PieceType.PAWN:
            # Append all valid moves for pawn to valid_moves
            if piece.piece_color == PieceColor.WHITE:
                # one step forward
                move = Coordinate(row=coordinate_of_piece.row-1, col=coordinate_of_piece.col)
                if move.isInsideBoard() and self.getPiece(move) is None:
                    valid_moves.append(move)

                # two steps forward
                if coordinate_of_piece.row == 6:
                    move = Coordinate(coordinate_of_piece.row-2, coordinate_of_piece.col)
                    if len(valid_moves) == 1 and self.getPiece(move) is None:
                        valid_moves.append(move)

                # left diagonal move
                move = Coordinate(coordinate_of_piece.row-1, coordinate_of_piece.col-1)
                if (move.isInsideBoard() and self.getPiece(move) is not None and self.getPiece(move).piece_color.value != piece.piece_color.value) or (self.en_passant_targets is not None and self.en_passant_targets.literal == move.literal):
                    valid_moves.append(move)

                # right diagonal move 
                move = Coordinate(coordinate_of_piece.row-1, coordinate_of_piece.col+1)
                if (move.isInsideBoard() and self.getPiece(move) is not None and self.getPiece(move).piece_color.value != piece.piece_color.value) or (self.en_passant_targets is not None and self.en_passant_targets.literal == move.literal):
                    valid_moves.append(move)  
            else:
                #Black:
                # one step forward
                move = Coordinate(coordinate_of_piece.row+1, coordinate_of_piece.col)
                if move.isInsideBoard() and self.getPiece(move) is None:
                    valid_moves.append(move)

                # two steps forward
                if coordinate_of_piece.row == 1:
                    move = Coordinate(coordinate_of_piece.row+2, coordinate_of_piece.col)
                    if len(valid_moves) == 1 and self.getPiece(move) is None:
                        valid_moves.append(move)

                # left diagonal move
                move = Coordinate(coordinate_of_piece.row+1, coordinate_of_piece.col-1)
                if (move.isInsideBoard() and self.getPiece(move) is not None and self.getPiece(move).piece_color.value != piece.piece_color.value) or (self.en_passant_targets is not None and self.en_passant_targets.literal == move.literal):
                    valid_moves.append(move)

                # right diagonal move 
                move = Coordinate(coordinate_of_piece.row+1, coordinate_of_piece.col+1)
                if (move.isInsideBoard() and self.getPiece(move) is not None and self.getPiece(move).piece_color.value != piece.piece_color.value) or (self.en_passant_targets is not None and self.en_passant_targets.literal == move.literal):
                    valid_moves.append(move) 

        elif piece.piece_type == PieceType.KNIGHT:
            # Append all valid moves for knight to valid_moves
            pass
        elif piece.piece_type == PieceType.BISHOP:
            # Append all valid moves for bishop to valid_moves
            pass
        elif piece.piece_type == PieceType.ROOK:
            # Append all valid moves for rook to valid_moves
            pass
        elif piece.piece_type == PieceType.QUEEN:
            # Append all valid moves for queen to valid_moves
            pass
        elif piece.piece_type == PieceType.KING:
            # Append all valid moves for king to valid_moves
            pass

        # Perform all valid_moves on copy of Boardstate and check if king is checked in any of the cases in that case, remove the move
        moves_to_remove = []
        for move in valid_moves:
            new_boardstate = BoardState()
            new_boardstate.applyFEN(self.createFEN())
            new_boardstate.movePiece(coordinate_of_piece, move)
            if new_boardstate.kingIsChecked(self.getPiece(coordinate_of_piece).piece_color):
                moves_to_remove.append(move)

        for move in moves_to_remove:
            valid_moves.remove(move)

        return valid_moves


    def kingIsChecked(self, color_of_king: PieceColor) -> bool:
        king_coordinates = None
        for row in range(8):
            for col in range(8):
                if self.pieces[row][col] is not None and self.pieces[row][col].piece_color.value == color_of_king.value and self.pieces[row][col].piece_type == PieceType.KING:
                    king_coordinates = Coordinate(row, col)
                    break
            if king_coordinates is not None:
                break    
        assert king_coordinates is not None, "No king was found"
        
        # check if pawn is checking king
        if color_of_king == PieceColor.WHITE:
            pawn_coordinate = Coordinate(king_coordinates.row-1, king_coordinates.col-1)
            pawn = self.getPiece(pawn_coordinate)
            if pawn is not None and pawn.piece_type == PieceType.PAWN and pawn.piece_color.value != color_of_king.value:
                return True
            
            pawn_coordinate = Coordinate(king_coordinates.row-1, king_coordinates.col+1)
            pawn = self.getPiece(pawn_coordinate)
            if pawn is not None and pawn.piece_type == PieceType.PAWN and pawn.piece_color.value != color_of_king.value:
                return True
        else:
            pawn_coordinate = Coordinate(king_coordinates.row+1, king_coordinates.col-1)
            pawn = self.getPiece(pawn_coordinate)
            if pawn is not None and pawn.piece_type == PieceType.PAWN and pawn.piece_color.value != color_of_king.value:
                return True
            
            pawn_coordinate = Coordinate(king_coordinates.row+1, king_coordinates.col+1)
            pawn = self.getPiece(pawn_coordinate)
            if pawn is not None and pawn.piece_type == PieceType.PAWN and pawn.piece_color.value != color_of_king.value:
                return True
        
        return False

    def movePiece(self, from_coordinate: Coordinate, to_coordinate: Coordinate):
        self.setPiece(to_coordinate, self.getPiece(from_coordinate))
        self.setPiece(from_coordinate, None)


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
        self.currently_shown_valid_moves = []

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

        for move in self.currently_shown_valid_moves:
            MoveIndication(self.board_state.getPiece(move) is not None).draw(self.parent_screen, move)          

    def coordinateFromPixelcords(self, pixel_coords: Tuple[int, int]):
        return Coordinate(row=int((pixel_coords[1]-self.y) / (self.height/8)), col=int((pixel_coords[0]-self.x) / (self.width/8)))

    def clicked(self, pos):
        self.currently_shown_valid_moves = self.board_state.getValidMovesOfPiece(self.coordinateFromPixelcords(pos))
