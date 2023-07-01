import pygame
from othello.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK
from othello.board import Board
from othello.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Othello ')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    game.valid_moves = game.get_valid_moves()

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game._spawn_piece(row, col)
                
                print(game.board.board_QTable)
                
        
        game.update()

    pygame.QUIT

main()