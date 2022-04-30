from pieces.piece import Piece


class Knight(Piece):
    """Class that inherits from the Piece class, and that handles things related to the knight piece.
    
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
        self.id = Piece.KNIGHT_ID
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