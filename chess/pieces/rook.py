from pieces.piece import Piece
from pieces.piece import BLACK_ROOK
from pieces.piece import WHITE_ROOK


class Rook(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.id = 3
        self.first_move = True
        if self.color == 'black':
            self.image = BLACK_ROOK
        else:
            self.image = WHITE_ROOK
    
    def calculate_valid_moves(self, board, castle_rights, en_passant):
        valid_moves_table = [[False for _ in range(8)] for _ in range(8)]
        valid_moves_list = []
        
        # TOP
        for row in range(self.row-1, -1, -1):
            if board[row][self.col] == None:
                valid_moves_table[row][self.col] = True
                valid_moves_list.append((self.col, row))
            elif board[row][self.col].color != self.color:
                valid_moves_table[row][self.col] = True
                valid_moves_list.append((self.col, row))
                break
            else: break
        
        # RIGHT
        for col in range(self.col+1, 8):
            if board[self.row][col] == None:
                valid_moves_table[self.row][col] = True
                valid_moves_list.append((col, self.row))
            elif board[self.row][col].color != self.color:
                valid_moves_table[self.row][col] = True
                valid_moves_list.append((col, self.row))
                break
            else: break
        
        # BOTTOM
        for row in range(self.row+1, 8):
            if board[row][self.col] == None:
                valid_moves_table[row][self.col] = True
                valid_moves_list.append((self.col, row))
            elif board[row][self.col].color != self.color:
                valid_moves_table[row][self.col] = True
                valid_moves_list.append((self.col, row))
                break
            else: break
        
        # LEFT
        for col in range(self.col-1, -1, -1):
            if board[self.row][col] == None:
                valid_moves_table[self.row][col] = True
                valid_moves_list.append((col, self.row))
            elif board[self.row][col].color != self.color:
                valid_moves_table[self.row][col] = True
                valid_moves_list.append((col, self.row))
                break
            else: break
        
        return valid_moves_table, valid_moves_list