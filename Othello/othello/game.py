import pygame
from .constants import BLACK, WHITE, BLUE, SQUARE_SIZE, ROWS, COLS, RED
from othello.board import Board
from .piece import Piece

LEFT = (0, -1)
TOP_LEFT = (-1, -1)
TOP = (-1, 0)
TOP_RIGHT = (-1, 1) 
RIGHT = (0, 1)
BOTTOM_RIGHT = (1, 1)
BOTTOM = (1, 0)
BOTOTM_LEFT = (1, -1)       

DIRECTIONS = (TOP_LEFT   , TOP   ,    TOP_RIGHT,
              LEFT       ,                RIGHT, 
              BOTOTM_LEFT, BOTTOM, BOTTOM_RIGHT)

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        # self.draw_opponent_neighbors(self.opponent_neighbors)
        pygame.display.update()
    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.black_count = 2 
        self.white_count = 2
        self.valid_moves = set()
        self.opponent_neighbors = set()

    def reset(self):
        self._init()
    
    def step(self, row, col):
        initial_blacks = len(self.board.black_pieces_coordinates)
        initial_whites = len(self.board.white_pieces_coordinates)

        self._spawn_piece(row, col)

        next_state = self.board.board
        reward = self.white_count - initial_whites
        done = True

        return next_state, reward, done 

    def _spawn_piece(self, row, col):   

        if (row, col) in self.valid_moves:  
            self.board.spawn_piece(row, col, self.turn)       
            self.flip_pieces(row, col) 
            # print('BLACK: ', self.black_count, ' | WHITE: ', self.white_count)
            print('BLACK: ', len(self.board.black_pieces_coordinates), ' | WHITE: ', len(self.board.white_pieces_coordinates))
            self.change_turn()     
        else:
            print('Not a valid move!')

