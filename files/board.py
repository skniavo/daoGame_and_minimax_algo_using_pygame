import pygame
from .constants import BOARD_LIGHT, BOARD_DARK, ROWS, COLS, SQUARE_SIZE, BLACK, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.create_board()
        
    def copy(self):
        new_board = Board()
        new_board.board = [row.copy() for row in self.board]
        return new_board
        
    def move(self,piece,row,col):
        # self.board[piece.row][piece.col] is where the piece is
        # self.board[row][col] is where we want to go
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col] #swap
        piece.move(row,col)
             
    def draw_squares(self, win):
        # Fill background with light color and draw dark squares
        win.fill(BOARD_LIGHT)
        for row in range(ROWS):
            # start column depends on row to create checker pattern
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, BOARD_DARK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
    def get_piece(self,row,col):
        return self.board[row][col]
                
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row == col:
                    self.board[row].append(Piece(row, col, WHITE))
                elif row + col == COLS -1:
                    self.board[row].append(Piece(row, col, BLACK))
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
        if piece.color == WHITE:
            opponent_color = BLACK
        else:
            opponent_color = WHITE
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
                moves[last_valid] = []    
        return moves
    
    def get_all_valid_moves(self, color):
        all_moves = {}
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0 and piece.color == color:
                    moves = self.get_valid_moves(piece)
                    if moves:
                        all_moves[piece] = list(moves.keys())
        return all_moves

    def check_winner(self, color):
        return self.check_horizontal_vertical_winner(color) or self.check_square_winner(color) or self.check_big_square_winner(color)

    def check_horizontal_vertical_winner(self, color):
        # Check for horizontal and vertical alignment of four pieces
        for row in range(ROWS):
            if all(self.board[row][col] != 0 and self.board[row][col].color == color for col in range(COLS)):
                return True
        for col in range(COLS):
            if all(self.board[row][col] != 0 and self.board[row][col].color == color for row in range(ROWS)):
                return True
        return False

    def check_square_winner(self, color):
        corners = [
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, COLS - 2), (0, COLS - 1), (1, COLS - 2), (1, COLS - 1)],
            [(ROWS - 2, 0), (ROWS - 2, 1), (ROWS - 1, 0), (ROWS - 1, 1)],
            [(ROWS - 2, COLS - 2), (ROWS - 2, COLS - 1), (ROWS - 1, COLS - 2), (ROWS - 1, COLS - 1)]
        ]
        max_count = 0
        for corner in corners:
            count = 0
            for (row, col) in corner:
                if self.board[row][col] != 0 and self.board[row][col].color == color:
                    count += 1
            if count > max_count:
                max_count = count
        
        return max_count == 4    
        
        
        
    
    
    

    def check_big_square_winner(self, color):
        # Check for a piece in each corner of the board
        corners = [(0, 0), (0, COLS - 1), (ROWS - 1, 0), (ROWS - 1, COLS - 1)]
        return all(self.board[row][col] != 0 and self.board[row][col].color == color for row, col in corners)    
    
    def winner(self):
        if self.check_winner(BLACK):
            return BLACK
        if self.check_winner(WHITE):
            return WHITE
        return None
    
    
    def evaluate(self, player_color):
        opponent_color = BLACK if player_color == WHITE else WHITE
        # Terminal states
        if self.check_winner(player_color):
            return 500
        if self.check_winner(opponent_color):
            return -500

        score = 0

        # Heuristiques existantes
        score += self.potential_alignment_score(player_color)          # alignements partiels
        score += self.potential_square_2x2_score(player_color)         # présence dans coins 2x2
        score += self.potential_corners_score(player_color)            # occupation des 4 coins du board

        # >>> NOUVEAU : menaces (poids forts)
        # 1) Menaces carré 2x2 (coins)
        my_2x2_threats, opp_2x2_threats = self._count_2x2_threats(player_color)
        score += 40 * my_2x2_threats          # j'ai 3/4 dans un coin => gros bonus
        score -= 60 * opp_2x2_threats         # l'adversaire a 3/4 => priorité absolue à bloquer

        # 2) Menaces lignes/colonnes (3 sur 4)
        my_line_threats, opp_line_threats = self._count_line_threats(player_color)
        score += 25 * my_line_threats         # alignement 3/4 pour moi
        score -= 35 * opp_line_threats        # alignement 3/4 pour l'adversaire

        return score


    def potential_alignment_score(self, color):
        row_counts = [0] * ROWS
        col_counts = [0] * COLS

        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != 0 and self.board[row][col].color == color:
                    row_counts[row] += 1
                    col_counts[col] += 1

        max_row_count = max(row_counts)
        max_col_count = max(col_counts)

        score = max_row_count + max_col_count
        
        return score
    
    def potential_square_2x2_score(self, color):
        corners = [
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, COLS - 2), (0, COLS - 1), (1, COLS - 2), (1, COLS - 1)],
            [(ROWS - 2, 0), (ROWS - 2, 1), (ROWS - 1, 0), (ROWS - 1, 1)],
            [(ROWS - 2, COLS - 2), (ROWS - 2, COLS - 1), (ROWS - 1, COLS - 2), (ROWS - 1, COLS - 1)]
        ]
        
        max_count = 0
        for corner in corners:
            count = 0
            for (row, col) in corner:
                if self.board[row][col] != 0 and self.board[row][col].color == color:
                    count += 1
            if count > max_count:
                max_count = count
        
        return max_count    
            
    def potential_corners_score(self, color):
        corners = [(0, 0), (0, COLS - 1), (ROWS - 1, 0), (ROWS - 1, COLS - 1)]
        count = 0
        for row, col in corners:
            if self.board[row][col] != 0 and self.board[row][col].color == color:
                count += 1
        
        return count
    
    
    
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    
    
    def _corner_squares(self):
        # Les 4 coins (2x2)
        return [
            [(0, 0), (0, 1), (1, 0), (1, 1)],
            [(0, COLS - 2), (0, COLS - 1), (1, COLS - 2), (1, COLS - 1)],
            [(ROWS - 2, 0), (ROWS - 2, 1), (ROWS - 1, 0), (ROWS - 1, 1)],
            [(ROWS - 2, COLS - 2), (ROWS - 2, COLS - 1), (ROWS - 1, COLS - 2), (ROWS - 1, COLS - 1)]
        ]

    def _count_2x2_threats(self, color):
        """Retourne (mes_3sur4, adv_3sur4) dans les 2x2 de coins."""
        my_three = 0
        opp_three = 0
        opp = BLACK if color == WHITE else WHITE

        for corner in self._corner_squares():
            c_my = c_opp = c_empty = 0
            for (r, c) in corner:
                cell = self.board[r][c]
                if cell == 0:
                    c_empty += 1
                elif cell.color == color:
                    c_my += 1
                else:
                    c_opp += 1
            # 3 de moi + 1 vide => je gagne au prochain coup si j'y ai accès
            if c_my == 3 and c_empty == 1:
                my_three += 1
            # 3 de l'adversaire + 1 vide => menace critique
            if c_opp == 3 and c_empty == 1:
                opp_three += 1

        return my_three, opp_three

    def _count_line_threats(self, color):
        """Menaces de type 3-sur-4 avec 1 vide sur lignes/colonnes (4x4). 
           Retourne (mes_3sur4, adv_3sur4).
        """
        my_three = 0
        opp_three = 0
        opp = BLACK if color == WHITE else WHITE

        # Lignes
        for r in range(ROWS):
            c_my = c_opp = c_empty = 0
            for c in range(COLS):
                cell = self.board[r][c]
                if cell == 0:
                    c_empty += 1
                elif cell.color == color:
                    c_my += 1
                else:
                    c_opp += 1
            if c_my == 3 and c_empty == 1:
                my_three += 1
            if c_opp == 3 and c_empty == 1:
                opp_three += 1

        # Colonnes
        for c in range(COLS):
            c_my = c_opp = c_empty = 0
            for r in range(ROWS):
                cell = self.board[r][c]
                if cell == 0:
                    c_empty += 1
                elif cell.color == color:
                    c_my += 1
                else:
                    c_opp += 1
            if c_my == 3 and c_empty == 1:
                my_three += 1
            if c_opp == 3 and c_empty == 1:
                opp_three += 1

        return my_three, opp_three
