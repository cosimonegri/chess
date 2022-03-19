import pygame
from constants import WIN_WIDTH, WIN_HEIGHT, WHITE, BACKGROUND_FADE


class Screen():
    def __init__(self, title, monitor_size, min_width=WIN_WIDTH, min_height=WIN_HEIGHT, fill_color=WHITE):
        self.title = title
        self.monitor_size = monitor_size
        self.min_width = min_width
        self.min_height = min_height
        self.fill_color = fill_color

        self.current = False
        self.fullscreen = False
        self.win_size = None

        self.big_background = None
        self.small_background = None
    
    
    def update_size(self):
        '''Update the size of the screen'''
        
        if self.fullscreen:
            self.screen = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
            self.win_size = self.monitor_size
        else:
            self.screen = pygame.display.set_mode((self.min_width, self.min_height))
            self.win_size = (self.min_width, self.min_height)
        

    
    
    def make_current(self, fullscreen):
        pygame.display.set_caption(self.title)
        self.current = True
        self.fullscreen = fullscreen
        self.update_size()
        self.init_background()
        self.update_content()  # update the positions and the dimensions of the content
    
    
    def end_current(self):
        self.current = False
        
        
    def is_current(self):
        return self.current
    
    
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self.update_size()
        self.update_content()  # update the positions and the dimensions of the content
    

    def init_background(self):
        try:
            background = pygame.image.load('./assets/Images/chess-background.jpg')
        except:
            background = pygame.image.load('./chess/assets/Images/chess-background.jpg')
        
        background.set_alpha(BACKGROUND_FADE)
        background.convert()
        self.big_background = pygame.transform.scale(background, self.monitor_size)
        self.small_background = pygame.transform.scale(background, (self.min_width, self.min_height))