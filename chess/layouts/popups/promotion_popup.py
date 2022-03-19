import pygame
from layouts.popup import Popup
from layouts.button import Button
from constants import GREY, BLACK, SELECT_COLOR, PIECES_PATHS, ALT_PIECES_PATHS, QUEEN_ID, ROOK_ID, BISHOP_ID, KNIGHT_ID


class PromotionPopup(Popup):
    PROMOTION_POPUP_WIDTH_RATIO = 32
    PROMOTION_POPUP_HEIGHT_RATIO = 33
    PROMOTION_POPUP_BORDER_WIDTH = 3

    def __init__(
        self, width_ratio=PROMOTION_POPUP_WIDTH_RATIO,
        height_ratio=PROMOTION_POPUP_HEIGHT_RATIO, border_width=PROMOTION_POPUP_BORDER_WIDTH
    ):
        super().__init__(width_ratio, height_ratio)
        self.border_width = border_width

        self.white_buttons = None
        self.black_buttons = None
        self.get_buttons_images()


    def get_buttons_images(self):
        try:
            self.white_buttons = [
                PromotionButton(pygame.image.load(PIECES_PATHS["white"][QUEEN_ID]), 0, 0),
                PromotionButton(pygame.image.load(PIECES_PATHS["white"][ROOK_ID]), 50, 0),
                PromotionButton(pygame.image.load(PIECES_PATHS["white"][BISHOP_ID]), 0, 50),
                PromotionButton(pygame.image.load(PIECES_PATHS["white"][KNIGHT_ID]), 50, 50),
            ]
            self.black_buttons = [
                PromotionButton(pygame.image.load(PIECES_PATHS["black"][QUEEN_ID]), 0, 0),
                PromotionButton(pygame.image.load(PIECES_PATHS["black"][ROOK_ID]), 50, 0),
                PromotionButton(pygame.image.load(PIECES_PATHS["black"][BISHOP_ID]), 0, 50),
                PromotionButton(pygame.image.load(PIECES_PATHS["black"][KNIGHT_ID]), 50, 50),
            ]
        except:
            self.white_buttons = [
                PromotionButton(pygame.image.load(ALT_PIECES_PATHS["white"][QUEEN_ID]), 0, 0),
                PromotionButton(pygame.image.load(ALT_PIECES_PATHS["white"][ROOK_ID]), 50, 0),
                PromotionButton(pygame.image.load(ALT_PIECES_PATHS["white"][BISHOP_ID]), 0, 50),
                PromotionButton(pygame.image.load(ALT_PIECES_PATHS["white"][KNIGHT_ID]), 50, 50),
            ]
            self.black_buttons = [
                PromotionButton(pygame.image.load(ALT_PIECES_PATHS["black"][QUEEN_ID]), 0, 0),
                PromotionButton(pygame.image.load(ALT_PIECES_PATHS["black"][ROOK_ID]), 50, 0),
                PromotionButton(pygame.image.load(ALT_PIECES_PATHS["black"][BISHOP_ID]), 0, 50),
                PromotionButton(pygame.image.load(ALT_PIECES_PATHS["black"][KNIGHT_ID]), 50, 50),
            ]
    
    
    def update(self, win_size, player_color):
        win_width, win_height = win_size
        self.width = (win_width * self.width_ratio) // 100
        self.height = (win_height * self.height_ratio) // 100
        self.left = (win_width - self.width) // 2
        self.top = (win_height - self.height) // 2
        
        if player_color == "white":
            self.buttons = self.white_buttons
        else:
            self.buttons = self.black_buttons
        
        for button in self.buttons:
            button.update_position(self.width, self.height, self.left, self.top)
    
    
    def draw(self, screen, win_size, mouse_pos):
        win_width, win_height = win_size
        
        # background
        pygame.draw.rect(screen, GREY, (self.left, self.top, self.width, self.height))
        
        # buttons
        for button in self.buttons:
            button.draw(screen, mouse_pos)
        
        # border
        pygame.draw.rect(screen, BLACK, (self.left, self.top, self.width, self.height), self.border_width)
        
        # buttons borders
        line_width = 2
        pygame.draw.line(screen, BLACK, (win_width // 2 - line_width // 2, self.top),
            (win_width // 2 - line_width // 2, self.top + self.height - self.border_width), line_width
        )
        pygame.draw.line(screen, BLACK, (self.left, win_height // 2 - line_width // 2),
            (self.left + self.width - self.border_width, win_height // 2 - line_width // 2), line_width
        )
    
    
    def handle_click(self, mouse_pos):
        if self.buttons[0].is_focused(mouse_pos):
            return 'q'
        if self.buttons[1].is_focused(mouse_pos):
            return 'r'
        if self.buttons[2].is_focused(mouse_pos):
            return 'b'
        if self.buttons[3].is_focused(mouse_pos):
            return 'k'
        return None



class PromotionButton(Button):
    
    # ratios relative to the popup
    PROMOTION_BUTTON_WIDTH_RATIO = 50
    PROMOTION_BUTTON_HEIGHT_RATIO = 50
    
    def __init__(self, image, left_ratio, top_ratio,
        w_ratio=PROMOTION_BUTTON_WIDTH_RATIO, h_ratio=PROMOTION_BUTTON_HEIGHT_RATIO
    ):
        super().__init__(left_ratio, top_ratio, w_ratio, h_ratio)
        self.image = image
    
    
    def update_position(self, popup_width, popup_height, popup_left, popup_top):
        self.width = (popup_width * self.w_ratio) // 100
        self.height = (popup_height * self.h_ratio) // 100
        self.left = popup_left + (popup_width * self.left_ratio) // 100
        self.top = popup_top + (popup_height * self.top_ratio) // 100
    
    
    def draw(self, screen, mouse_pos):
        if self.is_focused(mouse_pos):
            color = SELECT_COLOR
        else:
            color = GREY
        
        pygame.draw.rect(screen, color, (self.left, self.top, self.width, self.height))
        
        scaled_img = pygame.transform.scale(self.image, (self.height, self.height))
        screen.blit(scaled_img.convert_alpha(), (self.left + (self.width - self.height) // 2, self.top - 4))