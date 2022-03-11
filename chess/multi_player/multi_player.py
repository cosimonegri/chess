import pygame
import threading
from time import sleep

from board import Board
from layouts import LoadingScreen, GameScreen, PromotionPopup, GameEndPopup

from multi_player.client import ConnectionThread
from helpers import display_fps
from constants import FPS


def run_multi_player(monitor_size, application_state, player_name):
    print("[GAME] multiplayer game started")
    move_sound = pygame.mixer.Sound("./chess/assets/Sounds/move.wav")
    
    game_state = {
        "mode": "multi player",
        "my_name": player_name,
        "my_color": None,
        "enemy_name": None,
        "enemy_color": None,
        "should_draw_board": True
    }
    
    connection_state = {
        "client": None,
        "client_thread": None,
        "failed_connection": False,
        "new_fen_board": None
    }
    
    clock = pygame.time.Clock()
    board = Board()
    board.update_pseudo_legal_moves()  # at the beginning check impossible
    
    connection_thread = ConnectionThread(connection_state, game_state, board)
    connection_thread.start()
    print("start connection thread")
    
    loading_screen = LoadingScreen("Chess - loading", monitor_size)
    game_screen = GameScreen("Chess - multiplayer", monitor_size, board, game_state)
    promotion_popup = PromotionPopup()
    game_end_popup = GameEndPopup()
    
    loading_screen.make_current(application_state["fullscreen"])
    
    
    # LOADING SCREEN AND SETUP
    while loading_screen.is_current():
        clock.tick(FPS)
        
        if connection_state["failed_connection"]:
            loading_screen.end_current()
            return
        elif game_state["enemy_name"] != None:  # an opponent has been found
            loading_screen.end_current()
            game_screen.make_current(application_state["fullscreen"])
        
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                loading_screen.end_current()
                connection_thread.raise_exception()
                print("kill connection thread")
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loading_screen.end_current()
                    connection_thread.raise_exception()
                    print("kill connection thread")
                    return
                
                if event.key == pygame.K_f:
                    application_state["fullscreen"] = not application_state["fullscreen"]
                    loading_screen.toggle_fullscreen()
                
                if event.key == pygame.K_t:
                    for thread in threading.enumerate():
                        print(thread.name)
           
        loading_screen.draw()
        pygame.display.flip()
    
    
    
    # ACTUAL GAME
    while game_screen.is_current():
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        
        # UPDATE THE BOARD WHEN THE OPPENENT HAS MOVED
        if connection_state["new_fen_board"]:
            board.set_fen(connection_state["new_fen_board"])
            move_sound.play()
            
            # check if i have has lost
            board.update_legal_moves(board.turn)
            board.check_if_loser(board.turn)
            
            game_screen.update_content()
            game_state["should_draw_board"] = True
            
            connection_state["new_fen_board"] = None
        
        
        # SHOW AND HIDE POPUPS
        if board.turn == game_state["my_color"] and board.promotion_square != None:
            if not promotion_popup.is_active():
                promotion_popup.update(game_screen.screen, game_state["my_color"])
                promotion_popup.show()
        else:
            promotion_popup.hide()
        
        if board.is_checkmate() or board.is_stalemate() and not game_end_popup.is_active():
            game_end_popup.update(
                game_screen.screen, application_state["fullscreen"], game_state["my_color"], board.winner
            )
            game_end_popup.show()
        
        
        # GET EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_screen.end_current()
                connection_state["client_thread"].raise_exception()
                print("kill client thread")
                connection_state["client"].send("quit")
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_screen.end_current()
                    connection_state["client_thread"].raise_exception()
                    print("kill client thread")
                    connection_state["client"].send("quit")
                    return
                
                # TOGGLE FULLSCREEN ON AND OFF
                if event.key == pygame.K_f:
                    application_state["fullscreen"] = not application_state["fullscreen"]
                    game_state["should_draw_board"] = True
                    game_screen.toggle_fullscreen()
                    
                    if game_end_popup.is_active():
                        game_end_popup.update(
                            game_screen.screen, application_state["fullscreen"], game_state["my_color"], board.winner
                        )
                        
                    if promotion_popup.is_active():
                        promotion_popup.update(game_screen.screen, game_state["my_color"])
                
                if event.key == pygame.K_t:
                    for thread in threading.enumerate():
                        print(thread.name)


            # PLAYER TURN
            if event.type == pygame.MOUSEBUTTONDOWN:    
                if promotion_popup.is_active():
                    handle_promotion_button_down(board, promotion_popup, game_state, connection_state["client"])
                        
                elif game_end_popup.is_active():
                    back_to_menu = game_end_popup.handle_click(mouse_pos)
                    if back_to_menu:
                        game_screen.end_current()
                        connection_state["client_thread"].raise_exception()
                        print("kill client thread")
                        connection_state["client"].send("quit")
                        return
                    
                else:
                    if board.turn == game_state["my_color"]:
                        handle_game_click_down(board, game_screen, game_state)
            
            
            # PLAYER TURN
            if event.type == pygame.MOUSEBUTTONUP:
                if not promotion_popup.is_active() and not game_end_popup.is_active():
                    handle_game_click_up(board, game_screen, connection_state["client"], move_sound)
                    
                    game_screen.update_content()
                    game_state["should_draw_board"] = True
        
        
        # DRAW SCREEN AND POPUPS
        if game_state["should_draw_board"] or board.selected_piece != None:
            game_screen.draw(board)
            game_state["should_draw_board"] = False
        if promotion_popup.is_active():
            promotion_popup.draw(game_screen.screen, mouse_pos)
        if game_end_popup.is_active():
            game_end_popup.draw(game_screen.screen, mouse_pos)
        
        
        #display_fps(game_screen.screen, clock)
        game_screen.handle_mouse_icon(mouse_pos, board)
        pygame.display.flip()



