from pieces.piece import Piece
from pieces.piece import BLACK_KING
from pieces.piece import WHITE_KING


class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.id = 5
        if self.color == 'black':
            self.image = BLACK_KING
        else:
            self.image = WHITE_KING
    
    def calculate_valid_moves(self, board, castle_rights, en_passant):
        valid_moves_table = [[False for _ in range(8)] for _ in range(8)]
        valid_moves_list = []
        
        moves_list = [(self.col-1, self.row-1),
                      (self.col, self.row-1),
                      (self.col+1, self.row-1),
                      (self.col+1, self.row),
                      (self.col+1, self.row+1),
                      (self.col, self.row+1),
                      (self.col-1, self.row+1),
                      (self.col-1, self.row)]
        
        for col, row in moves_list:
            if self.is_move_inbound(row, col):
                if board[row][col] == None or board[row][col].color != self.color:
                    valid_moves_table[row][col] = True
                    valid_moves_list.append((col, row))
        
        
        opponent_pieces = []
        for row in board:
            for piece in row:
                if piece != None and piece.color != self.color:
                    opponent_pieces.append(piece)
        
        # RIGHT-CASTLING
        if 'K' in castle_rights and self.color == "white" or 'k' in castle_rights and self.color == "black":
            if board[self.row][7] and board[self.row][7].id == 3 and board[self.row][7].first_move:
                can_castle = True
                
                # free squares in the path
                for col in range(self.col+1, 7):
                    if board[self.row][col] != None: can_castle = False
                
                # in the path king not under check
                if can_castle:
                    for piece in opponent_pieces:
                        for col in range(self.col, 7):
                            if piece.valid_moves_table[self.row][col] == True: can_castle = False
                
                if can_castle:
                    valid_moves_table[self.row][col] = True
                    valid_moves_list.append((col, self.row))
        
        # LEFT-CASTLING
        if 'Q' in castle_rights and self.color == "white" or 'q' in castle_rights and self.color == "black":
            if board[self.row][0] and board[self.row][0].id == 3 and board[self.row][0].first_move:
                can_castle = True
                
                # free squares in the path
                for col in range(self.col-1, 1, -1):
                    if board[self.row][col] != None: can_castle = False
                
                # in the path king not under check
                if can_castle:
                    for piece in opponent_pieces:
                        for col in range(self.col, 1, -1):
                            if piece.valid_moves_table[self.row][col] == True: can_castle = False
                
                if can_castle:
                    valid_moves_table[self.row][col] = True
                    valid_moves_list.append((col, self.row))
        
        return valid_moves_table, valid_moves_list