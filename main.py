import pygame
from files.constants import WIDTH,HEIGHT, SQUARE_SIZE, RED
from files.board import Board
from files.game import Game

FPS = 60
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('dao game by Liantsoa')

def get_row_col_from_mouse(pos):
    """identifies row and col values 
    when pressing mouse down"""
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col 

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    
    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos() # get mouse position
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col) 
                
                
        game.update()              
    pygame.quit()
        
main()