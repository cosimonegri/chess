import pygame


BLACK_PAWN = pygame.image.load('./chess/assets/Images/black-pawn.png')
WHITE_PAWN = pygame.image.load('./chess/assets/Images/white-pawn.png')

BLACK_KNIGHT = pygame.image.load('./chess/assets/Images/black-knight.png')
WHITE_KNIGHT = pygame.image.load('./chess/assets/Images/white-knight.png')

BLACK_BISHOP = pygame.image.load('./chess/assets/Images/black-bishop.png')
WHITE_BISHOP = pygame.image.load('./chess/assets/Images/white-bishop.png')

BLACK_ROOK = pygame.image.load('./chess/assets/Images/black-rook.png')
WHITE_ROOK = pygame.image.load('./chess/assets/Images/white-rook.png')

BLACK_QUEEN = pygame.image.load('./chess/assets/Images/black-queen.png')
WHITE_QUEEN = pygame.image.load('./chess/assets/Images/white-queen.png')

BLACK_KING = pygame.image.load('./chess/assets/Images/black-king.png')
WHITE_KING = pygame.image.load('./chess/assets/Images/white-king.png')


class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.valid_moves_table = [[False for _ in range(8)] for _ in range(8)]  # [row][col]  // to check the validity of a particular move
        self.valid_moves_list = []  # (col, row)  // to iterate through all the valid moves
    
    def update_moves(self, board, castle_rights, en_passant):
        self.valid_moves_table, self.valid_moves_list = self.calculate_valid_moves(board, castle_rights, en_passant)
    
    def is_move_inbound(self, row, col):
        return row >= 0 and row <= 7 and col >= 0 and col <= 7
    
    def is_white(self):
        return self.color == "white"
    
    def is_black(self):
        return self.color == "black"
    
    def is_pawn(self):
        return self.id == 0
    
    def is_knight(self):
        return self.id == 1
    
    def is_bishop(self):
        return self.id == 2
    
    def is_rook(self):
        return self.id == 3
    
    def is_queen(self):
        return self.id == 4
    
    def is_king(self):
        return self.id == 5