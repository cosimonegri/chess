from pieces.piece import Piece
from pieces.piece import BLACK_BISHOP
from pieces.piece import WHITE_BISHOP


class Bishop(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.id = 2
        if self.color == 'black':
            self.image = BLACK_BISHOP
        else:
            self.image = WHITE_BISHOP
    
    def calculate_valid_moves(self, board, castle_rights, en_passant):
        valid_moves_table = [[False for _ in range(8)] for _ in range(8)]
        valid_moves_list = []
        
        # TOP-RIGHT
        for row, col in zip(range(self.row-1, -1, -1), range(self.col+1, 8)):
            if board[row][col] == None:
                valid_moves_table[row][col] = True
                valid_moves_list.append((col, row))
            elif board[row][col].color != self.color:
                valid_moves_table[row][col] = True
                valid_moves_list.append((col, row))
                break
            else: break
        
        
        # BOTTOM-RIGHT
        for row, col in zip(range(self.row+1, 8), range(self.col+1, 8)):
            if board[row][col] == None:
                valid_moves_table[row][col] = True
                valid_moves_list.append((col, row))
            elif board[row][col].color != self.color:
                valid_moves_table[row][col] = True
                valid_moves_list.append((col, row))
                break
            else: break
        
        # BOTTOM-LEFT
        for row, col in zip(range(self.row+1, 8), range(self.col-1, -1, -1)):
            if board[row][col] == None:
                valid_moves_table[row][col] = True
                valid_moves_list.append((col, row))
            elif board[row][col].color != self.color:
                valid_moves_table[row][col] = True
                valid_moves_list.append((col, row))
                break
            else: break
        
        # TOP-LEFT
        for row, col in zip(range(self.row-1, -1, -1), range(self.col-1, -1, -1)):
            if board[row][col] == None:
                valid_moves_table[row][col] = True
                valid_moves_list.append((col, row))
            elif board[row][col].color != self.color:
                valid_moves_table[row][col] = True
                valid_moves_list.append((col, row))
                break
            else: break
        
        return valid_moves_table, valid_moves_list