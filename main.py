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
    winner_color = None

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                if game.select(row, col):
                    if game.board.check_winner(game.turn):
                        winner_color = game.turn
                        game_over = True

        if not game_over:
            game.update()
        else:
            show_winner_screen(winner_color)
            return  
    pygame.quit()

def simple_machine_game():
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('dao game by Liantsoa')
    clock = pygame.time.Clock()
    game = Game(WIN)

    while True:
        clock.tick(FPS)

        # --- Events (WHITEturn) ---
        if game.turn == WHITE:
            valid_moves = game.board.get_all_valid_moves(WHITE)
            pygame.time.delay(300)  # léger cooldown visuel
            if valid_moves:
                piece, moves = random.choice(list(valid_moves.items()))
                row, col = random.choice(moves)
                game.board.move(piece, row, col)

                if game.board.check_winner(WHITE):
                    game.update()
                    show_winner_screen(WHITE)
                    return  # retour au menu

                game.change_turn()
            else:
                
                game.change_turn()

        # --- Events (BLACK turn) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  #Back to menu

            if game.turn == BLACK and event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                if game.select(row, col):
                    if game.board.check_winner(BLACK):
                        game.update()
                        show_winner_screen(BLACK)
                        return  #Back to menu

        
        game.update()

def minimax_game():
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('dao game by Liantsoa')
    clock = pygame.time.Clock()
    game = Game(WIN)

    SEARCH_DEPTH = 3  # Fix if needed

    while True:
        clock.tick(FPS)

        # --- Tour IA (WHITE) ---
        if game.turn == WHITE:
            try:
                value, new_board = minimax(game.get_board(), SEARCH_DEPTH, True, game)
            except Exception:
                game.change_turn()
            else:
                game.ai_move(new_board)
                if game.board.check_winner(WHITE):
                    game.update()
                    show_winner_screen(WHITE)
                    return  #Back menu

        # --- Events  BLACK) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  

            if game.turn == BLACK and event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                if game.select(row, col):
                    if game.board.check_winner(BLACK):
                        game.update()
                        show_winner_screen(BLACK)
                        return 

        # --- Dessin ---
        game.update()

def simple_machine_vs_minimax():
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("dao game by Liantsoa")
    clock = pygame.time.Clock()
    game = Game(WIN)
    count_moves = 0

    while True:
        clock.tick(FPS)

        if game.turn == BLACK:
            valid_moves = game.board.get_all_valid_moves(BLACK)
            pygame.time.delay(300)
            if valid_moves:
                piece, moves = random.choice(list(valid_moves.items()))
                row, col = random.choice(moves)
                game.board.move(piece, row, col)
                if game.board.check_winner(BLACK):
                    game.update()
                    show_winner_screen(BLACK)
                    return
                game.change_turn()
            else:
                game.change_turn()

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, True, game)
            game.ai_move(new_board)
            count_moves += 1
            if game.board.check_winner(WHITE):
                game.update()
                show_winner_screen(WHITE)
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        game.update()
        
def minimax_vs_minimax():
    FPS = 60
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("dao game by Liantsoa")
    clock = pygame.time.Clock()
    game = Game(WIN)

    if game.turn == BLACK:
        valid_moves = game.board.get_all_valid_moves(BLACK)
        pygame.time.delay(400)
        if valid_moves:
            piece, moves = random.choice(list(valid_moves.items()))
            row, col = random.choice(moves)
            game.board.move(piece, row, col)
            game.change_turn()

    while True:
        clock.tick(FPS)
        game.update()

        if game.turn == BLACK:
            value, new_board = minimax_red(game.get_board(), 3, True, game)
            game.ai_move(new_board)
            if game.board.check_winner(BLACK):
                game.update()
                show_winner_screen(BLACK)
                return

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, True, game)
            game.ai_move(new_board)
            if game.board.check_winner(WHITE):
                game.update()
                show_winner_screen(WHITE)
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


def show_winner_screen(winner_color=None, message=None):
    """Affiche un écran de fin avec le gagnant + bouton retour menu. Bloquant, retourne au menu quand on clique."""
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    CLOCK = pygame.time.Clock()
    BG = load_bg_for_window()

    # Texte principal
    if message:
        title = message
    else:
        if winner_color == WHITE:
            title = "WHITE WINS!"
        elif winner_color == BLACK:
            title = "BLACK WINS!"
        else:
            title = "GAME OVER"

    # Layout
    title_font_size = max(56, int(HEIGHT * 0.085))
    title_font = get_font(title_font_size)
    # Couleur du titre: vert thème (lisible sur BG)
    title_surface = title_font.render(title, True, pygame.Color("#769656"))
    title_rect = title_surface.get_rect(center=(WIDTH // 2, int(HEIGHT * 0.28)))

    # Bouton “Back to Menu”
    btn_w = int(WIDTH * 0.55)
    btn_h = int(HEIGHT * 0.09)
    def scale_button_image(filename: str, w: int, h: int) -> pygame.Surface:
        img = pygame.image.load(asset_path(filename)).convert_alpha()
        return pygame.transform.smoothscale(img, (w, h))
    back_img = scale_button_image("Play Rect.png", btn_w, btn_h)

    back_btn = Button(
        image=back_img,
        pos=(WIDTH // 2, int(HEIGHT * 0.55)),
        text_input="Back to Menu",
        font=get_font(max(28, int(HEIGHT * 0.045))),
        base_color="#d7fcd4",
        hovering_color="brown",
    )

    # Boucle écran de fin
    waiting = True
    while waiting:
        CLOCK.tick(60)
        WIN.blit(BG, (0, 0))
        WIN.blit(title_surface, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        back_btn.changeColor(mouse_pos)
        back_btn.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.checkForInput(mouse_pos):
                    waiting = False

        pygame.display.flip()
    # Retour au menu : on laisse juste la fonction RETURN
    return
      

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
    MENU_TEXT = title_font.render("Menu", True, pygame.Color("#769656")) #769656
    MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH // 2, title_y))

    
    play_img = scale_button_image("Play Rect.png", btn_w, btn_h)
    quit_img = scale_button_image("Quit Rect.png", btn_w, btn_h)

    
    btn_font = get_font(btn_font_size)

    
    buttons_spec = [
        ("Two player game",           first_btn_y + 0*btn_gap, play_img, two_player_game),
        ("You   VS random bot",       first_btn_y + 1*btn_gap, play_img, simple_machine_game),
        ("You   VS minimax bot",      first_btn_y + 2*btn_gap, play_img, minimax_game),
        ("Random VS minimax bot",    first_btn_y + 3*btn_gap, play_img, simple_machine_vs_minimax),
        ("Two minimax bots",   first_btn_y + 4*btn_gap, play_img, minimax_vs_minimax),
        ("QUIT",                 first_btn_y + 6*btn_gap, quit_img, None),
    ]

    
    buttons = []
    for label, y, img, cb in buttons_spec:
        btn = Button(
            image=img,
            pos=(WIDTH // 2, y),
            text_input=label,
            font=btn_font,
            base_color="#035757",
            hovering_color="brown",
        )
        buttons.append((btn, cb))

    
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



