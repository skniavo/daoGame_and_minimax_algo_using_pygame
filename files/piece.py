import pygame
from .constants import *



class Piece:
    PADDING = 20 #Dist between the edge of the square and the edge of the circle
    OUTLINE =  2 #Epaisseur pour faire genre c'est un border
    def __init__(self,row,col,color):
        self.row = row
        self.col = col
        self.color = color
        #proper to checker:
        self.king = False
        
        self.x = 0
        self.y = 0
        
        #We will need to adapt this direction
        self.direction = (self.x, self.y)
        
        self.calc_pos()
        
        
    def calc_pos(self):
        """Calculates center position over which we draw the circle piece"""
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE// 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE// 2
        
    #Proper to checker, really don't need:
    def make_king(self):
        self.king= True
        
    def draw(self, win):
        """draw the circles"""
        radius =  SQUARE_SIZE //2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE) #Larger circle to make border
        pygame.draw.circle(win, self.color, (self.x, self.y), radius )
        
    def __repr__(self) -> str:
        return str(self.color)
        
        