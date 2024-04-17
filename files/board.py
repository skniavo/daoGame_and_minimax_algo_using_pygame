import pygame
from .constants import BLACK, ROWS, COLS, RED, SQUARE_SIZE, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        # red_left, white_left red_kings, white_kings are proer to checkers
        self.red_left = self.white_left = 4 
        self.red_kings = self.white_kings = 0
        self.create_board()
        
    def move(self,piece,row,col):
        # self.board[piece.row][piece.col] is where the piece is
        # self.board[row][col] is where we want to go
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col] #swap
        piece.move(row,col)
        
        
        
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, RED,(row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
    def get_piece(self,row,col):
        return self.board[row][col]
                
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
                   
    def get_valid_moves(self, piece):
        moves = {}
        DIRECTIONS = [[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]]
        
        for d in DIRECTIONS:
            r, c = piece.row, piece.col
            last_valid = None
            while True:
                r += d[0]
                c += d[1]
                if 0 <= r < ROWS and 0 <= c < COLS:
                    if self.board[r][c] != 0:  # Vérifie s'il y a un obstacle
                        break
                    last_valid= (r,c)
                else:
                    break  # Arrête la boucle si on sort des limites du plateau
            if last_valid:
                moves[last_valid]=[]
        return moves


    
    



                
            
            
             
        
        
        
        
         
                 
                