import pygame ,sys
import random
from pathlib import Path
from files.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLACK, WHITE
from files.board import Board
from files.game import Game
from files.button import Button
from minimax.algorithm import minimax, minimax_red

BG =pygame.image.load("files/assets/background.png")

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "files" / "assets"

def asset_path(*parts) -> str:
    return str(ASSETS.joinpath(*parts))

def get_font(size: int) -> pygame.font.Font:
    try:
        return pygame.font.Font(asset_path("font.ttf"), size)
    except Exception:
        return pygame.font.SysFont(None, size)

def load_bg_for_window() -> pygame.Surface:
    bg = pygame.image.load(asset_path("background.png")).convert()
    return pygame.transform.smoothscale(bg, (WIDTH, HEIGHT))


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
                            print(f"#####################THE BLACK HAS WON #################")
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

            if not game_over and game.turn == BLACK and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()  # get mouse position
                row, col = get_row_col_from_mouse(pos)
                if game.select(row, col):
                    if game.board.check_winner(BLACK):
                        print(f"#############THE BLACK HAS WON ###############################")
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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if (not game_over) and game.turn == BLACK and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if game.select(row, col):
                    if game.board.check_winner(BLACK):
                        print("############# THE BLACK HAS WON ###############################")
                        game_over = True

        
        if (not game_over) and game.turn == WHITE:
            # max_player doit être booléen (True quand c'est à l'IA de maximiser)
            value, new_board = minimax(game.get_board(), 3, True, game)
            game.ai_move(new_board)
            if game.board.check_winner(WHITE):
                print("############ THE WHITE HAS WON ##############################")
                game_over = True

        
        game.update()

        # 4) Fin propre
        if game_over:
            pygame.time.delay(3000)
            run = False

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
    
        if game.turn == BLACK and not game_over:
            valid_moves = game.board.get_all_valid_moves(BLACK)
            #pygame.time.delay(1500) 
            if valid_moves:
                piece, move = random.choice(list(valid_moves.items()))
                row, col = random.choice(move)
                game.board.move(piece, row, col)
                
                
                if game.board.check_winner(BLACK):
                    print(f"############THE BLACK HAS WON ##################################")
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
    
    if game.turn == BLACK and not game_over:
            valid_moves = game.board.get_all_valid_moves(BLACK)
            pygame.time.delay(500) 
            if valid_moves:
                piece, move = random.choice(list(valid_moves.items()))
                row, col = random.choice(move)
                game.board.move(piece, row, col)
      
    while run:
        clock.tick(FPS)
        game.update()
        
        if game.turn == BLACK:
            value, new_board= minimax_red(game.get_board(),3,BLACK, game)
            game.ai_move(new_board)
            
        if game.board.check_winner(BLACK) or game.board.check_winner(WHITE):
            if game.board.check_winner(BLACK): 
                print("Black won")
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
        
        if game.board.check_winner(BLACK) or game.board.check_winner(WHITE):
            if game.board.check_winner(BLACK): 
                print("Black won")
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
        

def main_menu():
    pygame.init()
    pygame.display.set_caption("Main Menu")
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    BG = load_bg_for_window()

    # --- Layout scalable (basé sur 800x800) ---
    title_font_size = max(48, min(96, int(HEIGHT * 0.10)))   # ~80px
    btn_w = int(WIDTH * 0.72)                                # ~576px
    btn_h = int(HEIGHT * 0.09)                               # ~72px
    btn_font_size = max(28, min(56, int(HEIGHT * 0.048)))    # ~38px

    title_y = int(HEIGHT * 0.12)                             # ~96px
    first_btn_y = int(HEIGHT * 0.26)                         # ~208px
    btn_gap = int(HEIGHT * 0.11)                             # ~88px

    # --- Helpers ---
    def scale_button_image(filename: str, w: int, h: int) -> pygame.Surface:
        img = pygame.image.load(asset_path(filename)).convert_alpha()
        return pygame.transform.smoothscale(img, (w, h))

    title_font = get_font(title_font_size)
    MENU_TEXT = title_font.render("Menu", True, pygame.Color("#b68f40"))
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH // 2, title_y))

    # Images de base redimensionnées une fois
    play_img = scale_button_image("Play Rect.png", btn_w, btn_h)
    quit_img = scale_button_image("Quit Rect.png", btn_w, btn_h)

    # Police des boutons
    btn_font = get_font(btn_font_size)

    # Définition des boutons (label, y, image, callback)
    buttons_spec = [
        ("Two player game",           first_btn_y + 0*btn_gap, play_img, two_player_game),
        ("You   VS random bot",       first_btn_y + 1*btn_gap, play_img, simple_machine_game),
        ("You   VS minimax bot",      first_btn_y + 2*btn_gap, play_img, minimax_game),
        ("Random VS minimax bot",    first_btn_y + 3*btn_gap, play_img, simple_machine_vs_minimax),
        ("Two minimax bots",   first_btn_y + 4*btn_gap, play_img, minimax_vs_minimax),
        ("QUIT",                 first_btn_y + 6*btn_gap, quit_img, None),
    ]

    # Instanciation des boutons
    buttons = []
    for label, y, img, cb in buttons_spec:
        btn = Button(
            image=img,
            pos=(WIDTH // 2, y),
            text_input=label,
            font=btn_font,
            base_color="#5E3A55",
            hovering_color="brown",
        )
        buttons.append((btn, cb))

    # Boucle principale
    running = True
    while running:
        CLOCK.tick(60)
        WIN.blit(BG, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Titre
        WIN.blit(MENU_TEXT, MENU_RECT)

        # Boutons
        for btn, _ in buttons:
            btn.changeColor(mouse_pos)
            btn.update(WIN)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for btn, cb in buttons:
                    if btn.checkForInput(mouse_pos):
                        if cb is None:         # QUIT
                            running = False
                        else:
                            cb()
                            # Recharger le BG après retour du mode (au cas où set_mode ait tourné)
                            BG = load_bg_for_window()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":

    main_menu()



