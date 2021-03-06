PIECES_VALUES = {'P':  100, 'N':  320, 'B':  330, 'R':  500, 'Q':  900, 'K':  20000,
                 'p': -100, 'n': -320, 'b': -330, 'r': -500, 'q': -900, 'k': -20000}

POSITIONS_VALUES = {
    "start": {
        'P': [
             0,  0,  0,  0,  0,  0,  0,  0,
             5, 10, 10,-20,-20, 10, 10,  5,
             5, -5,-10,  0,  0,-10, -5,  5,
             0,  0,  0, 20, 20,  0,  0,  0,
             5,  5, 10, 25, 25, 10,  5,  5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
             0,  0,  0,  0,  0,  0,  0,  0,
        ],
        'N': [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50,
        ],
        'B': [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10,-10,-10,-10,-10,-20,
        ],
        'R': [
             0,  0,  0,  5,  5,  0,  0,  0,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
             5, 10, 10, 10, 10, 10, 10,  5,
             0,  0,  0,  0,  0,  0,  0,  0,
        ],
        'Q': [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -10,  5,  5,  5,  5,  5,  0,-10,
              0,  0,  5,  5,  5,  5,  0, -5,
             -5,  0,  5,  5,  5,  5,  0, -5,
            -10,  0,  5,  5,  5,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20,
        ],
        'K': [
             20, 30, 10,  0,  0, 10, 30, 20,
             20, 20,  0,  0,  0,  0, 20, 20,
            -10,-20,-20,-20,-20,-20,-20,-10,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
        ],
        'p': [
              0,  0,  0,  0,  0,  0,  0,  0,
            -50,-50,-50,-50,-50,-50,-50,-50,
            -10,-10,-20,-30,-30,-20,-10,-10,
             -5, -5,-10,-25,-25,-10, -5, -5,
              0,  0,  0,-20,-20,  0,  0,  0,
             -5,  5, 10,  0,  0, 10,  5, -5,
             -5,-10,-10, 20, 20,-10,-10, -5,
              0,  0,  0,  0,  0,  0,  0,  0,
        ],
        'n': [
            50, 40, 30, 30, 30, 30, 40, 50,
            40, 20,  0,  0,  0,  0, 20, 40,
            30,  0,-10,-15,-15,-10,  0, 30,
            30, -5,-15,-20,-20,-15, -5, 30,
            30,  0,-15,-20,-20,-15,  0, 30,
            30, -5,-10,-15,-15,-10, -5, 30,
            40, 20,  0, -5, -5,  0, 20, 40,
            50, 40, 30, 30, 30, 30, 40, 50,
        ],
        'b': [
            20, 10, 10, 10, 10, 10, 10, 20,
            10,  0,  0,  0,  0,  0,  0, 10,
            10,  0, -5,-10,-10, -5,  0, 10,
            10, -5, -5,-10,-10, -5, -5, 10,
            10,  0,-10,-10,-10,-10,  0, 10,
            10,-10,-10,-10,-10,-10,-10, 10,
            10, -5,  0,  0,  0,  0, -5, 10,
            20, 10, 10, 10, 10, 10, 10, 20,
        ],
        'r': [
            0,  0,  0,  0,  0,  0,  0,  0,
            5,-10,-10,-10,-10,-10,-10,  5,
            5,  0,  0,  0,  0,  0,  0,  5,
            5,  0,  0,  0,  0,  0,  0,  5,
            5,  0,  0,  0,  0,  0,  0,  5,
            5,  0,  0,  0,  0,  0,  0,  5,
            5,  0,  0,  0,  0,  0,  0,  5,
            0,  0,  0, -5, -5,  0,  0,  0,
        ],
        'q': [
            20, 10, 10,  5,  5, 10, 10, 20,
            10,  0,  0,  0,  0,  0,  0, 10,
            10,  0, -5, -5, -5, -5,  0, 10,
             5,  0, -5, -5, -5, -5,  0,  5,
             0,  0, -5, -5, -5, -5,  0,  5,
            10, -5, -5, -5, -5, -5,  0, 10,
            10,  0, -5,  0,  0,  0,  0, 10,
            20, 10, 10,  5,  5, 10, 10, 20,
        ],
        'k': [
             30, 40, 40, 50, 50, 40, 40, 30,
             30, 40, 40, 50, 50, 40, 40, 30,
             30, 40, 40, 50, 50, 40, 40, 30,
             30, 40, 40, 50, 50, 40, 40, 30,
             20, 30, 30, 40, 40, 30, 30, 20,
             10, 20, 20, 20, 20, 20, 20, 10,
            -20,-20,  0,  0,  0,  0,-20,-20,
            -20,-30,-10,  0,  0,-10,-30,-20,
        ],
    },
    
    "end": {
        'P': [
              0,  0,  0,  0,  0,  0,  0,  0,
            -40,-40,-40,-20,-20,-40,-40,-40,
            -20,-20,-20,-10,-10,-20,-20,-20,
             -5, -5, -5,  0,  0, -5, -5, -5,
             10, 10, 10, 10, 10, 10, 10, 10,
             30, 30, 30, 30, 30, 30, 30, 30,
             80, 80, 80, 80, 80, 80, 80, 80,
              0,  0,  0,  0,  0,  0,  0,  0,
        ],
        'N': [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50,
        ],
        'B': [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10,-10,-10,-10,-10,-20,
        ],
        'R': [
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
        ],
        'Q': [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -10,  5,  5,  5,  5,  5,  0,-10,
              0,  0,  5,  5,  5,  5,  0, -5,
             -5,  0,  5,  5,  5,  5,  0, -5,
            -10,  0,  5,  5,  5,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20,
        ],
        'K': [
            -50,-30,-30,-30,-30,-30,-30,-50,
            -30,-30,  0,  0,  0,  0,-30,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 30, 40, 40, 30,-10,-30,
            -30,-10, 20, 30, 30, 20,-10,-30,
            -30,-20,-10,  0,  0,-10,-20,-30,
            -50,-40,-30,-20,-20,-30,-40,-50,
        ],
        'p': [
              0,  0,  0,  0,  0,  0,  0,  0,
            -80,-80,-80,-80,-80,-80,-80,-80,
            -30,-30,-30,-30,-30,-30,-30,-30,
            -10,-10,-10,-10,-10,-10,-10,-10,
              5,  5,  5,  0,  0,  5,  5,  5,
             20, 20, 20, 10, 10, 20, 20, 20,
             40, 40, 40, 20, 20, 40, 40, 40,
              0,  0,  0,  0,  0,  0,  0,  0,
        ],
        'n': [
            50, 40, 30, 30, 30, 30, 40, 50,
            40, 20,  0,  0,  0,  0, 20, 40,
            30,  0,-10,-15,-15,-10,  0, 30,
            30, -5,-15,-20,-20,-15, -5, 30,
            30,  0,-15,-20,-20,-15,  0, 30,
            30, -5,-10,-15,-15,-10, -5, 30,
            40, 20,  0, -5, -5,  0, 20, 40,
            50, 40, 30, 30, 30, 30, 40, 50,
        ],
        'b': [
            20, 10, 10, 10, 10, 10, 10, 20,
            10,  0,  0,  0,  0,  0,  0, 10,
            10,  0, -5,-10,-10, -5,  0, 10,
            10, -5, -5,-10,-10, -5, -5, 10,
            10,  0,-10,-10,-10,-10,  0, 10,
            10,-10,-10,-10,-10,-10,-10, 10,
            10, -5,  0,  0,  0,  0, -5, 10,
            20, 10, 10, 10, 10, 10, 10, 20,
        ],
        'r': [
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
            0,  0,  0,  0,  0,  0,  0,  0,
        ],
        'q': [
            20, 10, 10,  5,  5, 10, 10, 20,
            10,  0,  0,  0,  0,  0,  0, 10,
            10,  0, -5, -5, -5, -5,  0, 10,
             5,  0, -5, -5, -5, -5,  0,  5,
             0,  0, -5, -5, -5, -5,  0,  5,
            10, -5, -5, -5, -5, -5,  0, 10,
            10,  0, -5,  0,  0,  0,  0, 10,
            20, 10, 10,  5,  5, 10, 10, 20,
        ],
        'k': [
            50, 40, 30, 20, 20, 30, 40, 50,
            30, 20, 10,  0,  0, 10, 20, 30,
            30, 10,-20,-30,-30,-20, 10, 30,
            30, 10,-30,-40,-40,-30, 10, 30,
            30, 10,-30,-40,-40,-30, 10, 30,
            30, 10,-20,-30,-30,-20, 10, 30,
            30, 30,  0,  0,  0,  0, 30, 30,
            50, 30, 30, 30, 30, 30, 30, 50
        ],
    }
}