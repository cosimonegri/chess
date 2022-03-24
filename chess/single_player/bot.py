import chess
from single_player.bot_data import PIECES_VALUES, POSITIONS_VALUES
         

def find_move(fen_board: str, color: str, level: int, is_end_game_phase: bool, result: list):
    global EVALUATED
    global USES_POSITIONS
    global MAX_DEPTH
    global GAME_PHASE
    
    if level == 1:
        USES_POSITIONS = False
        MAX_DEPTH = 2
    elif level == 2:
        USES_POSITIONS = True
        MAX_DEPTH = 2
    elif level == 3:
        USES_POSITIONS = False
        MAX_DEPTH = 4
    elif level == 4:
        USES_POSITIONS = True
        MAX_DEPTH = 4
    
    if is_end_game_phase:
        GAME_PHASE = "end"
    else:
        GAME_PHASE = "start"
    
    
    board = chess.Board(fen_board)
    if color == "white":
        board.turn = chess.WHITE
    else:
        board.turn = chess.BLACK
    
    EVALUATED = 0
    best_move= explore_path(board, MAX_DEPTH, float('-inf'), float('inf'), color == "white")
    print(EVALUATED)
    result.append(best_move)
                  

# white tries to maximize, black tries to minimize
def explore_path(board, depth, alpha, beta, maximize):
    global EVALUATED

    # leaf node reached, evaluate the score of the position
    if depth == 0 or board.outcome() != None:
        return evaluate(board, maximize)
    
    # maximizing player
    if maximize:
        max_eval = float('-inf')
        best_move = None
        
        legal_moves = order_moves(board.legal_moves, board)
        for move in legal_moves:
            
            new_board = board.copy()
            new_board.push(move)
            EVALUATED += 1
            eval = explore_path(new_board, depth-1, alpha, beta, False)
            
            if eval > max_eval:
                max_eval = eval
                best_move = move
            
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        
        if depth == MAX_DEPTH:
            # print(f"max eval: {max_eval}")
            # print(f"best move: {best_move}")
            return best_move
        else:
            return max_eval
    
    # minimizing player
    else:
        min_eval = float('inf')
        best_move = None
        
        legal_moves = order_moves(board.legal_moves, board)
        for move in legal_moves:
            
            new_board = board.copy()
            new_board.push(move)
            EVALUATED += 1
            eval = explore_path(new_board, depth-1, alpha, beta, True)
            
            if eval < min_eval:
                min_eval = eval
                best_move = move
            
            beta = min(beta, eval)
            if beta <= alpha:
                break
        
        if depth == MAX_DEPTH:
            # print(f"min eval: {min_eval}")
            # print(f"best move: {best_move}")
            return best_move
        else:
            return min_eval
    

def evaluate(board, maximize):
    # if board.is_checkmate():
    #     if maximize:
    #         return float('-inf')
    #     else:
    #         return float('inf')
    
    # if board.is_stalemate():
    #     return 0
    # if board.is_insufficient_material():
    #     return 0

    eval = 0
    for square in range(64):
        if board.piece_at(square) != None:
            piece = board.piece_at(square).symbol()
            eval += PIECES_VALUES[piece]
            if USES_POSITIONS:
                eval += POSITIONS_VALUES[GAME_PHASE][piece][square]
    
    return eval


def order_moves(moves, board):
    score_guesses = []
    
    for move in moves:
        score_guess = 0
        moving_piece = board.piece_at(move.from_square)
        eaten_piece = board.piece_at(move.to_square)
        
        if eaten_piece != None:
            score_guess += abs(PIECES_VALUES[eaten_piece.symbol()]) \
                - abs(PIECES_VALUES[moving_piece.symbol()])
        
        ### piece score for a promotion
        
        score_guesses.append(score_guess)
    
    return [move for _, move in sorted(zip(score_guesses, moves), key=lambda pair: pair[0])]