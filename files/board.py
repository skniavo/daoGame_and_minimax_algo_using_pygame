import pygame
from .constants import BLACK, ROWS, COLS, RED, SQUARE_SIZE, WHITE
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
        if piece.color == WHITE:
            opponent_color = RED
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
        if self.check_winner(RED):
            return RED
        if self.check_winner(WHITE):
            return WHITE
        return None
    
    def evaluate(self, player_color):
        opponent_color = RED if player_color == WHITE else WHITE
        score = 0
        
        if self.check_winner(player_color):
            return float('inf')
        if self.check_winner(opponent_color):
            return float('-inf')
        
        score += self.potential_alignment_score(player_color)
        score -= self.potential_alignment_score(opponent_color)
        
        score += self.potential_square_2x2_score(player_color)
        score -= self.potential_square_2x2_score(opponent_color)
        
        score += self.potential_corners_score(player_color)
        score -= self.potential_corners_score(opponent_color)
        
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
    
    def evaluate(self, player_color):
        opponent_color = RED if player_color == WHITE else WHITE
        score = 0
        
        if self.check_winner(player_color):
            return 500
        if self.check_winner(opponent_color):
            return -500
        
        score += self.potential_alignment_score(player_color)
        #score -= self.potential_alignment_score(opponent_color)
        
        score += self.potential_square_2x2_score(player_color)
        #score -= self.potential_square_2x2_score(opponent_color)
        
        score += self.potential_corners_score(player_color)
        #score -= self.potential_corners_score(opponent_color)
        
        return score
    
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces