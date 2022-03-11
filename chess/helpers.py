import pygame
import threading
import time


def stringify_move(player, start_row, start_col, end_row, end_col, promotion_piece):
    return (str(player) + str(start_row) + str(start_col) + str(end_row) + str(end_col) + promotion_piece)


def parse_move(string):
    data = {
        "player": int(string[0]),   # number of the player who did the move (1 or 2)
        "start_row": int(string[1]),  # starting row of the moved piece
        "start_col": int(string[2]),  # starting col of the moved piece
        "end_row": int(string[3]),   # target row of the moved piece
        "end_col": int(string[4]),   # target col of the moved piece
        "promotion_piece": string[5]   # ('q', 'r', 'b', 'k', 'x': none)
        # castle ('r', 'l', 'x': none)
        # extra row (row of an eaten piece for example en passant) (-1: none)
        # extra col (col of an eaten piece for example en passant) (-1: none)
    }
    return data


def display_fps(screen, clock):
    font = pygame.font.SysFont("Arial", 32)
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("black"))
    screen.blit(fps_text, (10, 10))



class Timer(threading.Thread):
    def __init__(self, interval):
        threading.Thread.__init__(self)     
        self.interval = interval  # seconds between calls
        self.runable = True

    def run(self, timer, player):
        while self.runable:
            time.sleep(self.interval)
            if self.runable:     
                timer[player] = timer[player] - 1

    def stop(self):
        self.runable = False