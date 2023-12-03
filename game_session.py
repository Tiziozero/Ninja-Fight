import pygame
import entity
import time
from debug import *

class Floor(pygame.sprite.Sprite):
    def __init__(self, rect, screen, group):
        super().__init__()
        self.image = pygame.Surface((rect.w, rect.h))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y
        self.screen = screen
        
    def draw(self):
        pygame.draw.rect(self.screen, (255,0,0), self.rect)
        # print("drawing floor 1")

class Game_Session:
    def __init__(self, screen):
        self.QuitGame = False
        self.screen = screen
        self.rect = (100,100,400,200)
        self.image_bank = entity.Image_Bank("graphics/sprites/")
        self.draw_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.ground_group = pygame.sprite.Group()
        ground_rect = pygame.Rect(0, 390, 800, 10)
        ground_rect1 = pygame.Rect(350, 300, 3000, 10)
        self.floor = Floor(ground_rect, screen, self.ground_group)
        self.floor1 = Floor(ground_rect1, screen, self.ground_group)
        self.ground_group.add(self.floor)
        self.ground_group.add(self.floor1)

    def draw(self, dt):
        pass
    def run(self, screen):
        test_en = entity.Player('00000001',self.image_bank, "graphics/sprites/", self.draw_sprites, self.ground_group)
        test_en.setup()
        p_time = time.time()
        while not self.QuitGame:
            dt = time.time() - p_time
            p_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                test_en.move(event)


            screen.fill((0,0,0))
            # self.floor.draw()
            test_en.update(screen, dt)
            self.ground_group.draw(self.screen)
            test_en.draw(screen, dt)
            # self.player_group.draw(screen)
            print_debug()

            pygame.display.flip()
