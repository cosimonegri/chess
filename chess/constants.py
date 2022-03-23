import pygame

# small screen size (no fullscreen)
WIN_WIDTH = 850
WIN_HEIGHT = 520

BACKGROUND_FADE = 200  # to fade the background

# Main colors
WHITE = (255, 255, 255)
GREY = (230,230,230)
DARK_GREY = (150, 150, 150)
BLACK = (0, 0, 0)
DARK_BROWN = (181,136,99)
LIGHT_BROWN = (240,217,181)
SELECT_COLOR = (249,188,56)
RED = (255,30,30)


LOADING_POINTS_NUM = 4  # max number of dynamic points in the "waiting for an opponent" animation
MAX_NAME_LENGHT = 10
FPS = 80
TIMER = 0.5  # time between requests to the server
DRAWS_AFTER_MINIMIZE = 3  # number of times to draw after the user exits fullscreen mode (to fix Linux black screen)


#pieces ids
PAWN_ID = 0
KNIGHT_ID = 1
BISHOP_ID = 2
ROOK_ID = 3
QUEEN_ID = 4
KING_ID = 5

# relatives paths of pieces images (index corresponds to piece id)
PIECES_PATHS = {
    "white": [
        './assets/Images/white-pawn.png',
        './assets/Images/white-knight.png',
        './assets/Images/white-bishop.png',
        './assets/Images/white-rook.png',
        './assets/Images/white-queen.png',
        './assets/Images/white-king.png'
    ],
    "black": [
        './assets/Images/black-pawn.png',
        './assets/Images/black-knight.png',
        './assets/Images/black-bishop.png',
        './assets/Images/black-rook.png',
        './assets/Images/black-queen.png',
        './assets/Images/black-king.png'
    ]
}

# alternative relatives paths
ALT_PIECES_PATHS = {
    "white": [
        './chess/assets/Images/white-pawn.png',
        './chess/assets/Images/white-knight.png',
        './chess/assets/Images/white-bishop.png',
        './chess/assets/Images/white-rook.png',
        './chess/assets/Images/white-queen.png',
        './chess/assets/Images/white-king.png'
    ],
    "black": [
        './chess/assets/Images/black-pawn.png',
        './chess/assets/Images/black-knight.png',
        './chess/assets/Images/black-bishop.png',
        './chess/assets/Images/black-rook.png',
        './chess/assets/Images/black-queen.png',
        './chess/assets/Images/black-king.png'
    ]
}