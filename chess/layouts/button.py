import pygame
from constants import BLACK, GREY, SELECT_COLOR


class Button():
    def __init__(self, left_ratio, top_ratio, w_ratio, h_ratio,
        color=GREY, hover_color=SELECT_COLOR, text_color=BLACK,
        font_name="Roboto", small_font_size=32, big_font_size=48
    ):
        self.left_ratio = left_ratio
        self.top_ratio = top_ratio
        self.w_ratio = w_ratio
        self.h_ratio = h_ratio
        self.color = color
        self.hover_color = hover_color
        
        self.font_name = font_name
        self.small_font_size = small_font_size
        self.big_font_size = big_font_size
        self.text_color = text_color
    
    
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
        
        self.font = pygame.font.SysFont(self.font_name, font_size)
        self.text_surface = self.font.render(self.text, 1, self.text_color)