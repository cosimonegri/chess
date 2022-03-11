import pygame
from layouts.screen import Screen
from constants import BLACK


class LoadingScreen(Screen):
    def __init__(self, title, monitor_size, text="Waiting for an opponent...",
        font_name="Roboto", big_font_size=50, small_font_size=34, text_color=BLACK
    ):
        super().__init__(title, monitor_size)
        
        self.text = text
        self.font_name = font_name
        self.big_font_size = big_font_size
        self.small_font_size = small_font_size
        self.text_color = text_color
    
    
    def update_content(self):
        win_width, win_height = self.get_size()
        
        if self.fullscreen:
            self.font = pygame.font.SysFont(self.font_name, self.big_font_size)
        else:
            self.font = pygame.font.SysFont(self.font_name, self.small_font_size)
        
        self.text_surface = self.font.render(self.text, 1, self.text_color)
        self.text_rect = self.text_surface.get_rect(
            center=(win_width / 2, win_height / 2)
        )
    
    
    def draw(self):
        self.screen.fill(self.fill_color)
        self.screen.blit(self.text_surface, self.text_rect)