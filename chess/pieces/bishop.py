from pieces.piece import Piece


class Bishop(Piece):
    """Class that inherits from the Piece class, and that handles things related to the bishop piece.
    
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
        self.id = Piece.BISHOP_ID
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