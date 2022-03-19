import pygame
import threading
import time

from board import Board
from layouts import LoadingScreen, GameScreen, PromotionPopup, GameEndPopup

from multi_player.client import ConnectionThread
from helpers import display_fps
from constants import FPS, DRAWS_AFTER_MINIMIZE, LOADING_POINTS_NUM


def run_multi_player(monitor_size, application_state, player_name):
    print("[GAME] multiplayer game started")

    try:
        move_sound = pygame.mixer.Sound("./assets/Sounds/move.wav")
    except:
        move_sound = pygame.mixer.Sound("./chess/assets/Sounds/move.wav")
    
    game_state = {
        "mode": "multi player",
        "my_name": player_name,
        "my_color": None,
        "enemy_name": None,
        "enemy_color": None,
        "remaining_draws": 1
    }
    
    connection_state = {
        "client": None,
        "client_thread": None,
        "failed_connection": False,
        "new_data": None,
        "disconnecting": False,
        "opponent_disconnected": False
    }
    
    clock = pygame.time.Clock()
    board = Board()
    board.update_legal_moves()  # not pseudo even if at the beginning check is impossible, just to be sure
    
    connection_thread = ConnectionThread(connection_state, game_state, board)
    connection_thread.start()
    print("start connection thread")
    
    loading_screen = LoadingScreen("Chess - loading", monitor_size)
    game_screen = GameScreen("Chess - multiplayer", monitor_size, board, game_state)
    promotion_popup = PromotionPopup()
    game_end_popup = GameEndPopup()
    loading_screen.make_current(application_state["fullscreen"])

    points_num = None  ## number of dots in the loading screen animation
    

    # LOADING SCREEN AND SETUP
    while loading_screen.is_current():
        clock.tick(FPS)

        seconds = time.time()
        old_points_num = points_num
        points_num = int(seconds % 1 // (1.0 / (LOADING_POINTS_NUM + 1)))
        if points_num != old_points_num:
            loading_screen.set_points(points_num)
            loading_screen.update_content()
        

        if connection_state["failed_connection"]:
            print("Connection failed")
            loading_screen.end_current()
            return
        elif game_state["enemy_name"] != None:  # an opponent has been found
            loading_screen.end_current()
            game_screen.make_current(application_state["fullscreen"])
        
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                connection_state["failed_connection"] = True
                loading_screen.end_current()
                connection_thread.raise_exception()
                print("kill connection thread")
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    connection_state["failed_connection"] = True
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
        if connection_state["new_data"]:
            new_fen_board, new_eaten_pieces = connection_state["new_data"]

            board.set_fen(new_fen_board)  # this also updates the turn
            board.eaten_pieces = new_eaten_pieces
            move_sound.play()
            
            # check if i have has lost
            board.update_legal_moves(board.turn)
            board.check_if_loser(board.turn)
            
            game_screen.update_content()
            game_state["remaining_draws"] += 1
            
            connection_state["new_data"] = None
        

        # YOU WIN IF THE OPPONENT LEAVES
        if connection_state["opponent_disconnected"]:
            board.winner = game_state["my_color"]
            game_screen.update_content()
            game_state["remaining_draws"] += 1
        
        
        # SHOW AND HIDE POPUPS
        if board.turn == game_state["my_color"] and board.promotion_square != None:
            if not promotion_popup.is_active():
                promotion_popup.update(game_screen.win_size, game_state["my_color"])
                promotion_popup.show()
        else:
            promotion_popup.hide()
        
        if board.is_checkmate() or board.is_stalemate() or connection_state["opponent_disconnected"]:
            if not game_end_popup.is_active():
                game_end_popup.update(
                    game_screen.win_size, application_state["fullscreen"], game_state["my_color"], board.winner
                )
                game_end_popup.show()
        
        
        # GET EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_screen.end_current()
                connection_state["disconnecting"] = True
                print("kill client thread")
                connection_state["client"].send("quit")
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_screen.end_current()
                    connection_state["disconnecting"] = True
                    print("kill client thread")
                    connection_state["client"].send("quit")
                    return
                
                # TOGGLE FULLSCREEN ON AND OFF
                if event.key == pygame.K_f:
                    application_state["fullscreen"] = not application_state["fullscreen"]
                    if application_state["fullscreen"]:
                        game_state["remaining_draws"] += 1
                    else:
                        game_state["remaining_draws"] += DRAWS_AFTER_MINIMIZE
                    game_screen.toggle_fullscreen()
                    
                    if game_end_popup.is_active():
                        game_end_popup.update(
                            game_screen.win_size, application_state["fullscreen"], game_state["my_color"], board.winner
                        )
                        
                    if promotion_popup.is_active():
                        promotion_popup.update(game_screen.win_size, game_state["my_color"])
                
                # SEE ACTIVE THREADS
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
                        connection_state["disconnecting"] = True
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
                    game_state["remaining_draws"] += 1
        
        
        # DRAW SCREEN AND POPUPS
        if game_state["remaining_draws"] or board.selected_piece != None:
            game_screen.draw(board)
            if game_state["remaining_draws"] > 0:
                game_state["remaining_draws"] -= 1
        if promotion_popup.is_active():
            promotion_popup.draw(game_screen.screen, game_screen.win_size, mouse_pos)
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
                    
                    # sending data to the server
                    response = client.send((board.to_fen(), board.eaten_pieces))
                    while response != "received":
                        print("Trying again to send the new board to the server")
                        response = client.send((board.to_fen(), board.eaten_pieces))
        
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
        
        # sending data to the server
        response = client.send((board.to_fen(), board.eaten_pieces))
        while response != "received":
            print("Trying again to send the new board to the server")
            response = client.send((board.to_fen(), board.eaten_pieces))