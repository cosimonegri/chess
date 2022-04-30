from pieces.piece import Piece


class King(Piece):
    """Class that inherits from the Piece class, and that handles things related to the king piece.
    
    :attr id: int
    :attr row: int
    :attr col: int
    :attr color: str
    :attr image: pygame.Surface
    """

    def __init__(self, row, col, color):
        """
        :param row: int
        :param col: int
        :param color: str
        """
        self.id = Piece.KING_ID
        super().__init__(row, col, color)
    

    def calculate_valid_moves(self, board, castle_rights, en_passant_square):
        """Calculates the squares where the piece can move.

        This function takes into account all the chess rules, except from check.
        Therefore, also moves that are not valid because you are in check, or because
        they would put you in check, are considere valid here.

        :param board: list[list[ optional[Piece] ]]
        :param castle_rights: str
        :param en_passant_square: tuple[int, int]
        :return: tuple[ list[list[bool]], list[tuple[int, int]] ]
        """
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
            if 0 <= row <= 7 and 0 <= col <= 7:
                if board[row][col] == None or board[row][col].color != self.color:
                    valid_moves_table[row][col] = True
                    valid_moves_list.append((col, row))
        
        opponent_pieces = []
        for row in board:
            for piece in row:
                if piece != None and piece.color != self.color:
                    opponent_pieces.append(piece)
        
        # KING-SIDE-CASTLING
        if 'K' in castle_rights and self.color == Piece.WHITE or 'k' in castle_rights and self.color == Piece.BLACK:
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
        
        # QUEEN-SIDE-CASTLING
        if 'Q' in castle_rights and self.color == Piece.WHITE or 'q' in castle_rights and self.color == Piece.BLACK:
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