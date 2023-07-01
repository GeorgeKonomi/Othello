import pygame
from .constants import BLACK, WHITE, ROWS, COLS, RED, COFFEE, CAMEL, SQUARE_SIZE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.board_QTable = [[0, 0, 0, 0, 0, 0, 0, 0], 
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, -1, 0, 0, 0],
                            [0, 0, 0, -1, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],                      
                           ] #
        self.black_count = self.white_count = 2
        self.black_pieces_coordinates = set()
        self.white_pieces_coordinates = set()
        self.create_board()
        
    def draw_squares(self, win):
        win.fill(COFFEE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, CAMEL, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def get_piece(self, row, col):
        return self.board[row][col]
    
    def get_player_pieces(self, color):
        if color == BLACK:
            return self.black_pieces_coordinates
        elif color == WHITE:
            return self.white_pieces_coordinates

    def get_opponent_pieces(self, color):
        if color == WHITE:
            return self.black_pieces_coordinates
        elif color == BLACK:
            return self.white_pieces_coordinates  

    def get_piece_count(self, color):
        if color == BLACK:
            return self.black_count
        elif color == WHITE:
            return self.white_count

    def spawn_piece(self, row, col, color):
        piece = Piece(row, col, color)

        if(self.board[row][col] != 0):
            print('Invalid move! The tile (', row, ', ', col, ') is already taken')
        else:    
            self.board[row][col] = piece
            if(color == BLACK):
                self.black_pieces_coordinates.add((row, col))
                print("print1: ", self.board_QTable[row][col])
                print("print2: ", self.board_QTable[row][col])
                self.board_QTable[row][col] = -1 # added for RL
                self.black_count += 1
            elif(color == WHITE):
                self.white_pieces_coordinates.add((row, col))
                self.board_QTable[row][col] = 1 # added for RL
                self.white_count += 1

    def flip_piece(self, row, col):
        self.board[row][col].change_color()

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if((row == 3 and col == 3) or (row == 4 and col == 4)):
                    piece = Piece(row, col, WHITE)
                    self.board[row].append(piece)
                    # self.board_QTable = 1  # 1 refers to white pieces
                    self.white_pieces_coordinates.add(piece.get_position())
                elif((row == 3 and col == 4) or (row == 4 and col == 3)):
                    piece = Piece(row, col, BLACK)
                    self.board[row].append(piece)
                    # self.board[row] = -1 # -1 refers to black pieces
                    self.black_pieces_coordinates.add(piece.get_position())                  
                else:
                    self.board[row].append(0)
                    # self.board_QTable[row] = 0 # 0 refers to non-occupied board positions

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)