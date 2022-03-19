import pygame
from layouts.screen import Screen
from layouts.button import Button

from constants import BLACK, GREY, DARK_GREY, SELECT_COLOR, BACKGROUND_FADE


try:
    # original background image ratio width:height = 1.777
    BACKGROUND_IMG = pygame.image.load('./assets/Images/chess-background.jpg')
except:
    # original background image ratio width:height = 1.777
    BACKGROUND_IMG = pygame.image.load('./chess/assets/Images/chess-background.jpg')


class MultiplayerSettingsScreen(Screen):
    
    def __init__(self, title, monitor_size,
        font_name="Roboto", big_font_size=50, small_font_size=34, normal_color=BLACK
    ):
        super().__init__(title, monitor_size)
        
        self.font_name = font_name
        self.big_font_size = big_font_size
        self.small_font_size = small_font_size
        self.normal_color = normal_color
        
        self.text_input = TextInput()
        self.start_button = MultiPlayerButton("Start Game")
    
    
    def update_content(self, text=""):
        self.text_input.text = text
        self.text_input.update_position(self.win_size)
        self.text_input.update_font_size(self.fullscreen)
        
        self.start_button.update_position(self.win_size)
        self.start_button.update_font_size(self.fullscreen)
    
    
    def draw(self, mouse_pos, player_name):
        self.screen.fill(self.fill_color)

        BACKGROUND_IMG.convert()
        BACKGROUND_IMG.set_alpha(BACKGROUND_FADE)
        background = pygame.transform.scale(BACKGROUND_IMG, self.win_size)
        self.screen.blit(background, (0, 0))
        
        self.text_input.draw(self.screen, player_name)
        self.start_button.draw(self.screen, mouse_pos, player_name)
    
    
    def handle_click(self, mouse_pos, player_name):
        if self.text_input.is_focused(mouse_pos):
            self.text_input.selected = True
            return True, False
        else:
            self.text_input.selected = False
        
        if self.start_button.is_focused(mouse_pos) and player_name:  # player name is not an empty string
            return False, True
        return False, False


class TextInput():
    TEXT_INPUT_W_RATIO = 40
    TEXT_INPUT_H_RATIO = 15
    TEXT_INPUT_TOP_RATIO = 25

    def __init__(self, left_ratio=None, top_ratio=TEXT_INPUT_TOP_RATIO, w_ratio=TEXT_INPUT_W_RATIO,
        h_ratio=TEXT_INPUT_H_RATIO, color=GREY, hover_color=SELECT_COLOR, text_color1=BLACK, text_color2=DARK_GREY,
        font_name="Roboto", big_font_size=50, small_font_size=34
    ):  
        self.text = ""
        self.alt_text = "Type your name here"
        self.selected = False
        
        self.left_ratio = left_ratio
        self.top_ratio = top_ratio
        self.w_ratio = w_ratio
        self.h_ratio = h_ratio
        self.color = color
        self.hover_color = hover_color
        
        self.font_name = font_name
        self.small_font_size = small_font_size
        self.big_font_size = big_font_size
        self.text_color1 = text_color1
        self.text_color2 = text_color2
    
    
    def is_focused(self, mouse_pos):
        x, y = mouse_pos
        if x >= self.left and x <= self.left + self.width and y >= self.top and y <= self.top + self.height:
            return True
        else: return False
    
    
    def update_font_size(self, fullscreen):
        if fullscreen:
            font_size = self.big_font_size
        else:
            font_size = self.small_font_size
        
        if self.text or self.selected:
            text = self.text
            color = self.text_color1
        else:
            text = self.alt_text
            color = self.text_color2
        
        self.font = pygame.font.SysFont(self.font_name, font_size)
        self.text_surface = self.font.render(text, 1, color)
    
    
    def update_position(self, win_size):
        self.width = (win_size[0] * self.w_ratio) // 100
        self.height = (win_size[1] * self.h_ratio) // 100
        self.left = (win_size[0] - self.width) // 2
        self.top = (win_size[1] * self.top_ratio) // 100
    
    
    def draw(self, screen, player_name):
        if self.selected:
            background_color = self.hover_color
        else:
            background_color = self.color
        
        pygame.draw.rect(screen, background_color, (self.left, self.top, self.width, self.height))
        text_rect = self.text_surface.get_rect(
            center=(self.left + (self.width//2), self.top + (self.height//2))
        )
        screen.blit(self.text_surface, text_rect)



class MultiPlayerButton(Button):
    START_BUTTON_W_RATIO = 40
    START_BUTTON_H_RATIO = 15
    START_BUTTON_TOP_RATIO = 60
    
    def __init__(self, text, left_ratio=None, top_ratio=START_BUTTON_TOP_RATIO,
        w_ratio=START_BUTTON_W_RATIO, h_ratio=START_BUTTON_H_RATIO
    ):
        super().__init__(left_ratio, top_ratio, w_ratio, h_ratio)
        self.text = text
    
    
    def update_position(self, win_size):
        self.width = (win_size[0] * self.w_ratio) // 100
        self.height = (win_size[1] * self.h_ratio) // 100
        self.left = (win_size[0] - self.width) // 2
        self.top = (win_size[1] * self.top_ratio) // 100
    
    
    def draw(self, screen, mouse_pos, player_name):
        if self.is_focused(mouse_pos) and player_name:  # player name is not an empty string
            background_color = self.hover_color
        else:
            background_color = self.color
        
        pygame.draw.rect(screen, background_color, (self.left, self.top, self.width, self.height))
        text_rect = self.text_surface.get_rect(
            center=(self.left + (self.width//2), self.top + (self.height//2))
        )
        screen.blit(self.text_surface, text_rect)