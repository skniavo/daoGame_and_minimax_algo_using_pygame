import pygame
from .constants import RED, WHITE
from files.board import Board

class Game:
    def __init__(self, win) -> None:
        self._init() #calls the private init method
        self.win = win
        
    def update(self):
        self.board.draw(self.win)
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
            result = self._move(row, col) #try to move it
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
        pass
        