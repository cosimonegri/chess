from pieces.piece import Piece


class Pawn(Piece):
    """Class that inherits from the Piece class, and that handles things related to the pawn piece.
    
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
        self.id = Piece.PAWN_ID
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
        
        if self.color == Piece.WHITE:
            forward = -1
        else:
            forward = 1
        
        # FORWARD
        if self.row + forward >= 0 and self.row + forward <= 7:
            if board[self.row + forward][self.col] == None:
                valid_moves_table[self.row + forward][self.col] = True
                valid_moves_list.append((self.col, self.row + forward))
        
        # FIRST MOVE
        if self.row == 6 and self.color == Piece.WHITE or self.row == 1 and self.color == Piece.BLACK:
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
            if (self.row + forward, self.col - 1) == en_passant_square:
                valid_moves_table[self.row + forward][self.col - 1] = True
                valid_moves_list.append((self.col - 1, self.row + forward))
        
        if self.col + 1 <= 7:
            if (self.row + forward, self.col + 1) == en_passant_square:
                valid_moves_table[self.row + forward][self.col + 1] = True
                valid_moves_list.append((self.col + 1, self.row + forward))
        
        return valid_moves_table, valid_moves_list