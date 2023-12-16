import pygame, time, json
from entity import  Image_Bank, Sound_Bank
from player import Player
from enemy_1 import Enemy_1
from debug import *


class Floor(pygame.sprite.Sprite):
    def __init__(self, rect, screen, group, image = None):
        super().__init__()
        # Floor Image, rect and screen to draw to
        
        self.image = pygame.Surface((rect.w, rect.h))
        if image != None:
            self.image = image
        # self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = rect.x
        self.rect.y = rect.y
        self.screen = screen
        

class Game_Session:
    def __init__(self, screen):
        # Game variables
        self.guit_game = False
        self.screen = screen
        # self.rect = (100,100,400,200)

        # Banks
        self.image_bank = Image_Bank("graphics/sprites/")
        self.sound_bank = Sound_Bank("sounds/sword/")

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.draw_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.ground_group = pygame.sprite.Group()
        self.entity_group = pygame.sprite.Group()
        self.bullets_group = pygame.sprite.Group()
        self.groups = {"draw": self.draw_sprites, "player": self.player_group, "ground": self.ground_group, "entity": self.entity_group, "all": self.all_sprites, "bullets": self.bullets_group}
        # Background  and terrain
        self.bg = pygame.image.load("graphics/bg_1.jpg")
        self.bg = pygame.transform.scale(self.bg, (1200, 600))
        self.bg_rect = self.bg.get_rect()
        self.camera_offset = [0, 0]

        # Game ground
        ground_rect = pygame.Rect(-1200, 580, 3600, 20)
        self.floor = Floor(ground_rect, screen, self.ground_group)
        self.ground_group.add(self.floor)
        self.draw_sprites.add(self.floor)
        self.bg_music = pygame.mixer.music.load("sounds/music/Like that, Sleep token.mp3")

    def setup_game_player(self, player_id, player_name, character):
        self.player_id = player_id
        self.player_name = player_name
        self.player_character = character
        return True

    def setup_terrain(self, terrain):
        print("setup...")
        with open('terrain_1.json', 'r') as file:
            data = json.load(file)
            log(str(f"data: {data}, length terrain: {len(data)}"))# def __init__(self, rect, screen, group, image = None):
            terrain_1_surf = pygame.image.load("graphics/terrain/terrain_300x10.png").convert_alpha()
            for key, val in data.items():
                rect_ = pygame.Rect(val[0], val[1], 0, 0)
                floor = Floor(rect_, self.screen, self.ground_group, image=terrain_1_surf)
                self.ground_group.add(floor)
                self.ground_group.add(floor)
                self.all_sprites.add(floor)
                self.draw_sprites.add(floor)
    
    def draw(self, dt):
        pass
    def run(self, screen):
        pygame.mixer.music.play()
        self.setup_terrain(0)
        # Game player
        test_en = Player(self.player_id, self.player_name, self.player_character, self.image_bank, self.groups, player=0)
        test_en.setup()
        # Test entity enemy
        test_enemy_1 = Enemy_1('32001207', "george",  self.image_bank, self.groups)
        self.entity_group.add(test_en)
        # self.entity_group.add(test_enemy_1)
        self.all_sprites.add(test_en)
        # self.all_sprites.add(test_enemy_1)
        self.draw_sprites.add(test_en)
        # self.draw_sprites.add(test_enemy_1)
        self.player_group.add(test_en)
        test_en = Player(str(int(self.player_id) + 1), self.player_name, self.player_character, self.image_bank, self.groups, player=1)
        test_en.setup()
        # Test entity enemy
        test_enemy_1 = Enemy_1('32001207', "george",  self.image_bank, self.groups)
        self.entity_group.add(test_en)
        # self.entity_group.add(test_enemy_1)
        self.all_sprites.add(test_en)
        # self.all_sprites.add(test_enemy_1)
        self.draw_sprites.add(test_en)
        # self.draw_sprites.add(test_enemy_1)
        self.player_group.add(test_en)

        # Setup game variables
        p_time = time.time()
        while not self.guit_game:
            # Update dt
            dt = time.time() - p_time
            p_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.guit_game = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        self.guit_game = True
                # Entity events
                for entity in self.entity_group:
                    entity.move(event)


            # Update and draw background
            pygame.draw.rect(screen, (0, 0, 255), self.bg_rect)
            # screen.blit(self.bg, self.bg_rect, self.dest_rect)
            screen.blit(self.bg, self.bg_rect)
            
            self.all_sprites.update(screen, dt)
            self.draw_sprites.draw(self.screen)

            # Display to screen debug info
            print_debug()

            # Update screen
            pygame.display.flip()
