import pygame
from entity import Image_Bank
from player import Player
from enemy_1 import Enemy_1
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
        self.image_bank = Image_Bank("graphics/sprites/")
        self.draw_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.ground_group = pygame.sprite.Group()
        ground_rect = pygame.Rect(0, 530, 1200, 70)
        self.floor = Floor(ground_rect, screen, self.ground_group)
        self.ground_group.add(self.floor)
        self.bg_index = 2
        self.bg = pygame.image.load("graphics/bg.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1200, (600 * 3)))
        self.bg_rect = pygame.Rect(0, 0, 1200, 600)
        self.bg_rect = self.bg.get_rect()
        self.dest_rect = pygame.Rect(0, (self.bg_rect.h // 3) * self.bg_index, self.bg_rect.w, self.bg_rect.h // 3)
    def draw(self, dt):
        pass
    def run(self, screen):
        test_en = Player('00000001',self.image_bank, "graphics/sprites/", self.draw_sprites, self.ground_group)
        test_en.setup()
        test_enemy_1 = Enemy_1('00000002', self.image_bank, self.draw_sprites, self.ground_group)
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


            #screen.fill((0,0,0))
            pygame.draw.rect(screen, (0, 0, 255), self.bg_rect)
            screen.blit(self.bg, self.bg_rect, self.dest_rect)
            test_en.update(screen, dt)
            test_en.draw(screen, dt)
            test_enemy_1.update(screen, dt)
            test_enemy_1.draw(screen, dt)
            print_debug()

            pygame.display.flip()
