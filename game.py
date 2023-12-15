import pygame
import game_session
import menu
import debug
from debug import log
import json
import sys
class Game:
    def __init__(self):
        # pygame.init()
        self.screen = pygame.display.set_mode((1200, 600))
        debug.screen = self.screen
        self.player_id = 00000000
        self.player_name = ""
        self.setup()

        log("Game created")
        
    def setup(self):
        debug.setup(self.screen, False)
        log("setup...", level=0)
        with open('player_data.json', 'r') as file:
            data = json.load(file)
            self.player_id = int(data["player_id"])
            self.player_name = data["name"]
            log(f"Game player id:   {self.player_id}", level=0)
            log(f"Game player name: {self.player_name}", level=0)


    def run(self):
        log("Running")
        menu_ = menu.Game_Menu(self.screen)
        menu_.run()
        game = game_session.Game_Session(self.screen)
        if game.setup_game_player(self.player_id, self.player_name, "lonely_fui"):
            game.run(self.screen)
        else:
            log("error setting up player game data", level=0)
            sys.exit()
