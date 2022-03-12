import pygame
from layouts.screen import Screen
from constants import BLACK, GREY, DARK_BROWN, LIGHT_BROWN, SELECT_COLOR, PIECES_PATHS, ALT_PIECES_PATHS

# ratios relative to the tile size
# small circle in the tile where you can move, big circle in the tiles where you can move and capture a piece
SMALL_CIRCLE_RADIUS_RATIO = 15
BIG_CIRCLE_RADIUS_RATIO = 42
BIG_CIRCLE_WIDTH_RATIO = 6


class GameScreen(Screen):
    def __init__(self, title, monitor_size, board, game_state,
        font_name="Roboto", big_font_size=50, small_font_size=34, normal_color=BLACK, highlight_color=SELECT_COLOR
    ):
        super().__init__(title, monitor_size)
        self.board = board
        self.game_state = game_state
        
        self.font_name = font_name
        self.big_font_size = big_font_size
        self.small_font_size = small_font_size
        self.normal_color = normal_color
        self.highlight_color = highlight_color

        self.pieces_images = {"white": [], "black": []}
        try:
            for key, value in ALT_PIECES_PATHS.items():
                self.pieces_images[key] = list(map(lambda path: pygame.image.load(path), value))
        except:
            for key, value in PIECES_PATHS.items():
                self.pieces_images[key] = list(map(lambda path: pygame.image.load(path), value))
    
    
    def draw(self, board):
        self.draw_tiles()
        self.draw_pieces(board.board)
        
        if board.selected_piece != None:
            self.draw_valid_moves(board.board, board.selected_piece)
            self.draw_moving_piece(board.selected_piece)
        
        self.draw_eaten_pieces(board.eaten_pieces)
        self.draw_players_info()
    
    
    def update_content(self):
        win_width, win_height = self.win_size
        self.tile_size = win_height / 8
        
        if self.fullscreen:
            self.font = pygame.font.SysFont(self.font_name, self.big_font_size)
        else:
            self.font = pygame.font.SysFont(self.font_name, self.small_font_size)
        
        if self.board.turn == self.game_state["my_color"]:
            my_name_color = self.highlight_color
            enemy_name_color = self.normal_color
        else:
            my_name_color = self.normal_color
            enemy_name_color = self.highlight_color
        
        self.my_name_surface = self.font.render(self.game_state["my_name"], 1, my_name_color)
        self.enemy_name_surface = self.font.render(self.game_state["enemy_name"], 1, enemy_name_color)
    
    
    def draw_tiles(self):
        screen = self.screen
        win_width, win_height = self.win_size
        tile_size = self.tile_size
        screen.fill(GREY)
        
        for row in range(8):
            for col in range(0, 8, 2):
                if row % 2 == 0:
                    pygame.draw.rect(screen, LIGHT_BROWN, (col*tile_size + \
                        (win_width - win_height) / 2, row*tile_size, tile_size, tile_size))
                    pygame.draw.rect(screen, DARK_BROWN, ((col+1)*tile_size + \
                        (win_width - win_height) / 2, row*tile_size, tile_size, tile_size))
                else:
                    pygame.draw.rect(screen, DARK_BROWN, (col*tile_size + \
                        (win_width - win_height) / 2, row*tile_size, tile_size, tile_size))
                    pygame.draw.rect(screen, LIGHT_BROWN, ((col+1)*tile_size + \
                        (win_width - win_height) / 2, row*tile_size, tile_size, tile_size))
    
    
    def draw_pieces(self, board):
        screen = self.screen
        win_width, win_height = self.win_size
        tile_size = self.tile_size
        
        for row in range(8):
            for col in range(8):
                if board[row][col] != None:
                    scaled_img = pygame.transform.scale(
                        board[row][col].image, (tile_size, tile_size)
                    )
                    
                    if self.game_state["my_color"] == "black": # reflect vertically and horizzontally
                        draw_col = 7 - col
                        draw_row = 7 - row
                    else:
                        draw_col = col
                        draw_row = row
                    
                    screen.blit(scaled_img.convert_alpha(),
                        (draw_col*tile_size + (win_width - win_height) / 2, draw_row*tile_size)
                    )
    
    
    def draw_valid_moves(self, board, selected_piece):
        screen = self.screen
        win_width, win_height = self.win_size
        
        tile_size = self.tile_size
        small_circle_radius = int((tile_size * SMALL_CIRCLE_RADIUS_RATIO) // 100)
        big_circle_radius = int((tile_size * BIG_CIRCLE_RADIUS_RATIO) // 100)
        big_circle_width = int((tile_size * BIG_CIRCLE_WIDTH_RATIO) // 100)
        
        for (col, row) in selected_piece.valid_moves_list:
            if self.game_state["my_color"] == "black": # reflect vertically and horizzontally
                draw_col = 7 - col
                draw_row = 7 - row
            else:
                draw_col = col
                draw_row = row
        
            if board[row][col] == None:
                pygame.draw.circle(screen, SELECT_COLOR,
                    (draw_col*tile_size + tile_size/2+ (win_width - win_height) / 2,
                    draw_row*tile_size + tile_size/2), small_circle_radius
                )
            else:
                pygame.draw.circle(screen, SELECT_COLOR,
                    (draw_col*tile_size + tile_size/2+ (win_width - win_height) / 2,
                     draw_row*tile_size + tile_size/2), big_circle_radius, width=big_circle_width
                )
    
    
    def draw_moving_piece(self, selected_piece):
        x, y = pygame.mouse.get_pos()
        screen = self.screen
        win_width, win_height = self.win_size
        tile_size = self.tile_size
        piece_row, piece_col = selected_piece.row, selected_piece.col
        
        if self.game_state["my_color"] == "black": # reflect vertically and horizzontally
            draw_col = 7 - piece_col
            draw_row = 7 - piece_row
        else:
            draw_col = piece_col
            draw_row = piece_row
        
        # highlight the tile to hide the original piece
        pygame.draw.rect(
            screen, SELECT_COLOR, (draw_col*tile_size + (win_width - win_height) / 2,
            draw_row*tile_size, tile_size, tile_size)
        )
        
        # draw the moving piece
        scaled_img = pygame.transform.scale(selected_piece.image, (tile_size, tile_size))
        self.screen.blit(
            scaled_img.convert_alpha(), (x - tile_size//2, y - tile_size//2)
        )
    
    
    def draw_players_info(self):
        win_width, win_height = self.win_size
        top_offset = win_height / 100 * 5
        
        my_name_rect = self.my_name_surface.get_rect(
            center=((win_width - win_height) / 4, top_offset)
        )
        enemy_name_rect = self.enemy_name_surface.get_rect(
            center=(win_height + (win_width - win_height) * 3 / 4, top_offset)
        )
        
        self.screen.blit(self.my_name_surface, my_name_rect)
        self.screen.blit(self.enemy_name_surface, enemy_name_rect)
    
    
    def draw_eaten_pieces(self, eaten_pieces):
        win_width, win_height = self.win_size
        screen = self.screen
        piece_size = self.tile_size / 10 * 7
        my_color, enemy_color = self.game_state["my_color"], self.game_state["enemy_color"]
        
        you_start_x = (win_width - win_height) / 4 - piece_size
        you_start_y = win_height / 10 * 2
        enemy_start_x = win_height + (win_width - win_height) / 4 * 3 - piece_size
        enemy_start_y = win_height / 10 * 2
        
        you_eaten_number = 0
        enemy_eaten_number = 0
        
        for piece_id in range(5):
            scaled_img = pygame.transform.scale(self.pieces_images[enemy_color][piece_id], (piece_size, piece_size))
            for _ in range(eaten_pieces[enemy_color][piece_id]):

                you_x = you_start_x + (piece_size * (you_eaten_number % 2))
                you_y = you_start_y + (piece_size * (you_eaten_number // 2))
                screen.blit(scaled_img.convert_alpha(), (you_x, you_y))
                you_eaten_number += 1
            
            scaled_img = pygame.transform.scale(self.pieces_images[my_color][piece_id], (piece_size, piece_size))
            for _ in range(eaten_pieces[my_color][piece_id]):

                enemy_x = enemy_start_x + (piece_size * (enemy_eaten_number % 2))
                enemy_y = enemy_start_y + (piece_size * (enemy_eaten_number // 2))
                screen.blit(scaled_img.convert_alpha(), (enemy_x, enemy_y))
                enemy_eaten_number += 1
    
    
    def get_board_row_col(self, mouse_pos):
        x, y = mouse_pos
        win_width, win_height = self.win_size
        tile_size = win_height / 8
        if self.game_state["my_color"] == "white":
            row = int(y // tile_size)
            col = int((x - (win_width - win_height) // 2) // tile_size)
        else:
            row = int(7 - (y // tile_size))
            col = int(7 - ((x - (win_width - win_height) // 2) // tile_size))
        return (row, col)
    
    
    def handle_mouse_icon(self, mouse_pos, board):
        if board.turn == self.game_state["my_color"]:
            row, col = self.get_board_row_col(mouse_pos)
            
            if 0 <= row <= 7 and 0 <= col <= 7:
                if board.board[row][col] != None and board.board[row][col].color == self.game_state["my_color"]:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    return
        
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)