import pygame
from layouts.screen import Screen
from layouts.button import Button
from constants import BACKGROUND_FADE


LEVELS_NUMBER = 4  # number of possible bot difficulty levels


COLOR_BUTTON_W_RATIO = 20
COLOR_BUTTON_H_RATIO = 12
COLOR_BUTTON_TOP_RATIO = 10
COLOR_BUTTON_PADDING_RATIO = 10
    
LEVEL_BUTTON_W_RATIO = 12
LEVEL_BUTTON_H_RATIO = 12
LEVEL_BUTTON_TOP_RATIO = 30
LEVEL_BUTTON_PADDING_RATIO = 6
    
START_BUTTON_W_RATIO = 30
START_BUTTON_H_RATIO = 12
START_BUTTON_TOP_RATIO = 70


try:
    # original background image ratio width:height = 1.777
    BACKGROUND_IMG = pygame.image.load('./assets/Images/chess-background.jpg')
except:
    # original background image ratio width:height = 1.777
    BACKGROUND_IMG = pygame.image.load('./chess/assets/Images/chess-background.jpg')


class SingleplayerSettingsScreen(Screen):
    
    def __init__(self, title, monitor_size):
        super().__init__(title, monitor_size)
        
        self.button_color_white = SinglePlayerButton("White", id="white")
        self.button_color_black = SinglePlayerButton("Black", id="black")
        
        self.button_lvl_1 = SinglePlayerButton("LvL 1", id=1)
        self.button_lvl_2 = SinglePlayerButton("LvL 2", id=2)
        self.button_lvl_3 = SinglePlayerButton("LvL 3", id=3)
        self.button_lvl_4 = SinglePlayerButton("LvL 4", id=4)
        
        self.button_start_game = SinglePlayerButton("Start Game", id="start")
        
        self.buttons = [
            self.button_color_white, self.button_color_black,
            self.button_lvl_1, self.button_lvl_2, self.button_lvl_3, self.button_lvl_4,
            self.button_start_game
        ]
        self.selected_buttons_id = ["white", 1]  # default single player settings, that will be changed by the user
    
    
    def update_content(self):
        for button in self.buttons:
            button.update_position(self.win_size)
            button.update_font_size(self.fullscreen)
    
    
    def draw(self, mouse_pos):
        self.screen.fill(self.fill_color)

        BACKGROUND_IMG.convert()
        BACKGROUND_IMG.set_alpha(BACKGROUND_FADE)
        background = pygame.transform.scale(BACKGROUND_IMG, self.win_size)
        self.screen.blit(background, (0, 0))
        
        for button in self.buttons:
            button.draw(self.screen, mouse_pos, self.selected_buttons_id)
    
    
    def handle_click(self, mouse_pos):
        '''Returns the choosen settings if the game has started, otherwise None'''
        
        for button in self.buttons:
            if button.is_focused(mouse_pos):
                if button.id == "start":
                    return self.selected_buttons_id
                else:
                    if type(button.id) == str:
                        self.selected_buttons_id[0] = button.id
                        return None
                    else:
                        self.selected_buttons_id[1] = button.id
                        return None



class SinglePlayerButton(Button):
    
    def __init__(self, text, id=None):
        self.text = text
        self.id = id
        self.init_dimensions()
    
    
    def init_dimensions(self):
        if self.id == "start":
            w_ratio = START_BUTTON_W_RATIO
            h_ratio = START_BUTTON_H_RATIO
            top_ratio = START_BUTTON_TOP_RATIO
            padding_ratio = 0
            
            start_left_ratio = (100 - w_ratio) / 2
            button_number = 0
        else:
            if type(self.id) == str:
                w_ratio = COLOR_BUTTON_W_RATIO
                h_ratio = COLOR_BUTTON_H_RATIO
                top_ratio = COLOR_BUTTON_TOP_RATIO
                padding_ratio = COLOR_BUTTON_PADDING_RATIO
                
                start_left_ratio = (100 - w_ratio*2 - padding_ratio) / 2
                button_number = 0 if self.id == "white" else 1
            else:
                w_ratio = LEVEL_BUTTON_W_RATIO
                h_ratio = LEVEL_BUTTON_H_RATIO
                top_ratio = LEVEL_BUTTON_TOP_RATIO
                padding_ratio = LEVEL_BUTTON_PADDING_RATIO
                
                start_left_ratio = (100 - w_ratio*LEVELS_NUMBER - padding_ratio*(LEVELS_NUMBER-1)) / 2
                button_number = self.id - 1
        
        left_ratio = start_left_ratio + (w_ratio + padding_ratio) * button_number
        super().__init__(left_ratio, top_ratio, w_ratio, h_ratio)
    
    
    def update_position(self, win_size):
        self.left = (win_size[0] * self.left_ratio) / 100
        self.top = (win_size[1] * self.top_ratio) / 100
        self.width = (win_size[0] * self.w_ratio) / 100
        self.height = (win_size[1] * self.h_ratio) / 100
    
    
    def draw(self, screen, mouse_pos, selected_buttons_id):
        if self.id in selected_buttons_id or self.is_focused(mouse_pos):
            background_color = self.hover_color
        else:
            background_color = self.color
        
        pygame.draw.rect(screen, background_color, (self.left, self.top, self.width, self.height))
        text_rect = self.text_surface.get_rect(
            center=(self.left + (self.width/2), self.top + (self.height/2))
        )
        screen.blit(self.text_surface, text_rect)