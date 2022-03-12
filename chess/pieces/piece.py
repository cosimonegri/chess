import pygame
from constants import PIECES_PATHS, ALT_PIECES_PATHS, PAWN_ID, KNIGHT_ID, BISHOP_ID, ROOK_ID, QUEEN_ID, KING_ID


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.image = None
        self.find_image()  # self.id already setted in each piece class

        self.valid_moves_table = [[False for _ in range(8)] for _ in range(8)]  # [row][col]  // to check the validity of a particular move
        self.valid_moves_list = []  # (col, row)  // to iterate through all the valid moves
    

    def find_image(self):
        try:
            self.image = pygame.image.load(PIECES_PATHS[self.color][self.id])
        except:
            self.image = pygame.image.load(ALT_PIECES_PATHS[self.color][self.id])


    def update_moves(self, board, castle_rights, en_passant):
        self.valid_moves_table, self.valid_moves_list = self.calculate_valid_moves(board, castle_rights, en_passant)
    

    def is_move_inbound(self, row, col):
        return row >= 0 and row <= 7 and col >= 0 and col <= 7
    

    def is_white(self):
        return self.color == "white"
    
    def is_black(self):
        return self.color == "black"
    
    def is_pawn(self):
        return self.id == PAWN_ID
    
    def is_knight(self):
        return self.id == KNIGHT_ID
    
    def is_bishop(self):
        return self.id == BISHOP_ID
    
    def is_rook(self):
        return self.id == ROOK_ID
    
    def is_queen(self):
        return self.id == QUEEN_ID
    
    def is_king(self):
        return self.id == KING_ID