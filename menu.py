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
            log(f"loading buttons: {buttons}", level=1)
            for info in buttons:
                text = self.font.render(info["name"], True, (20, 120, 108))
                rect = text.get_rect(center=(int(info["x"]), int(info["y"])))
                log(f"done loading button {info['name']}, button return value: {info['return']}", level=2)
                button = Button(rect, text, int(info["return"]))
                self.buttons.add(button)

    def get_button(self, pos):
        x, y = pos[0], pos[1]
        for button in self.buttons:
            if x > button.rect.left and x < button.rect.right:
                if y > button.rect.top and y < button .rect.bottom:
                    return button.function

        return 0


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        ret_val = int(self.get_button(pygame.mouse.get_pos()))
                        if ret_val == 1:
                            log("game selected", level=2)
                            return 1
                        elif ret_val == 2:
                            log("quit selected", level=2)
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
        self.function = function
