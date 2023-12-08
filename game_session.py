import pygame
from entity import  Image_Bank
from player import Player
from enemy_1 import Enemy_1
import time
from debug import *

class Floor(pygame.sprite.Sprite):
    def __init__(self, rect, screen, group):
        super().__init__()
        # Floor Image, rect and screen to draw to
        self.image = pygame.Surface((rect.w, rect.h))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y
        self.screen = screen
        
    def draw(self):
        pygame.draw.rect(self.screen, (255,0,0), self.rect)

class Game_Session:
    def __init__(self, screen):
        # Game variables
        self.QuitGame = False
        self.screen = screen
        # self.rect = (100,100,400,200)

        # Image Banks
        self.image_bank = Image_Bank("graphics/sprites/")

        # Groups
        self.draw_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.ground_group = pygame.sprite.Group()
        self.entity_group = pygame.sprite.Group()
        self.groups = {"draw": self.draw_sprites, "player": self.player_group, "ground": self.ground_group, "entity": self.entity_group}

        # Game ground
        ground_rect = pygame.Rect(0, 530, 1200, 70)
        self.floor = Floor(ground_rect, screen, self.ground_group)
        self.ground_group.add(self.floor)

        # Background 
        self.bg_index = 2
        self.bg = pygame.image.load("graphics/bg.png").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1200, (600 * 3)))
        self.bg_rect = pygame.Rect(0, 0, 1200, 600)
        self.bg_rect = self.bg.get_rect()
        self.dest_rect = pygame.Rect(0, (self.bg_rect.h // 3) * self.bg_index, self.bg_rect.w, self.bg_rect.h // 3)


    def draw(self, dt):
        pass
    def run(self, screen):
        # Game player
        test_en = Player('00000001',self.image_bank, self.groups)
        test_en.setup()
        # Test entity enemy
        test_enemy_1 = Enemy_1('00000002', self.image_bank, self.groups)
        self.entity_group.add(test_en)
        self.entity_group.add(test_enemy_1)

        # Setup game variables
        p_time = time.time()
        while not self.QuitGame:
            # Update dt
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
                # Entity events
                test_en.move(event)


            # Update and draw background
            pygame.draw.rect(screen, (0, 0, 255), self.bg_rect)
            screen.blit(self.bg, self.bg_rect, self.dest_rect)

            # Update sprites
            # test_en.update(screen, dt)
            # test_enemy_1.update(screen, dt)

            # Draw sprites
            # test_en.draw(screen, dt)
            # test_enemy_1.draw(screen, dt)
            self.entity_group.update(self.screen, dt)
            self.entity_group.draw(self.screen)
            # Display to screen debug info
            print_debug()

            # Update screen
            pygame.display.flip()
