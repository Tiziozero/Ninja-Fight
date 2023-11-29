import pygame
import game_session
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        print("Game created")

    def run(self):
        print("Running")
        game = game_session.Game_Session(self.screen)
        game.run(self.screen)
