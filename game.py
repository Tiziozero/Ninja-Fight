import pygame
import game_session
import debug
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))
        debug.screen = self.screen
        print("Game created")

    def run(self):
        print("Running")
        game = game_session.Game_Session(self.screen)
        game.run(self.screen)
