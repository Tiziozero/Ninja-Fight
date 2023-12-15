from debug import debug, log
from game_session import Game_Session
import pygame, sys, json


class Game_Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("fonts/DangerNight.otf", 50)
        self.buttons = pygame.sprite.Group()
        self.setup()
    def setup(self):
        self.font = pygame.font.Font("fonts/DangerNight.otf", 50)
        with open('buttons_menu.json', 'r') as buttons:
            buttons = json.load(buttons)
            print(buttons)
            for info in buttons:
                text = self.font.render(info["name"], True, (20, 120, 108))
                rect = text.get_rect(center=(int(info["x"]), int(info["y"])))
                print("done")
                button = Button(rect, text, 1)
                self.buttons.add(button)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill((0,0,0))
            self.buttons.draw(self.screen)
            pygame.display.flip()


class Button(pygame.sprite.Sprite):
    def __init__(self, rect, surf, function):
        super().__init__()
        self.rect = rect
        self.image = surf
        self.button_function_return = function
    
        
