from pieces import Piece
from pieces import Pawn
from pieces import Knight
from pieces import Bishop
from pieces import Rook
from pieces import Queen
from pieces import King


class Board:
    """Class used to handle the game logic, and to contain the board and other data needed in a chess match.
    
    :attr board: list[list[ optional[Piece] ]]
    :attr turn: str
    :attr castle_rights: str
    :attr en_passant_square: str
    :attr selected_piece: optional[Piece]
    :attr eaten_pieces: dict[ str, dict[int, int] ]
    :attr white_king_pos: tuple[int, int]
    :attr black_king_pos: tuple[int, int]
    :attr promotion_square: optional[ tuple[int, int] ]
    :attr checkmate: bool
    :attr stalemate: bool
    :attr winner: optional[str]
    """

    STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    PIECE_ID_MAP = {
        'p': Piece.PAWN_ID, 'n': Piece.KNIGHT_ID, 'b': Piece.BISHOP_ID,
        'r': Piece.ROOK_ID, 'q': Piece.QUEEN_ID, 'k': Piece.KING_ID
    }
    PIECE_LETTER_MAP = {
        Piece.PAWN_ID: 'p', Piece.KNIGHT_ID: 'n', Piece.BISHOP_ID: 'b',
        Piece.ROOK_ID: 'r', Piece.QUEEN_ID: 'q', Piece.KING_ID: 'k'
    }
    

    def __init__(self, fen=STARTING_FEN):
        """Initialize the board using the Forsyth-Edwards Notation (FEN) and other game data.
        
        :param fen: str
        """
        self.from_fen(fen)
        self.white_king_pos = self.find_king(Piece.WHITE)  # (row, col)
        self.black_king_pos = self.find_king(Piece.BLACK)  # (row, col)
        
        self.selected_piece = None
        self.eaten_pieces = {
            Piece.WHITE: {Piece.PAWN_ID: 0, Piece.KNIGHT_ID: 0, Piece.BISHOP_ID: 0, Piece.ROOK_ID: 0, Piece.QUEEN_ID: 0},
            Piece.BLACK: {Piece.PAWN_ID: 0, Piece.KNIGHT_ID: 0, Piece.BISHOP_ID: 0, Piece.ROOK_ID: 0, Piece.QUEEN_ID: 0}
        }
        
        self.promotion_square = None
        self.checkmate = False
        self.stalemate = False
        self.winner = None
    
    
    def from_fen(self, fen):
        """Uses the FEN string passed as argument to set the board, the turn, the castle rights,
        the en passant square, the halfmove clock and the fullmove number.
        
        :param fen: str
        :return: None
        """
        try:
            self.board = [[None for _ in range(8)] for _ in range(8)]
            splitted_fen = fen.split()
            row = 0
            col = 0
            
            for char in splitted_fen[0]:
                if char >= '1' and char <= '8':
                    col += int(char)
                
                elif char == "/":
                    col = 0
                    row += 1
                    continue
                
                else:
                    color = Piece.WHITE if char.isupper() else Piece.BLACK
                    id = self.PIECE_ID_MAP[char.lower()]
                    
                    if id == Piece.PAWN_ID:
                        self.board[row][col] = Pawn(row, col, color)
                    elif id == Piece.KNIGHT_ID:
                        self.board[row][col] = Knight(row, col, color)
                    elif id == Piece.BISHOP_ID:
                        self.board[row][col] = Bishop(row, col, color)
                    elif id == Piece.ROOK_ID:
                        self.board[row][col] = Rook(row, col, color)
                    elif id == Piece.QUEEN_ID:
                        self.board[row][col] = Queen(row, col, color)
                    elif id == Piece.KING_ID:
                        self.board[row][col] = King(row, col, color)
                    
                    col += 1
            
            if splitted_fen[1] == "b":
                self.turn = Piece.BLACK
            else:
                self.turn = Piece.WHITE
            
            
            if splitted_fen[2] != '-':
                self.castle_rights = splitted_fen[2]
            else:
                self.castle_rights = ''
            
            if splitted_fen[3] != '-':
                self.en_passant_square = self.square_from_uci(splitted_fen[3])
            else:
                self.en_passant_square = ''
        
        except:
            raise Exception("You have tried to create a board with an invalid FEN string.")
        
        # aggiungere regole strane per 50, 70 turni
    
    
    def to_fen(self):
        """Creates a FEN string using the data of the current board.
        
        :return: str
        """
        fen_board = ''
        free_squares = 0
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]

                if piece != None:
                    if free_squares != 0:
                        fen_board += str(free_squares)
                        free_squares = 0
                    char = self.PIECE_LETTER_MAP[piece.id]
                    if piece.color == Piece.WHITE:
                        char = char.upper()
                    fen_board += char

                else:
                    free_squares += 1

            if free_squares != 0:
                fen_board += str(free_squares)
                free_squares = 0

            if row != 7:
                fen_board += '/'
        
        fen_board += ' '
        if self.turn == Piece.WHITE:
            fen_board += 'w'
        else:
            fen_board += 'b'
        fen_board += ' '
        
        if self.castle_rights:
            fen_board += self.castle_rights
        else:
            fen_board += '-'
        fen_board += ' '
        
        if self.en_passant_square:
            fen_board += self.square_to_uci(self.en_passant_square[0], self.en_passant_square[1])
        else:
            fen_board += '-'
        fen_board += ' '
        
        #############  ADD RULES for fifty rule move and moves count
        fen_board += '0 0'
        return fen_board
    
    
    def square_to_uci(self, row, col):
        """Uses the row and col of a square to get its coordinates in UCI notation.
        
        :param row: int
        :param row: int
        :return: str
        """
        col_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return col_map[col] + str(8 - row)

    
    def square_from_uci(self, square):
        """Uses the coordinates in UCI notation of a square to get its row and col.
        
        :param square: str
        :return: tuple[int, int]
        """
        col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        col = col_map[square[0]]
        row = 8 - int(square[1])
        return (row, col)
                
            
    def at_square(self, row, col):
        """Gets the piece at a specific position on the board.

        :param row: int
        :param col: int
        :return: optional[Piece]
        """
        return self.board[row][col]

    
    def set_piece_at(self, piece, row, col):
        """Sets a piece at a specific position on the board.

        :param piece: Piece
        :param row: int
        :param col: int
        :return: None
        """
        self.board[row][col] = piece
    
    
    def get_pieces(self, color=None):
        """Finds all the pieces of the given color on the current board.
        
        If no color is passed as argument, the color is the one of the player on duty.

        :param color: optional[str]
        :return: list[Piece]
        """
        if color == None:
            color = self.turn

        return [piece for row in self.board for piece in row if piece != None and piece.color == color]
    
    
    def change_turn(self):
        """Changes the turn.
        
        :return: None
        """
        if self.turn == Piece.WHITE:
            self.turn = Piece.BLACK
        else:
            self.turn = Piece.WHITE


    def find_king(self, color):
        """Finds the position on the board of the king of the given color.

        :param color: str
        :return: None
        """
        for row in self.board:
            for piece in row:
                if piece != None and piece.is_king() and piece.color == color:
                    return piece.row, piece.col
    
    
    def get_king_pos(self, color):
        """Returns the position on the board of the king of the given color.

        The position is already stored in a class attribute.
        
        :param color: str
        :return: tuple[int, int]
        """
        if color == Piece.WHITE:
            return self.white_king_pos
        if color == Piece.BLACK:
            return self.black_king_pos
    
    
    def update_king_pos(self, end_row, end_col, color=None):
        """Updates the class attribute that contains the position of the king of the given color.

        If no color is passed as argument, the color is the one of the player on duty.

        :param end_row: int
        :param start_row: int
        :param end_col: optional[str]
        :return: None
        """
        if self.turn == Piece.WHITE:
            self.white_king_pos = (end_row, end_col)
        else:
            self.black_king_pos = (end_row, end_col)
    
    
    def is_checkmate(self):
        """
        :return: bool
        """
        return self.checkmate
    
    
    def is_stalemate(self):
        """
        :return: bool
        """
        return self.stalemate
    
    
    def is_move_inbound(self, start_row, start_col, end_row, end_col):
        """Checks if the selected start square and end square are exist on the board.

        :param start_row: int
        :param start_col: int
        :param end_row: int
        :param end_col: int
        :return: bool
        """
        return all(0 <= elem <= 7 for elem in [start_row, start_col, end_row, end_col])
    
    
    def move(self, start_row, start_col, end_row, end_col):
        """Moves the piece on the board, from the start square to the end square.

        If the end square is occupied by an enemy piece, the function returns it before overwriting it.
        
        :param start_row: int
        :param start_col: int
        :param end_row: int
        :param end_col: int
        :return: optional[Piece]
        """
        selected_piece = self.board[start_row][start_col]
        eaten_piece = self.board[end_row][end_col]

        self.board[end_row][end_col] = selected_piece
        self.board[start_row][start_col] = None
        selected_piece.row = end_row
        selected_piece.col = end_col
        
        return eaten_piece
    
    
    def update_pseudo_legal_moves(self):
        """Updates the pseudo legal moves of all the pieces on the board.

        Pseudo legal moves are calculated applying all the chess rules, except from the check rule.
        Therefore, the king might be in check after a pseudo legal move.
        
        :return: None
        """
        for row in self.board:
            for piece in row:
                if piece != None:
                    piece.update_moves(self.board, self.castle_rights, self.en_passant_square)
    
    
    # Call this function at the beginning of a player's turn, with his color.
    def update_legal_moves(self, color=None):
        """Updates the pseudo legal moves of all the pieces and the legal moves of the pieces with the given color.

        If no color is passed as argument, the color is the one of the player on duty.
        Pseudo legal moves are calculated applying all the chess rules, except from the check rule.
        Therefore, the king might be in check after a pseudo legal move.
        Legal moves are calculated taking in consideration all chess rules.

        :param color: optional[str]
        :return: None
        """
        if color == None:
            color = self.turn
        
        self.update_pseudo_legal_moves()

        my_pieces = self.get_pieces(color)
        enemy_pieces = self.get_pieces(Piece.BLACK) if color == Piece.WHITE else self.get_pieces(Piece.WHITE)
        
        for my_piece in my_pieces:
            new_valid_moves_list = []  # contain all the moves without the valid ones
            start_row = my_piece.row
            start_col = my_piece.col
            
            for move in my_piece.valid_moves_list:
                move_has_to_be_removed = False
                end_col, end_row = move

                # do the move
                eaten_piece = self.move(start_row, start_col, end_row, end_col) ####  FORSE QUA SE NON FACCIO EXECUTE SBALGIO ROBA????????
                
                if my_piece.is_king():
                    king_row = end_row
                    king_col = end_col
                else:
                    king_row, king_col = self.get_king_pos(color)
                
                # control if after the move the king would be under check
                for enemy_piece in enemy_pieces:
                    if enemy_piece != eaten_piece:
                        enemy_piece.update_moves(self.board, self.castle_rights, self.en_passant_square)
                        if enemy_piece.valid_moves_table[king_row][king_col] == True:
                            move_has_to_be_removed = True
                            break
                
                # do not save the move in the new list if it has to be removed
                if move_has_to_be_removed:
                    #print("removing", end_row, end_col)
                    my_piece.valid_moves_table[end_row][end_col] = False
                else:
                    new_valid_moves_list.append(move)
                
                # undo the move
                self.move(end_row, end_col, start_row, start_col)
                self.board[end_row][end_col] = eaten_piece
                
                if eaten_piece != None:
                    eaten_piece.update_moves(self.board, self.castle_rights, self.en_passant_square)
            
            # update the list of the valid moves
            my_piece.valid_moves_list = new_valid_moves_list
    
    
    def is_legal_move(self, start_row, start_col, end_row, end_col):
        """Checks if the given move is among the legal moves.

        :param start_row: int
        :param start_col: int
        :param end_row: int
        :param end_col: int
        :return: bool
        """
        selected_piece = self.board[start_row][start_col]
        if selected_piece == None:
            return False
        return selected_piece.valid_moves_table[end_row][end_col]

    
    def en_passant_capture(self, piece):
        """Handles the capture done during an en passant move.

        :param piece: Piece
        :return: None
        """
        if (piece.row, piece.col) == self.en_passant_square:
            if piece.color == Piece.WHITE:
                forward = -1
            else:
                forward = 1
            eaten_piece = self.board[piece.row - forward][piece.col]
            self.eaten_pieces[eaten_piece.color][eaten_piece.id] += 1
            self.board[piece.row - forward][piece.col] = None
    
    
    def move_castled_rook(self, end_row, end_col):
        """Handles the movement of the rook after a castle.

        :param end_row: int
        :param end_col: int
        :return: None
        """
        if 'K' in self.castle_rights and end_row == 7 and end_col == 6:
            self.move(7, 7, 7, 5)
        elif 'Q' in self.castle_rights and end_row == 7 and end_col == 2:
            self.move(7, 0, 7, 3)
        if 'k' in self.castle_rights and end_row == 0 and end_col == 6:
            self.move(0, 7, 0, 5)
        elif 'q' in self.castle_rights and end_row == 0 and end_col == 2:
            self.move(0, 0, 0, 3)
    
    
    def update_castle_rights(self, piece, start_row, start_col):
        """Updates the castle rights.

        :param piece: Piece
        :param start_row: int
        :param start_col: int
        :return: None
        """
        if piece.is_king():
            if piece.color == Piece.WHITE:
                self.castle_rights = self.castle_rights.replace("K", "")
                self.castle_rights = self.castle_rights.replace("Q", "")
            else:
                self.castle_rights = self.castle_rights.replace("k", "")
                self.castle_rights = self.castle_rights.replace("q", "")
        
        elif piece.is_rook():
            if start_row == 7 and start_col == 7:
                self.castle_rights = self.castle_rights.replace("K", "")
            elif start_row == 7 and start_col == 0:
                self.castle_rights = self.castle_rights.replace("Q", "")
            elif start_row == 0 and start_col == 7:
                self.castle_rights = self.castle_rights.replace("k", "")
            elif start_row == 0 and start_col == 0:
                self.castle_rights = self.castle_rights.replace("q", "")
    
    
    def update_en_passant_square(self, piece, start_row, end_row, end_col):
        """Updates the en passant square and saves it in an attribute.

        The en passant square is the square where the opponent pawn has to move if he does the en passant move.

        :param piece: Piece
        :param start_row: int
        :param end_row: int
        :param end_col: int
        :return: None
        """
        self.en_passant_square = ''
        
        if piece.color == Piece.WHITE and start_row == 6 and end_row == 4:
            self.en_passant_square = (5, end_col)
        elif piece.color == Piece.BLACK and start_row == 1 and end_row == 3:
            self.en_passant_square = (2, end_col)

    
    def execute_move(self, start_row, start_col, end_row, end_col, from_bot=False):
        """Executes the move passed as argument and handles everything that has to be handled during a move, like
        captured pieces, castle rights, rooks that have to move after a castle ecc...
        
        :param start_row: int
        :param start_col: int
        :param end_row: int
        :param end_col: int
        :param from_bot: bool ??????????????
        :return: None
        """
        piece = self.board[start_row][start_col]
        
        # move the selected piece and add it (if there is one) to the eaten pieces
        eaten_piece = self.move(start_row, start_col, end_row, end_col)
        if eaten_piece != None:
            self.eaten_pieces[eaten_piece.color][eaten_piece.id] += 1
        
        if piece.is_king():
            self.update_king_pos(end_row, end_col)
            self.move_castled_rook(end_row, end_col)  # it does something only if there was a castle
        
        if piece.is_king() or piece.is_rook():
            self.update_castle_rights(piece, start_row, start_col)
        
        if piece.is_pawn():
            self.en_passant_capture(piece)  # it does something if there was an en passant
            self.update_en_passant_square(piece, start_row, end_row, end_col)
        
        if not piece.is_pawn():
            self.en_passant_square = ''  # reset en passant

        # handle the promotion, which is different between player and bot
        if piece.is_pawn() and (piece.row == 0 or piece.row == 7):
            if not from_bot:
                self.promotion_square = (end_row, end_col)
            else:
                self.board[end_row][end_col] = Queen(end_row, end_col, piece.color)
 

    def promote(self, new_piece, color):
        """Promotes the piece in the promotion square (saved in an attribute) to the given piece.

        :param new_piece: str
        :param color: str
        :return: None
        """
        row, col = self.promotion_square
        id = self.PIECE_ID_MAP[new_piece]

        if id == Piece.QUEEN_ID:
            new_piece = Queen(row, col, color)
        elif id == Piece.ROOK_ID:
            new_piece = Rook(row, col, color)
        elif id == Piece.BISHOP_ID:
            new_piece = Bishop(row, col, color)
        elif id == Piece.KNIGHT_ID:
            new_piece = Knight(row, col, color)
        
        self.board[row][col] = new_piece
        self.promotion_square = None
    
    
    def do_bot_move(self, bot_move):
        ######## destroy and put everything in singleplayer function ??????????
        
        col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        start_row = 8 - int(bot_move[1])
        start_col = col_map[bot_move[0]]
        end_row = 8 - int(bot_move[3])
        end_col = col_map[bot_move[2]]
        
        self.execute_move(start_row, start_col, end_row, end_col, from_bot=True)
    

    # Remember to update the player/bot moves before cheking if he lost
    def check_if_loser(self, my_color):
        """Checks if the player of the given color is under checkmate or if there is a stalemate.

        The result about checkmate and stalemate is then stored in the corresponding attributes.
        
        :param my_color: str
        :return: None
        """
        if my_color == Piece.WHITE:
            enemy_color = Piece.BLACK
        else:
            enemy_color = Piece.WHITE
        my_pieces = self.get_pieces(my_color)
        enemy_pieces = self.get_pieces(enemy_color)
        
        i_have_moves = False
        for my_piece in my_pieces:
            if my_piece.valid_moves_list != []:
                i_have_moves = True
                break
            
        king_row, king_col = self.get_king_pos(my_color)
        
        if i_have_moves == False:
            for enemy_piece in enemy_pieces:
                enemy_piece.update_moves(self.board, self.castle_rights, self.en_passant_square)
                if enemy_piece.valid_moves_table[king_row][king_col] == True:
                    self.checkmate = True
                    self.winner = enemy_color
                    break
            else:
                self.stalemate = True
    

    def is_end_game_phase(self):
        """Checks if the game is in its final phase.

        This is decided on the basis of how many pieces (except from pawns and kings) remain on the board.
        The information about the game phase is used by the bot, in order to decide which points tables to use
        and adapt the game style.
        
        :return: bool
        """
        white_pieces = 0 
        black_pieces = 0

        for row in self.board:
            for piece in row:
                if piece != None and piece.id != Piece.PAWN_ID and piece.id != Piece.KING_ID:
                    if piece.color == Piece.WHITE:
                        white_pieces += 1
                    else:
                        black_pieces += 1
        
        if white_pieces <= 3 and black_pieces <= 3:
            return True
        
        elif white_pieces <= 2 or black_pieces <= 2:
            return True
        
        return False