import pygame
from board import Board, BoardState, Coordinate
from piece import Piece, PieceColor, PieceType


# pygame setup
pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True
board = Board(screen, board_state=BoardState(), width=screen.get_width(), height=screen.get_height())
board.board_state.applyFEN("rnbqkbnr/pppppppp/8/1r5K/5P4/4N3/8/RNBQ1BNR w KQkq - 0 0")
print(board.board_state.kingIsChecked(PieceColor.WHITE))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                board.clicked(pygame.mouse.get_pos())

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("lightgrey")

    # RENDER YOUR GAME HERE
    board.draw()


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()