import pygame
import random
from files.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from files.board import Board
from files.game import Game
from minimax.algorithm import minimax, minimax_red


def get_row_col_from_mouse(pos):
    """Identifies row and col values when pressing mouse down"""
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def two_player_game():
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('dao game by Liantsoa')
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    game_over = False

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # get mouse position
                row, col = get_row_col_from_mouse(pos)
                if game.select(row, col):
                    if game.board.check_winner(game.turn):
                        if game.turn == WHITE:
                            print(f"#####################THE WHITE HAS WON #################")
                            print("###############################################################")
                        else:
                            print(f"#####################THE RED HAS WON #################")
                            print("###############################################################")
                            
                        game_over = True
                        game.update()
                        pygame.time.delay(3000)  # Pause de _ secondes avant de fermer
                        run = False  # Stop the game loop
        if not game_over:
            game.update()
    pygame.quit()

def simple_machine_game():
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('dao game by Liantsoa')
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    game_over = False

    while run:
        clock.tick(FPS)

        if game.turn == WHITE and not game_over:
            valid_moves = game.board.get_all_valid_moves(WHITE)
            pygame.time.delay(500) 
            if valid_moves:
                piece, move = random.choice(list(valid_moves.items()))
                row, col = random.choice(move)
                game.board.move(piece, row, col)
                
                if game.board.check_winner(WHITE):
                    print(f"############THE WHITE HAS WON ##############################")
                    print("###############################################################")
                    game_over = True
                    game.update()
                    pygame.time.delay(3000)  # Pause de 3 secondes avant de fermer
                    run = False  # Stop the game loop
                game.change_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not game_over and game.turn == RED and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # get mouse position
                row, col = get_row_col_from_mouse(pos)
                if game.select(row, col):
                    if game.board.check_winner(RED):
                        print(f"#############THE RED HAS WON ###############################")
                        print("###############################################################")
                        game_over = True
                        game.update()
                        pygame.time.delay(1000) 
                        run = False  # Stop the game loop
        if not game_over:
            game.update()
    pygame.quit()

def minimax_game():
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('dao game by Liantsoa')
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    game_over = False
    
    while run:
        clock.tick(FPS)
        
        if game.turn == WHITE:
            value, new_board= minimax(game.get_board(),4, WHITE, game)
            game.ai_move(new_board)
        
        if game.board.check_winner(RED) or game.board.check_winner(WHITE):
            game_over = True
            game.update()
            pygame.time.delay(1000) 
            run = False
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
                
        if not game_over:
            game.update()
    pygame.quit()

def simple_machine_vs_minimax():
    count_moves = 0
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('dao game by Liantsoa')
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    game_over = False
    
    while run:
        clock.tick(FPS)
    
        if game.turn == RED and not game_over:
            valid_moves = game.board.get_all_valid_moves(RED)
            #pygame.time.delay(1500) 
            if valid_moves:
                piece, move = random.choice(list(valid_moves.items()))
                row, col = random.choice(move)
                game.board.move(piece, row, col)
                
                
                if game.board.check_winner(RED):
                    print(f"############THE RED HAS WON ##################################")
                    game_over = True
                    game.update()
                    pygame.time.delay(3000)  
                    run = False 
                game.change_turn()
                
        game.update()
        
        if game.turn == WHITE and not game_over:
            value, new_board= minimax(game.get_board(),3, WHITE, game) #THREE LEVEL TO BE MORE EFFICIENT
            game.ai_move(new_board)
            count_moves += 1
            
            if game.board.check_winner(WHITE):
                    print(f"############## THE WHITE HAS WON AFTER {count_moves} moves ################")
                    game_over = True
                    game.update()
                    pygame.time.delay(3000)  
                    run = False  
                        
        if not game_over:
            game.update()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
def minimax_vs_minimax():
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('dao game by Liantsoa')
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    game_over = False
    
    if game.turn == RED and not game_over:
            valid_moves = game.board.get_all_valid_moves(RED)
            pygame.time.delay(500) 
            if valid_moves:
                piece, move = random.choice(list(valid_moves.items()))
                row, col = random.choice(move)
                game.board.move(piece, row, col)
      
    while run:
        clock.tick(FPS)
        game.update()
        
        if game.turn == RED:
            value, new_board= minimax_red(game.get_board(),3,RED, game)
            game.ai_move(new_board)
            
        if game.board.check_winner(RED) or game.board.check_winner(WHITE):
            if game.board.check_winner(RED): 
                print("Red won")
            else: print("White won")
            game_over = True
            game.update()
            pygame.time.delay(1000) 
            run = False
            
        game.update()
        
        if game.turn == WHITE:
            value, new_board= minimax(game.get_board(),3, WHITE, game)
            game.ai_move(new_board)
            
        game.update()
        
        if game.board.check_winner(RED) or game.board.check_winner(WHITE):
            if game.board.check_winner(RED): 
                print("Red won")
            else: print("White won")
            game_over = True
            game.update()
            pygame.time.delay(1000) 
            run = False
            
        if not game_over:
            game.update()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()
        
    
def main():
    print("###############################################################")
    print("#                 Select game mode:                           #")
    print("#                 0 - Two player game                         #")
    print("#                 1 - Play against a simple machine           #")
    print("#                 2 - Play against minimax machine            #")
    print("#                 3 - Simple machine VS minimax               #")
    print("#                 4 - minimax VS minimax                      #")
    print("###############################################################")
    choice = input("###################################### Enter your choice: ")
    print("################ OKAY LETS PLAY ###############################")

    if choice == '0':
        two_player_game()
    elif choice == '1':
        simple_machine_game()
    elif choice == '2':
        minimax_game()
    elif choice == '3':
        simple_machine_vs_minimax()
    elif choice == '4':
        minimax_vs_minimax()
    
    else:
        print("Invalid choice. Exiting the game.")
        pygame.quit()

main()