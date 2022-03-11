import threading
import pygame

from layouts import MenuScreen, SingleplayerSettingsScreen, MultiplayerSettingsScreen
from single_player import run_single_player
from multi_player import run_multi_player

from helpers import display_fps
from constants import FPS


MAX_NAME_LENGHT = 10

ICON_SIZE = 64
ICON_IMG =  pygame.transform.scale(pygame.image.load('./chess/assets/Images/chess-icon.jpg'), (ICON_SIZE, ICON_SIZE))


def run():
    pygame.init()
    pygame.mixer.init()
    pygame.event.set_allowed([
        pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION,
        pygame.KEYDOWN, pygame.QUIT, pygame.VIDEORESIZE
    ])
    pygame.display.set_icon(ICON_IMG)
    
    monitor_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
    menu_screen = MenuScreen("Chess - menu", monitor_size)
    singleplayer_settings_screen = SingleplayerSettingsScreen("Chess - settings", monitor_size)
    multiplayer_settings_screen = MultiplayerSettingsScreen("Chess - settings", monitor_size)
    
    application_state = {
        "running": True,
        "in_single_player": False,
        "in_multi_player": False,
        "fullscreen": False,
    }
    
    
    while application_state["running"]:
        run_main_menu(menu_screen, application_state)
        
        
        if application_state["in_single_player"]:
            game_settings = run_singleplayer_settings_screen(singleplayer_settings_screen, application_state)
            
            if game_settings:
                run_single_player(monitor_size, application_state, game_settings)
                # stuck here until the user quits the game
            
            application_state["in_single_player"] = False
        
        
        if application_state["in_multi_player"]:
            player_name = run_multiplayer_settings_screen(multiplayer_settings_screen, application_state)
            
            if player_name:
                run_multi_player(monitor_size, application_state, player_name)
                # stuck here until the user quits the game
            
            application_state["in_multi_player"] = False
      
    pygame.quit()



def run_main_menu(menu_screen, application_state):
    clock = pygame.time.Clock()
    menu_screen.make_current(application_state["fullscreen"])
    
    while menu_screen.is_current():
        clock.tick(FPS)
        
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                menu_screen.end_current()
                application_state["running"] = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_screen.end_current()
                    application_state["running"] = False
                    return
                
                if event.key == pygame.K_f:
                    application_state["fullscreen"] = not application_state["fullscreen"]
                    menu_screen.toggle_fullscreen()
                
                if event.key == pygame.K_t:
                    for thread in threading.enumerate():
                        print(thread.name)
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                in_single_player, in_multi_player = menu_screen.handle_click(mouse_pos)
                
                if in_single_player:
                    menu_screen.end_current()
                    application_state["in_single_player"] = True
                    return
                    
                elif in_multi_player:
                    menu_screen.end_current()
                    application_state["in_multi_player"] = True
                    return
        
        menu_screen.draw(mouse_pos)
        #display_fps(menu_screen.screen, clock)
        pygame.display.flip()



def run_singleplayer_settings_screen(screen, application_state):
    '''Returns the choosen settings if the user starts the game, None if the user quits'''
    
    clock = pygame.time.Clock()
    screen.make_current(application_state["fullscreen"])
    
    while screen.is_current():
        clock.tick(FPS)
        
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                screen.end_current()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen.end_current()
                    return None
                
                if event.key == pygame.K_f:
                    application_state["fullscreen"] = not application_state["fullscreen"]
                    screen.toggle_fullscreen()
                    
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_settings = screen.handle_click(mouse_pos)
                
                if game_settings:
                    screen.end_current()
                    return game_settings
        
        
        screen.draw(mouse_pos)
        pygame.display.flip()



def run_multiplayer_settings_screen(screen, application_state):
    '''Returns the choosen settings if the user starts the game, None if the user quits'''
    
    clock = pygame.time.Clock()
    screen.make_current(application_state["fullscreen"])
    player_name = ""
    is_typing = False
    
    while screen.is_current():
        clock.tick(FPS)
        
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                screen.end_current()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    screen.end_current()
                    return None
                
                if not is_typing:
                    if event.key == pygame.K_f:
                        application_state["fullscreen"] = not application_state["fullscreen"]
                        screen.toggle_fullscreen()
                        screen.update_content(player_name)
                
                else:
                    if event.key == pygame.K_BACKSPACE:
                        if len(player_name) > 0:
                            player_name = player_name[:-1]
                    else:
                        if len(player_name) < MAX_NAME_LENGHT:
                            player_name += event.unicode
                    
                    screen.update_content(player_name)
                    
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                is_typing, start_game = screen.handle_click(mouse_pos, player_name)
                
                if start_game:
                    screen.end_current()
                    return player_name
        
        
        screen.draw(mouse_pos, player_name)
        pygame.display.flip()



if __name__ == '__main__':
    run()