import pygame
from layouts.screen import Screen
from layouts.button import Button


LOGO_SIZE_RATIO = 50
LOGO_IMG = pygame.image.load('./chess/assets/Images/chess-logo.png')

# original background image ratio width:height = 1.777
BACKGROUND_IMG = pygame.image.load('./chess/assets/Images/chess-background.jpg')


class MenuScreen(Screen):
    def __init__(self, title, monitor_size):
        super().__init__(title, monitor_size)
        
        self.single_player_button = MenuButton("Single Player", 1.6)
        self.multi_player_button = MenuButton("Multiplayer", 1.2)
    
    
    def update_content(self):
        self.single_player_button.update_position(self.win_size)
        self.multi_player_button.update_position(self.win_size)
        
        self.single_player_button.update_font_size(self.fullscreen)
        self.multi_player_button.update_font_size(self.fullscreen)
    
    
    def draw(self, mouse_pos):
        self.draw_background()
        self.draw_buttons(mouse_pos)
    
    
    def draw_background(self):
        self.screen.fill(self.fill_color)
        
        BACKGROUND_IMG.convert()
        BACKGROUND_IMG.set_alpha(200)
        background = pygame.transform.scale(BACKGROUND_IMG, self.win_size)
        self.screen.blit(background, (0, 0))
        
        width, height = self.win_size
        size = (LOGO_SIZE_RATIO*height) / 100
        LOGO_IMG.convert_alpha()
        logo = pygame.transform.scale(LOGO_IMG, (size, size))
        self.screen.blit(logo, ((width - size) / 2, 0))
    
    
    def draw_buttons(self, mouse_pos):
        self.single_player_button.draw(self.screen, mouse_pos)
        self.multi_player_button.draw(self.screen, mouse_pos)
    
    
    def handle_click(self, mouse_pos):
        '''Returns two booleans regarding in_single_player and in_multi_player respectively'''
        
        if self.single_player_button.is_focused(mouse_pos):
            return True, False
        elif self.multi_player_button.is_focused(mouse_pos):
            return False, True
        else:
            return False, False



class MenuButton(Button):
    
    MENU_BUTTON_WIDTH_RATIO = 35
    MENU_BUTTON_HEIGHT_RATIO = 13

    def __init__(self, text, top_ratio, left_ratio=None,
        w_ratio=MENU_BUTTON_WIDTH_RATIO, h_ratio=MENU_BUTTON_HEIGHT_RATIO
    ):
        super().__init__(left_ratio, top_ratio, w_ratio, h_ratio)
        self.text = text
        
        
    def update_position(self, win_size):
        self.width = (win_size[0] * self.w_ratio) / 100
        self.height = (win_size[1] * self.h_ratio) / 100
        self.left = (win_size[0] - self.width) / 2
        self.top = (win_size[1] - self.height) / self.top_ratio
    
    
    def draw(self, screen, mouse_pos):
        #print("draw buttons")
        if self.is_focused(mouse_pos):
            background_color = self.hover_color
        else:
            background_color = self.color
        
        pygame.draw.rect(screen, background_color, (self.left, self.top, self.width, self.height))
        text_rect = self.text_surface.get_rect(
            center=(self.left + (self.width/2), self.top + (self.height/2))
        )
        screen.blit(self.text_surface, text_rect)