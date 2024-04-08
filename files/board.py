import pygame
from .constants import BLACK, ROWS, COLS, RED, SQUARE_SIZE, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        # red_left, white_left red_kings, white_kings are proer to checkers
        self.red_left = self.white_left = 4 
        self.red_kings = self.white_kings = 0
        self.create_board()
        
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, RED,(row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row == col:
                    self.board[row].append(Piece(row, col, WHITE))
                elif row + col == COLS -1:
                    self.board[row].append(Piece(row, col, RED))
                else:
                    self.board[row].append(0)
          
    def draw(self, win):
        self.draw_squares(win) #draw the squares
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
                 
                