from pieces.piece import Piece
from constants import PAWN_ID


class Pawn(Piece):
    def __init__(self, row, col, color):
        self.id = PAWN_ID
        super().__init__(row, col, color)
    
    
    def calculate_valid_moves(self, board, castle_rights, en_passant):
        valid_moves_table = [[False for _ in range(8)] for _ in range(8)]
        valid_moves_list = []
        
        if self.color == 'white': forward = -1
        else: forward = 1
        
        # FORWARD
        if self.row + forward >= 0 and self.row + forward <= 7:
            if board[self.row + forward][self.col] == None:
                valid_moves_table[self.row + forward][self.col] = True
                valid_moves_list.append((self.col, self.row + forward))
        
        # FIRST MOVE
        if self.row == 6 and self.color == "white" or self.row == 1 and self.color == "black":
            if board[self.row + forward][self.col] == None and board[self.row + 2*forward][self.col] == None:
                valid_moves_table[self.row + 2*forward][self.col] = True
                valid_moves_list.append((self.col, self.row + 2*forward))
        
        # DIAGONAL
        if self.col - 1 >= 0:
            if board[self.row + forward][self.col - 1] != None:
                if board[self.row + forward][self.col - 1].color != self.color:
                    valid_moves_table[self.row + forward][self.col - 1] = True
                    valid_moves_list.append((self.col - 1, self.row + forward))
                    
                    
        if self.col + 1 <= 7:
            if board[self.row + forward][self.col + 1] != None:
                if board[self.row + forward][self.col + 1].color != self.color:
                    valid_moves_table[self.row + forward][self.col + 1] = True
                    valid_moves_list.append((self.col + 1, self.row + forward))
        
        # EN PASSANT
        if self.col - 1 >= 0:
            if (self.row + forward, self.col - 1) == en_passant:
                valid_moves_table[self.row + forward][self.col - 1] = True
                valid_moves_list.append((self.col - 1, self.row + forward))
        
        if self.col + 1 <= 7:
            if (self.row + forward, self.col + 1) == en_passant:
                valid_moves_table[self.row + forward][self.col + 1] = True
                valid_moves_list.append((self.col + 1, self.row + forward))
        
        return valid_moves_table, valid_moves_list