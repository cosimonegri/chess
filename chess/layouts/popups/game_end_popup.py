import pygame
from layouts.popup import Popup
from layouts.button import Button
from constants import GREY, BLACK


class GameEndPopup(Popup):
    
    # ratios are relative to the screen
    GAME_END_POPUP_WIDTH_RATIO = 32
    GAME_END_POPUP_HEIGHT_RATIO = 33
    GAME_END_POPUP_BORDER_WIDTH = 3

    def __init__(self, width_ratio=GAME_END_POPUP_WIDTH_RATIO,
        height_ratio=GAME_END_POPUP_HEIGHT_RATIO, border_width=GAME_END_POPUP_BORDER_WIDTH,
        font_name="Roboto", small_font_size=32, big_font_size=48, text_color=BLACK
    ):
        super().__init__(width_ratio, height_ratio)
        self.border_width = border_width
        
        self.font_name = font_name
        self.big_font_size = big_font_size
        self.small_font_size = small_font_size
        self.text_color = text_color
        
        self.back_menu_button = GameEndButton("MENU")
    
    
    def update(self, screen, fullscreen, player_color, winner):
        self.update_position(screen)
        self.update_font(fullscreen)
        
        self.back_menu_button.update_position(self.width, self.height, self.left, self.top)
        self.back_menu_button.update_font(self.font)
        
        self.find_message(player_color, winner)
    
    
    def update_position(self, screen):
        win_width, win_height = screen.get_size()
        self.width = (win_width * self.width_ratio) / 100
        self.height = (win_height * self.height_ratio) / 100
        self.left = (win_width - self.width) / 2
        self.top = (win_height - self.height) / 2
    
    
    def update_font(self, fullscreen):
        if fullscreen:
            self.font = pygame.font.SysFont(self.font_name, self.big_font_size)
        else:
            self.font = pygame.font.SysFont(self.font_name, self.small_font_size)
    
    
    def find_message(self, player_color, winner):
        if winner == None:
            self.message = "Draw"
        else:
            if winner == player_color:
                self.message = "You won!"
            else:
                self.message = "You lost"
        
        self.text_surface = self.font.render(self.message, 1, self.text_color)
    
    
    def draw(self, screen, mouse_pos):
        line_width = 2
        line_top_ratio = 3.3
        
        # background and border
        pygame.draw.rect(screen, GREY, (self.left, self.top, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.left, self.top, self.width, self.height), self.border_width)
        pygame.draw.line(screen, BLACK, (self.left, self.top + (self.height / line_top_ratio)),
            (self.left + self.width - self.border_width, self.top + (self.height / line_top_ratio)), line_width
        )
        
        # win, loss, draw message
        text_rect = self.text_surface.get_rect(
            center=(self.left + (self.width/2), 0), top = self.top + self.height/10
        )
        screen.blit(self.text_surface, text_rect)
        
        # back home button
        self.back_menu_button.draw(screen, mouse_pos)
        
    
    def handle_click(self, mouse_pos):
        if self.back_menu_button.is_focused(mouse_pos):
            return True
        else: return False



class GameEndButton(Button):
    
    # ratios relative to the popup
    GAME_END_BUTTON_WIDTH_RATIO = 90
    GAME_END_BUTTON_HEIGHT_RATIO = 55
    GAME_END_BUTTON_TOP_RATIO = 38

    def __init__(self, text, left_ratio=None, top_ratio=GAME_END_BUTTON_TOP_RATIO,
        w_ratio=GAME_END_BUTTON_WIDTH_RATIO, h_ratio=GAME_END_BUTTON_HEIGHT_RATIO
    ):
        super().__init__(left_ratio, top_ratio, w_ratio, h_ratio)
        self.text = text
    
    
    def update_position(self, popup_width, popup_height, popup_left, popup_top):
        self.width = (popup_width * self.w_ratio) / 100
        self.height = (popup_height * self.h_ratio) / 100
        self.left = popup_left + (popup_width - self.width) / 2
        self.top = popup_top + (popup_height * self.top_ratio) / 100
    
    
    def update_font(self, font):
        self.font = font
        self.text_surface = self.font.render(self.text, 1, self.text_color)
    
    
    def draw(self, screen, mouse_pos):
        if self.is_focused(mouse_pos):
            background_color = self.hover_color
        else:
            background_color = self.color
        
        pygame.draw.rect(screen, background_color, (self.left, self.top, self.width, self.height))
        text_rect = self.text_surface.get_rect(
            center=(self.left + self.width/2, self.top + self.height/2)
        )
        screen.blit(self.text_surface, text_rect)