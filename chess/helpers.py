import pygame
import threading
import time


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