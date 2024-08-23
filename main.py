import pygame
from board import Board
from piece import Piece, PieceColor, PieceType

# pygame setup
pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("lightgrey")

    # RENDER YOUR GAME HERE
    board = Board(screen, width=screen.get_width(), height=screen.get_height())
    board.draw()
    piece = Piece(screen, 0,0, PieceType.KNIGHT, PieceColor.WHITE)
    piece.draw()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()