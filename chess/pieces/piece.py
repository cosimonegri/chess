import pygame
from pieces.constants import PIECES_PATHS, ALT_PIECES_PATHS


class Piece:
    """General class that handles things that all the pieces have in common.
    
    :attr row: int
    :attr col: int
    :attr color: str
    :attr image: pygame.Surface
    """
    
    WHITE = "white"
    BLACK = "black"
    PAWN_ID = 0
    KNIGHT_ID = 1
    BISHOP_ID = 2
    ROOK_ID = 3
    QUEEN_ID = 4
    KING_ID = 5

    def __init__(self, row, col, color):
        """
        :param row: int
        :param col: int
        :param color: str
        """
        self.row = row
        self.col = col
        self.color = color
        self.find_image()  # self.id already setted in each specific piece class

        # Data structure to check the validity of a particular move in constant time
        self.valid_moves_table = [[False for _ in range(8)] for _ in range(8)]  # [row][col]

        # Data structuer to iterate through all the valid moves in linear time
        self.valid_moves_list = []  # (col, row)
    

    def find_image(self):
        """Loads the image of the current piece from the Images folder.
        
        :return: None
        """
        try:
            self.image = pygame.image.load(PIECES_PATHS[self.color][self.id])
        except:
            try:
                self.image = pygame.image.load(ALT_PIECES_PATHS[self.color][self.id])
            except:
                raise Exception("Could not load the images of the pieces. If you have moved or changed \
                        files and folders inside the project, try to install it again from github.")


    def update_moves(self, board, castle_rights, en_passant_square):
        """Calls a method that updates the squares where the piece can move.

        The called method takes into account all the chess rules, except from check.
        Therefore, also moves that are not valid because you are in check, or because
        they would put you in check, are considere valid here.

        :param board: list[list[ optional[Piece] ]]
        :param castle_rights: str
        :param en_passant_square: tuple[int, int]
        :return: None
        """
        self.valid_moves_table, self.valid_moves_list = self.calculate_valid_moves(board, castle_rights, en_passant_square)
    

    def is_white(self):
        """
        :return: bool
        """
        return self.color == self.WHITE
    
    def is_black(self):
        """
        :return: bool
        """
        return self.color == self.BLACK
    
    def is_pawn(self):
        """
        :return: bool
        """
        return self.id == self.PAWN_ID
    
    def is_knight(self):
        """
        :return: bool
        """
        return self.id == self.KNIGHT_ID
    
    def is_bishop(self):
        """
        :return: bool
        """
        return self.id == self.BISHOP_ID
    
    def is_rook(self):
        """
        :return: bool
        """
        return self.id == self.ROOK_ID
    
    def is_queen(self):
        """
        :return: bool
        """
        return self.id == self.QUEEN_ID
    
    def is_king(self):
        """
        :return: bool
        """
        return self.id == self.KING_ID