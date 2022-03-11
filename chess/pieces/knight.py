from pieces.piece import Piece
from pieces.piece import BLACK_KNIGHT
from pieces.piece import WHITE_KNIGHT


class Knight(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.id = 1
        if self.color == 'black':
            self.image = BLACK_KNIGHT
        else:
            self.image = WHITE_KNIGHT
    
    def calculate_valid_moves(self, board, castle_rights, en_passant):
        valid_moves_table = [[False for _ in range(8)] for _ in range(8)]
        valid_moves_list = []
        
        if self.row-2 >= 0:
            
            # TOP-LEFT
            if self.col-1 >= 0:
                if board[self.row-2][self.col-1] == None or board[self.row-2][self.col-1].color != self.color:
                    valid_moves_table[self.row-2][self.col-1] = True
                    valid_moves_list.append((self.col-1, self.row-2))
            
            # TOP-RIGHT
            if self.col+1 <= 7:
                if board[self.row-2][self.col+1] == None or board[self.row-2][self.col+1].color != self.color:
                    valid_moves_table[self.row-2][self.col+1] = True
                    valid_moves_list.append((self.col+1, self.row-2))
        
        if self.col + 2 <= 7:
        
            # RIGHT-TOP
            if self.row - 1 >= 0:
                if board[self.row-1][self.col+2] == None or board[self.row-1][self.col+2].color != self.color:
                    valid_moves_table[self.row-1][self.col+2] = True
                    valid_moves_list.append((self.col+2, self.row-1))
            
            # RIGHT-BOTTOM
            if self.row + 1 <= 7:
                if board[self.row+1][self.col+2] == None or board[self.row+1][self.col+2].color != self.color:
                    valid_moves_table[self.row+1][self.col+2] = True
                    valid_moves_list.append((self.col+2, self.row+1))
        
        if self.row + 2 <= 7:
            
            # BOTTOM-RIGHT
            if self.col + 1 <= 7:
                if board[self.row+2][self.col+1] == None or board[self.row+2][self.col+1].color != self.color:
                    valid_moves_table[self.row+2][self.col+1] = True
                    valid_moves_list.append((self.col+1, self.row+2))
            
            # BOTTOM-LEFT
            if self.col - 1 >= 0:
                if board[self.row+2][self.col-1] == None or board[self.row+2][self.col-1].color != self.color:
                    valid_moves_table[self.row+2][self.col-1] = True
                    valid_moves_list.append((self.col-1, self.row+2))
        
        if self.col - 2 >= 0:
                
            # LEFT-BOTTOM
            if self.row + 1 <= 7:
                if board[self.row+1][self.col-2] == None or board[self.row+1][self.col-2].color != self.color:
                    valid_moves_table[self.row+1][self.col-2] = True
                    valid_moves_list.append((self.col-2, self.row+1))
                    
            # LEFT-TOP
            if self.row - 1 >= 0:
                if board[self.row-1][self.col-2] == None or board[self.row-1][self.col-2].color != self.color:
                    valid_moves_table[self.row-1][self.col-2] = True
                    valid_moves_list.append((self.col-2, self.row-1))
                    
        return valid_moves_table, valid_moves_list