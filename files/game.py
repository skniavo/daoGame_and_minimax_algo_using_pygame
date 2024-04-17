import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from files.board import Board

class Game:
    def __init__(self, win) -> None:
        self._init() #calls the private init method
        self.win = win
        
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
        
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        
    def reset(self):
        self._init()
        
    def select(self, row, col):
        if self.selected: # if smth is selected
            result = self._move(row, col) #try to move it, may be false if red's trun and white piece is selected
            if not result: #if that does not work, 
                self.selected = None #get rid of our current selection
                self.select(row, col) #reselect something else and do the rest
        else:
            piece = self.board.get_piece(row, col)
            
            if piece != 0 and piece.color == self.turn: 
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True

        return False
            
              
    
    def _move(self, row, col):
        #12:56
        piece = self.board.get_piece(row,col) #Place we want to go
        if self.selected and piece == 0 and (row,col) in self.valid_moves: #smth is selected, place does not contain piece, and (row,col) in valid moves
            self.board.move(self.selected, row, col) #Move the selected piece where we want to go
            self.change_turn()
            self.valid_moves = {}
            
        else: 
            return False
        return True
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)
            
    
    def change_turn(self):
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
        