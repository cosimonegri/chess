import pygame
from pprint import pprint

from pieces import Piece
from pieces import Pawn
from pieces import Knight
from pieces import Bishop
from pieces import Rook
from pieces import Queen
from pieces import King

from helpers import stringify_move


class Board:
    STARTING_FEN = '4k3/8/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    
    def __init__(self, fen=STARTING_FEN):
        self.board = [[None for _ in range(8)] for _ in range(8)]  # [row][col]
        
        # all this are updated with the fen passed as argument
        self.turn = None
        self.castle_rights = ''
        self.en_passant = None
        
        self.set_fen(fen)
        
        self.selected_piece = None
        self.eaten_pieces = {0: [], 1: [], 2: [], 3: [], 4: []}
        
        self.white_king_pos = self.find_king("white")  # (row, col)
        self.black_king_pos = self.find_king("black")  # (row, col)
        
        self.promotion_square = None
        self.checkmate = False
        self.stalemate = False
        self.winner = None
    
    
    def set_fen(self, fen):
        '''Set the board from the fen passed as argument'''
        
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
                color = "white" if char.isupper() else "black"
                char = char.lower()
                
                if char == "p":
                    self.board[row][col] = Pawn(row, col, color)
                elif char == "n":
                    self.board[row][col] = Knight(row, col, color)
                elif char == "b":
                    self.board[row][col] = Bishop(row, col, color)
                elif char == "r":
                    self.board[row][col] = Rook(row, col, color)
                elif char == "q":
                    self.board[row][col] = Queen(row, col, color)
                elif char == "k":
                    self.board[row][col] = King(row, col, color)
                
                col += 1
        
        self.turn = "black" if splitted_fen[1] == "b" else "white"
        
        print(splitted_fen[2])
        if splitted_fen[2] != '-':
            self.castle_rights = splitted_fen[2]
        else:
            self.castle_rights = ''
        
        if splitted_fen[3] != '-':
            self.en_passant = self.square_from_uci(splitted_fen[3])
        else:
            self.en_passant = None
        
        # aggiungere regole strane per 50, 70 turni
    
    
    def to_fen(self):
        colors_map = {"white": 0, "black": 1}
        pieces_map = {
            0: 'P', 1: 'p', 2: 'N', 3: 'n', 4: 'B', 5: 'b',
            6: 'R', 7: 'r', 8: 'Q', 9: 'q', 10: 'K', 11: 'k'        
        }
        
        board = self.board
        fen_board = ''
        free_squares = 0
        
        for row in range(8):
            for col in range(8):
                piece = piece = board[row][col]
                if piece != None:
                    if free_squares != 0:
                        fen_board += str(free_squares)
                        free_squares = 0
                    fen_board += pieces_map[2*piece.id + colors_map[piece.color]]
                else:
                    free_squares += 1
            if free_squares != 0:
                fen_board += str(free_squares)
                free_squares = 0
            if row != 7: fen_board += '/'
        
        fen_board += ' '
        fen_board += 'w' if self.turn == "white" else 'b'
        fen_board += ' '
        
        # positions where the pieces should be in order to be able to castle
        if self.castle_rights == '':
            fen_board += '-'
        else:
            fen_board += self.castle_rights
        fen_board += ' '
        
        if self.en_passant == None:
            fen_board += '-'
        else:
            fen_board += self.square_to_uci(self.en_passant[0], self.en_passant[1])
        fen_board += ' '
        
        #############  ADD RULES for fifty rule move and moves count
        fen_board += '0 0'
        return fen_board


        # aggiornare nella tabella fen il castling del bot se
    
    
    def square_to_uci(self, row, col):
        col_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        return col_map[col] + str(8 - row)

    
    def square_from_uci(self, square: str):
        col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        col = col_map[square[0]]
        row = 8 - int(square[1])
        return (row, col)
                
            
    def at_square(self, row, col):
        return self.board[row][col]

    
    def set_piece_at(self, piece, row, col):
        self.board[row][col] = piece
    
    
    def get_pieces(self, color=None):
        if color == None:
            color = self.turn
        
        return [piece for row in self.board for piece in row if piece != None and piece.color == color]
    
    
    def change_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"


    def find_king(self, color):
        for row in self.board:
            for piece in row:
                if piece != None and piece.is_king() and piece.color == color:
                    return piece.row, piece.col
    
    
    def get_king_pos(self, color):
        if color == "white": return self.white_king_pos
        if color == "black": return self.black_king_pos
        else: print("Error in method get_king_pos of class Board")
    
    
    def update_king_pos(self, end_row, end_col):
        if self.turn == "white":
            self.white_king_pos = (end_row, end_col)
        else:
            self.black_king_pos = (end_row, end_col)
    
    
    def is_checkmate(self):
        return self.checkmate
    
    
    def is_stalemate(self):
        return self.stalemate
    
    
    def is_move_inbound(self, start_row, start_col, end_row, end_col):
        return all(elem >= 0 and elem <= 7 for elem in [start_row, start_col, end_row, end_col])
    
    
    def move(self, start_row, start_col, end_row, end_col):
        '''Move the piece from the start position to the end position. Returns the eaten piece if there is one, otherwise None'''
        
        selected_piece = self.board[start_row][start_col]
        eaten_piece = self.board[end_row][end_col]

        self.board[end_row][end_col] = selected_piece
        self.board[start_row][start_col] = None
        selected_piece.row = end_row
        selected_piece.col = end_col
        
        return eaten_piece
    
    
    def update_pseudo_legal_moves(self):
        '''Update the pseudo legal moves of all the pieces'''
        
        for row in self.board:
            for piece in row:
                if piece != None:
                    piece.update_moves(self.board, self.castle_rights, self.en_passant)
    
    
    def update_legal_moves(self, color=None):
        '''Update the legal moves of the pieces with the specified color'''
        ### all'inizio del mio turno aggiorno le mie
        
        if color == None:
            color = self.turn
        
        self.update_pseudo_legal_moves()

        my_pieces = self.get_pieces(color)
        enemy_pieces = self.get_pieces("black") if color == "white" else self.get_pieces("white")
        
        for my_piece in my_pieces:
            new_valid_moves_list = []  # contain all the moves without the valid ones
            start_row = my_piece.row
            start_col = my_piece.col
            
            for move in my_piece.valid_moves_list:
                move_has_to_be_removed = False
                end_col, end_row = move

                # do the move
                eaten_piece = self.move(start_row, start_col, end_row, end_col) ###########  FORSE QUA SE NON FACCIO EXECUTE SBALGIO ROBA????
                
                if my_piece.is_king():
                    king_row = end_row
                    king_col = end_col
                else:
                    king_row, king_col = self.get_king_pos(color)
                
                # control if after the move the king would be under check
                for enemy_piece in enemy_pieces:
                    if enemy_piece != eaten_piece:
                        enemy_piece.update_moves(self.board, self.castle_rights, self.en_passant)
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
                self.set_piece_at(eaten_piece, end_row, end_col)
                
                if eaten_piece != None:
                    eaten_piece.update_moves(self.board, self.castle_rights, self.en_passant)
            
            # update the list of the valid moves
            my_piece.valid_moves_list = new_valid_moves_list
    
    
    def is_legal_move(self, start_row, start_col, end_row, end_col):
        selected_piece = self.at_square(start_row, start_col)
        
        if selected_piece == None:
            return False
        
        return selected_piece.valid_moves_table[end_row][end_col]

    
    def en_passant_capture(self, piece):
        if (piece.row, piece.col) == self.en_passant:
            if piece.color == 'white': forward = -1
            else: forward = 1
            
            self.eaten_pieces[0].append(self.board[piece.row - forward][piece.col])
            self.board[piece.row - forward][piece.col] = None
    
    
    def move_castled_rook(self, end_row, end_col):
        if 'K' in self.castle_rights and end_row == 7 and end_col == 6:
            self.move(7, 7, 7, 5)
        elif 'Q' in self.castle_rights and end_row == 7 and end_col == 2:
            self.move(7, 0, 7, 3)
        if 'k' in self.castle_rights and end_row == 0 and end_col == 6:
            self.move(0, 7, 0, 5)
        elif 'q' in self.castle_rights and end_row == 0 and end_col == 2:
            self.move(0, 0, 0, 3)
    
    
    def update_castle_rights(self, piece, start_row, start_col):
        if piece.is_king():
            if piece.color == "white":
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
    
    
    def update_en_passant_reference(self, piece, start_row, end_row, end_col):
        self.en_passant = None
        
        if piece.color == "white" and start_row == 6 and end_row == 4:
            self.en_passant = (5, end_col)
        elif piece.color == "black" and start_row == 1 and end_row == 3:
            self.en_passant = (2, end_col)

    
    def execute_move(self, start_row, start_col, end_row, end_col, from_bot=False):
        '''Execute a move, with all the other things that should change with it'''

        piece = self.board[start_row][start_col]
        
        # move the selected piece and add it (if there is one) to the eaten pieces
        eaten_piece = self.move(start_row, start_col, end_row, end_col)
        if eaten_piece != None:
            self.eaten_pieces[eaten_piece.id].append(eaten_piece)
        
        if piece.is_king():
            self.update_king_pos(end_row, end_col)
            self.move_castled_rook(end_row, end_col)  # it does something only if there was a castling
        
        if piece.is_king() or piece.is_rook():
            self.update_castle_rights(piece, start_row, start_col)
        
        if piece.is_pawn():
            self.en_passant_capture(piece)  # it does something if there was an en passant
            self.update_en_passant_reference(piece, start_row, end_row, end_col)
        
        if not piece.is_pawn():
            self.en_passant = None  # reset en passant

        # handle the promotion, which is different between player and bot
        if piece.is_pawn() and (piece.row == 0 or piece.row == 7):
            if not from_bot:
                self.promotion_square = (end_row, end_col)
            else:
                self.board[end_row][end_col] = Queen(end_row, end_col, piece.color)
        
        # reset the possibility to perform en passant to none if you are the one who just moved
        # if not from_server: self.reset_en_passant()
 

    def promote(self, new_piece: str, color: str):
        row, col = self.promotion_square
        if new_piece == 'q':
            new_piece = Queen(row, col, color)
        elif new_piece == 'r':
            new_piece = Rook(row, col, color)
        elif new_piece == 'b':
            new_piece = Bishop(row, col, color)
        elif new_piece == 'k':
            new_piece = Knight(row, col, color)
        
        self.board[row][col] = new_piece
        self.promotion_square = None
    
    
    def end_turn_multi_player(self, client, start_row, start_col, end_row, end_col, promotion_piece='x'):
        self.my_turn = False
        print("Setting my turn to False")
        
        # sending move info to the server
        response = client.send(stringify_move(
            client.id, start_row, start_col, end_row, end_col, promotion_piece
        ))
    
    
    def do_bot_move(self, bot_move):
        ########ààà destroy and put everything in singleplayer function
        
        col_map = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        start_row = 8 - int(bot_move[1])
        start_col = col_map[bot_move[0]]
        end_row = 8 - int(bot_move[3])
        end_col = col_map[bot_move[2]]
        
        self.execute_move(start_row, start_col, end_row, end_col, from_bot=True)
    
    
    def check_if_loser(self, color):
        '''Check if player of the given color is under checkmate or stalemate.
        Remember to update the player/bot moves before cheking if he lost'''
        
        my_color = color
        enemy_color = "black" if color == "white" else "white"
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
                enemy_piece.update_moves(self.board, self.castle_rights, self.en_passant)
                if enemy_piece.valid_moves_table[king_row][king_col] == True:
                    self.checkmate = True
                    self.winner = enemy_color
                    break
            else:
                self.stalemate = True