def handle_game_click_down(board, game_screen, game_state):
    mouse_pos = pygame.mouse.get_pos()
    row, col = game_screen.get_board_row_col(mouse_pos)

    if row >= 0 and col >= 0 and row <= 7 and col <= 7:
        selected_piece = board.at_square(row, col)
        
        if selected_piece and selected_piece.color == game_state["my_color"]:
            board.selected_piece = selected_piece


def handle_game_click_up(board, game_screen, client, move_sound):
    selected_piece = board.selected_piece
    mouse_pos = pygame.mouse.get_pos()
    
    if selected_piece != None:
        start_row = selected_piece.row
        start_col = selected_piece.col
        end_row, end_col = game_screen.get_board_row_col(mouse_pos)
        
        if board.is_move_inbound(start_row, start_col, end_row, end_col):
            if board.is_legal_move(start_row, start_col, end_row, end_col):
                board.execute_move(start_row, start_col, end_row, end_col)
                move_sound.play()
                board.selected_piece = None
                
                if board.promotion_square == None:
                    board.change_turn()
                    
                    # check if the enemy has lost
                    board.update_legal_moves(board.turn)
                    board.check_if_loser(board.turn)
                    
                    # sending new board to the server
                    response = client.send(board.to_fen())
                    if response != "received":
                        print("Trying again to send the new board to the server")
                        response = client.send(board.to_fen())
        
    board.selected_piece = None


def handle_promotion_button_down(board, promotion_popup, game_state, client):
    mouse_pos = pygame.mouse.get_pos()
    new_piece = promotion_popup.handle_click(mouse_pos)
    if new_piece != None:
        board.promote(new_piece, game_state["my_color"])
        board.change_turn()
        
        # check if the bot has lost
        board.update_legal_moves(board.turn)
        board.check_if_loser(board.turn)
        
        # sending new board to the server
        response = client.send(board.to_fen())
        if response != "received":
            print("Trying again to send the new board to the server")
            response = client.send(board.to_fen())