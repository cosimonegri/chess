import pygame
import threading

from board import Board
from layouts import GameScreen, PromotionPopup, GameEndPopup

from single_player.bot import find_move
from constants import FPS, DRAWS_AFTER_MINIMIZE



def run_single_player(monitor_size, application_state, game_settings):
    print("[GAME] single player game started")

    try:
        move_sound = pygame.mixer.Sound("./assets/Sounds/move.wav")
    except:
        move_sound = pygame.mixer.Sound("./chess/assets/Sounds/move.wav")
    
    player_color = game_settings[0]
    bot_level = game_settings[1]
    
    game_state = {
        "my_name": "You",
        "my_color": player_color,
        "enemy_name": "Bot lvl " + str(bot_level),
        "enemy_color": ("black" if player_color == "white" else "white"),
        "bot_lvl": bot_level,
        "bot_is_choosing": False,
        "is_end_game_phase": False,
        "remaining_draws": 1,
        "has_shown_end_popup": False,
    }
    
    clock = pygame.time.Clock()
    board = Board()
    board.update_legal_moves()  # not pseudo even if at the beginning check is impossible, just to be sure
    
    game_screen = GameScreen("Chess - single player", monitor_size, board, game_state)
    promotion_popup = PromotionPopup()
    game_end_popup = GameEndPopup()
    game_screen.make_current(application_state["fullscreen"])
    
    
    while game_screen.is_current():
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        
        # SHOW AND HIDE POPUPS
        if board.turn == game_state["my_color"] and board.promotion_square != None:
            if not promotion_popup.is_active():
                promotion_popup.update(game_screen.win_size, game_state["my_color"])
                promotion_popup.show()
        else:
            promotion_popup.hide()
        
        if (board.is_checkmate() or board.is_stalemate()) and not game_state["has_shown_end_popup"]:
            game_state["has_shown_end_popup"] = True
            game_end_popup.update(
                game_screen.win_size, application_state["fullscreen"], game_state["my_color"], board.winner
            )
            game_end_popup.show()
        
        
        # BOT TURN
        if board.turn == game_state["enemy_color"] and not board.is_checkmate() and not board.is_stalemate():
            if not game_state["bot_is_choosing"]:
                game_state["is_end_game_phase"] = board.is_end_game_phase()
                fen_board = board.to_fen()
                bot_move = []
                bot_thread = threading.Thread(
                    target=find_move, args=(
                        fen_board, board.turn, game_state["bot_lvl"], game_state["is_end_game_phase"], bot_move
                    )
                )
                bot_thread.start()
                game_state["bot_is_choosing"] = True
            
            if bot_move != []:
                bot_thread.join()
                if bot_move[0] != None:
                    bot_move = bot_move[0].uci()  # using external chess library
                    board.do_bot_move(bot_move)
                    move_sound.play()
                else:
                    print("Problems with the bot move choice")
                
                game_state["bot_is_choosing"] = False
                board.change_turn()
                
                # check if the player has lost
                board.update_legal_moves(board.turn)
                board.check_if_loser(board.turn)
                
                game_screen.update_content()
                game_state["remaining_draws"] += 1
        
        
        # GET EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_screen.end_current()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_screen.end_current()
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
                    handle_promotion_button_down(board, promotion_popup, game_state)
                        
                elif game_end_popup.is_active():
                    see_game = game_end_popup.handle_click(mouse_pos)
                    if see_game:
                        game_end_popup.hide()
                    
                else:
                    if board.turn == game_state["my_color"]:
                        handle_game_click_down(board, game_screen, game_state)
            
            
            # PLAYER TURN
            if event.type == pygame.MOUSEBUTTONUP:
                if not promotion_popup.is_active() and not game_end_popup.is_active():
                    handle_game_click_up(board, game_screen, move_sound)
                
                    game_screen.update_content()  # to update things in the sidebar
                    game_state["remaining_draws"] += 1
        
        
        # DRAW SCREEN AND POPUPS
        if game_state["remaining_draws"] or board.selected_piece != None:
            game_screen.draw()
            if game_state["remaining_draws"] > 0:
                game_state["remaining_draws"] -= 1
        
        if promotion_popup.is_active():
            promotion_popup.draw(game_screen.screen, game_screen.win_size, mouse_pos)
        if game_end_popup.is_active():
            game_end_popup.draw(game_screen.screen, mouse_pos)
        
        
        game_screen.handle_mouse_icon(mouse_pos, board)
        pygame.display.flip()



def handle_game_click_down(board, game_screen, game_state):
    mouse_pos = pygame.mouse.get_pos()
    row, col = game_screen.get_board_row_col(mouse_pos)

    if row >= 0 and col >= 0 and row <= 7 and col <= 7:
        selected_piece = board.at_square(row, col)
        
        if selected_piece and selected_piece.color == game_state["my_color"]:
            board.selected_piece = selected_piece


def handle_game_click_up(board, game_screen, move_sound):
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
                    
                    # check if the bot has lost
                    board.update_legal_moves(board.turn)
                    board.check_if_loser(board.turn)
        
    board.selected_piece = None


def handle_promotion_button_down(board, promotion_popup, game_state):
    mouse_pos = pygame.mouse.get_pos()
    new_piece = promotion_popup.handle_click(mouse_pos)
    if new_piece != None:
        board.promote(new_piece, game_state["my_color"])
        board.change_turn()
        # check if the bot has lost
        board.update_legal_moves(board.turn)
        board.check_if_loser(board.turn)