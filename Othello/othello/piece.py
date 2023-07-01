import pygame
from .constants import BLACK, WHITE, SQUARE_SIZE, GREY

class Piece:

    PADDING = 20
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col

        # mallon to color tha prepei na allazei analoga me kapoio attribute pou deixnei se poio paikti anikei
        # dhl tou if self.opponent = 1 then self.color = white else if self.opponent == 2 then self.color = black
        self.color = color 
        self.x = 0
        self.y = 0
        self.calc_pos()
    
    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.color == other
        return super().__eq__(other)

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2 
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING   
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)

    def get_position(self):
        return (self.row, self.col)

    def get_color(self):
        return self.color
    
    def change_color(self):
        if self.color == BLACK:
            self.color == WHITE
        elif self.color == WHITE:
            self.color == BLACK

    def __repr__(self):
        return str(self.color)