# PROBLEMA ME TO FLIP PIECES


    def flip_pieces(self, row, col):
        flipping_directions = set()
        piece = self.board.board[row][col]
        
        # this loop starts from the spawned piece position and extends to all directions while it finds oppponent pieces
        # if it a finds the current player's piece along this path, all oppponent piece in this path should be flip,
        # so the direction is stored

        for direction in DIRECTIONS:
            neighbor_position = tuple(x + y for x, y in zip((row, col), direction))
            if(neighbor_position[0] >= 0 and neighbor_position[1] >= 0 and
               neighbor_position[0] < ROWS and neighbor_position[1] < ROWS):
                next_piece = self.board.get_piece(neighbor_position[0], neighbor_position[1])

                while(next_piece == self.get_opponent()):
                    next_piece_coordinates = tuple(x + y for x, y in zip(next_piece.get_position(), direction))
                    if(next_piece_coordinates[0] < ROWS and next_piece_coordinates[1] < ROWS and
                       next_piece_coordinates[0] >= 0 and next_piece_coordinates[1] >= 0):
                           next_piece = self.board.get_piece(next_piece_coordinates[0], next_piece_coordinates[1])
                    else:
                        break
                    
                    if next_piece == self.turn:
                       flipping_directions.add(direction)

        # we iterate once again from the spawned piece position, only to the flipping direction,
        # we flip all enemy piece along this path

        for direction in flipping_directions:
            neighbor_position = tuple(x + y for x, y in zip((row, col), direction))
            if(neighbor_position[0] >= 0 and neighbor_position[1] >= 0 and
               neighbor_position[0] < ROWS and neighbor_position[1] < ROWS):
                next_piece = self.board.get_piece(neighbor_position[0], neighbor_position[1])
                next_piece_coordinates = neighbor_position
                print(next_piece_coordinates)

                while( next_piece == self.get_opponent() ):
                    self.board.get_player_pieces(self.turn).add(next_piece.get_position())
                    # self.change_score()
                    self.board.get_opponent_pieces(self.turn).remove(next_piece.get_position())
                    self.board.board[next_piece.get_position()[0]][next_piece.get_position()[1]] = Piece(next_piece_coordinates[0], next_piece_coordinates[1], self.turn)
                    
                    # added numbers board
                    pos  = next_piece.get_position()   

                    if self.turn == WHITE:
                        self.board.board_QTable[pos[0]][pos[1]] = 1
                    elif self.turn == BLACK:
                        self.board.board_QTable[pos[0]][pos[1]] = -1
                    
                    # end of initial numbes board addition

                    next_piece_coordinates = tuple(x + y for x, y in zip((next_piece_coordinates[0], next_piece_coordinates[1]), direction))
                    next_piece = self.board.get_piece(next_piece_coordinates[0], next_piece_coordinates[1])

    def change_turn(self):
        
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK
        
        self.valid_moves=self.get_valid_moves()

        if(len(self.valid_moves)) == 0:
            if( len(self.board.black_pieces_coordinates) +  len(self.board.white_pieces_coordinates) == 64):
              print('The game ended!')
              print('FINAL SCORE: ', 'BLACK: ', len(self.board.black_pieces_coordinates), ' | WHITE: ', len(self.board.white_pieces_coordinates))
              if(len(self.board.black_pieces_coordinates) > len(self.board.white_pieces_coordinates)):
                print('BLACK HAS WON')
              elif(len(self.board.white_pieces_coordinates) > len(self.board.black_pieces_coordinates)):
                print('WHITE HAS WON')  
              elif(len(self.board.white_pieces_coordinates) == len(self.board.black_pieces_coordinates)):
                print('IT IS A TIE')
              else:
                print('Error calculating score')  
              
            else:  
                self.change_turn()
                print('----||||||----')
                print('~~~~~~~~~~~~~~')
                print('NO VALID MOVES')
                print('IT IS ', self.turn, '`s turn again!')
                print('~~~~~~~~~~~~~~')
                print('----||||||----')
        
    def get_valid_moves(self):
        opponent_adjuscent_cells = set()
        moves = set()

        for piece in self.board.get_opponent_pieces(self.turn):
            for direction in DIRECTIONS:
                neighbor=self.get_opponents_neighbors(piece, direction, opponent_adjuscent_cells)
                if(neighbor != None):
                    opponent_adjuscent_cells.add(neighbor)

        #mexri edw doylevei kala pernw ola ta adjuscent cells tou antipalou
        self.opponent_neighbors = opponent_adjuscent_cells

        for opponent_adjuscent_cell in opponent_adjuscent_cells:   
            for direction in DIRECTIONS:
                possible_move = tuple(x + y for x, y in zip(opponent_adjuscent_cell, direction))
                if (possible_move[0] < ROWS and possible_move[1] < ROWS and
                    possible_move[0] >= 0 and possible_move[1] >= 0):   
                    
                    next_piece = self.board.get_piece(possible_move[0], possible_move[1])

                    while(next_piece == self.get_opponent()):
                         next_piece_coordinates = tuple(x + y for x, y in zip(next_piece.get_position(), direction))
                         if(next_piece_coordinates[0] < ROWS and next_piece_coordinates[1] < ROWS and
                            next_piece_coordinates[0] >= 0 and next_piece_coordinates[1] >= 0):
                                next_piece = self.board.get_piece(next_piece_coordinates[0], next_piece_coordinates[1])
                         else:
                             break
                         
                         if next_piece == self.turn:
                            moves.add(opponent_adjuscent_cell)

        return moves

    def get_opponents_neighbors(self, piece, direction, moves):
        neighbor = tuple(x + y for x, y in zip(piece, direction))

        if neighbor not in moves:
            if(neighbor[0] >= 0 and neighbor[1] >= 0 and neighbor[0] < ROWS and neighbor[1] < ROWS):
                if(self.board.get_piece(neighbor[0], neighbor[1]) != None):
                    if self.board.get_piece(neighbor[0], neighbor[1]) == 0:
                        return neighbor

    def get_opponent(self):
        if self.turn == BLACK:
            return WHITE
        elif self.turn == WHITE :
            return BLACK
    
    def change_score(self):
        if self.turn == BLACK:
            self.black_count += 1
            self.white_count -= 1
        elif self.turn == WHITE:
            self.white_count += 1
            self.black_count -= 1
        
    def get_piece_count(self):
        if self.turn == BLACK:
            return self.black_count
        elif self.turn == WHITE:
            return self.white_count

    def next_piece_in_direction(self, current_tile, direction):
        next_piece = tuple(x + y for x, y in zip(current_tile, direction))

        if(next_piece[0] > ROWS - 1 or next_piece[1] > ROWS - 1 or
           next_piece[0] < 0 or next_piece[1] < 0):
            return False

        if(self.board.get_piece(next_piece[0], next_piece[1]) == self.get_opponent()):
            self.next_piece_in_direction(next_piece, direction)
        elif(self.board.get_piece(next_piece[0], next_piece[1]) == self.turn):
            return True
        else:
            return False    

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)
    
    def draw_opponent_neighbors(self, opponent_neighbors):
        for move in opponent_neighbors:
            row, col = move
            pygame.draw.circle(self.win, RED, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 10)