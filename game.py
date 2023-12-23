import pygame
from game_session import Game_Session
from game_session_online import Game_Session_Online
from menu import Game_Menu
from debug import log
import debug
import json
import sys
class Game:
    def __init__(self):
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
        menu_ = Game_Menu(self.screen)
        while True:
            log("Running")
            m = menu_.run()
            if m == 1:
                game = Game_Session(self.screen)
                if game.setup_game_player(self.player_id, self.player_name, "lonely_fui"):
                    game.run(self.screen)
                else:
                    log("error setting up player game data", level=0)
                    sys.exit()
            elif m == 2:
                game = Game_Session_Online(self.screen)
                if game.setup_game_player(self.player_id, self.player_name, "lonely_fui"):
                    game.run(self.screen)
                else:
                    log("error setting up player game data", level=0)
                    sys.exit()
