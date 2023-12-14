import pygame
import game_session
import debug
import json
import sys
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))
        debug.screen = self.screen
        self.player_id = 00000000
        self.player_name = ""
        self.setup()

        print("Game created")
        
    def setup(self):
        debug.setup(self.screen, False)
        print("setup...")
        with open('player_data.json', 'r') as file:
            data = json.load(file)
            self.player_id = int(data["player_id"])
            self.player_name = data["name"]
            print(self.player_id)
            print(self.player_name)


    def run(self):
        print("Running")
        game = game_session.Game_Session(self.screen)
        if game.setup_game_player(self.player_id, self.player_name, "lonely_fui"):
            game.run(self.screen)
        else:
            print("error setting up player game data")
            sys.exit()
