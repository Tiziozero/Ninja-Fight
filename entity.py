import pygame, os, sys, time, math
from debug import debug, print_debug


class Images:
    def __init__(self, path):
        print("image for path", path)
        self.images = {}
        self.images_dirctory_path_relative_to_main_file = path
        self.images = {}
        self.image_rect = {}
        self.image_dest_offset = 150
        self.image_size = 200 # may vary
        self.image_names = ['Attack1', 'Attack2', 'Death', 'Fall', 'Idle', 'Jump', 'Run', 'Take Hit']
        self.image_indexes = ['Attack1', 'Attack2', 'Death', 'Fall', 'Idle', 'Jump', 'Run', 'Take Hit']
        self.body_rect = pygame.Rect(0, 0, 0, 0)
        self.image_dest_rect = {}
        self.images_lef = {}
        self.images_right = {}
        self.image_index = 'Idle'
        self.image_format = '.png'
        self.blit_rect = pygame.Rect(0, 0, self.image_size, self.image_size)
        self.body_rect = pygame.Rect(0, 0, 50, 50)
        self.rect = pygame.Rect(0,0,0,0)
        self.offset = 150
        self.load_img(path)

    def load_img(self, path):
        for name in self.image_names:
            path_to_image = path + name + self.image_format 

            image_current = pygame.image.load(path_to_image).convert_alpha()

            self.images[name] = [image_current, pygame.transform.flip(image_current, True, False)]
            self.image_rect[name] = self.images[name][0].get_rect()
            self.image_dest_rect[name] = [
                                            [pygame.Rect(self.image_size * i, 0, self.image_size, self.image_size)  for i in range(self.image_rect[name].w // self.image_size)], # right
                                            [pygame.Rect(self.image_rect[name].w - self.image_size - self.image_size * i, 0, self.image_size, self.image_size)  for i in range(self.image_rect[name].w // self.image_size)]  # left
                                            ]


class Entity(pygame.sprite.Sprite):
    def __init__(self, entity_id, image_bank, img_dir_path, groups):
        super().__init__(groups)
        self.id = entity_id
        self.images = {}
        self.mov = None
        self.image = None
        self.offset = 0
        self.x_pos, self.y_pos = 0, 0
        self.load_img(img_dir_path)

    def load_img(self, path):
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        print(f"{str(self.id):_<10} rect w: {str(self.rect.w):_<5}, rect h: {str(self.rect.h):_<5}, rect x: {str(self.rect.x):_<5}, rect y: {str(self.rect.y):_<5}")
        self.dest_rect = pygame.Rect(0, 0, self.rect.w//8, self.rect.h)
    """
    def draw(self, screen):
        screen.blit(
                    self.images[self.image_index][self.direction], # Imgae ( images, which image, what dirrection )
                    self.blit_rect, # Draw rect ( where to draw )
                    self.image_dest_rect[self.image_index][self.direction][int(self.dest_rect_index)] # Which tile ( destination rects, for which image, what direction )
                )
    """
    def update(self, screen, dt):
        # self.draw(screen)
        #self.dest_rect.x += self.dest_rect.w
        self.x_pos += dt
        self.dest_rect.x = self.x_pos
        print(f"dt: {str(dt):_<50}; x position: {str(self.x_pos):_<50}")
        if self.dest_rect.x >= self.rect.w:
            self.dest_rect.x = 0
            self.x_pos

class Player(pygame.sprite.Sprite):
    def __init__(self, entity_id, image_bank, img_dir_path, groups, ground_group):
        super().__init__(groups)
        # Player ID
        self.player_id = entity_id
        self.ground_group = ground_group
        print(len(self.ground_group))

        self.image_bank = image_bank

        # Textures and Rect
        self.images_dirctory_path_relative_to_main_file = img_dir_path
        self.images = {}
        self.image_rect = {}
        self.image_dest_offset = 150
        self.image_size = 200 # may vary
        self.image_names = ['Attack1', 'Attack2', 'Death', 'Fall', 'Idle', 'Jump', 'Run', 'Take Hit']
        self.image_indexes = ['Attack1', 'Attack2', 'Death', 'Fall', 'Idle', 'Jump', 'Run', 'Take Hit']
        self.body_rect = pygame.Rect(0, 0, 0, 0)
        self.image_dest_rect = {}
        self.images_lef = {}
        self.images_right = {}
        self.image_index = 'Idle'
        self.image_format = '.png'
        self.blit_rect = pygame.Rect(0, 0, self.image_size, self.image_size)
        self.body_rect = pygame.Rect(0, 0, 50, 50)
        self.rect = pygame.Rect(0,0,0,0)
        self.offset = 150

        # Animation Stuff
        self.direction = 0
        self.clock = 0
        self.animation_speed = 10
        self.dest_rect_index = 0
        self.jumping = False 
        self.attacking = False
        self.font_size = 20
        self.font = pygame.font.Font('fonts/CaskaydiaCoveNerdFont-Regular.ttf', self.font_size)

        # Test propeties
        self.image = None
        self.x_position, self.y_position = 0, 0
        self.velocity = 300
        self.horizontal_velocity = 0
        self.vertical_velocity = 0
        self.in_air = True
        self.jump_hight = 800

    def setup(self):
        self.load_img(self.images_dirctory_path_relative_to_main_file)

    def load_img(self, path):
        for name in self.image_names:
            path_to_image = path + name + self.image_format 

            image_current = pygame.image.load(path_to_image).convert_alpha()

            self.images[name] = [image_current, pygame.transform.flip(image_current, True, False)]
            self.image_rect[name] = self.images[name][0].get_rect()
            self.image_dest_rect[name] = [
                                            [pygame.Rect(self.image_size * i, 0, self.image_size, self.image_size)  for i in range(self.image_rect[name].w // self.image_size)], # right
                                            [pygame.Rect(self.image_rect[name].w - self.image_size - self.image_size * i, 0, self.image_size, self.image_size)  for i in range(self.image_rect[name].w // self.image_size)]  # left
                                            ]

    def move(self, event):
        if not self.attacking:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    self.horizontal_velocity = 0
                    self.attacking = True
                    self.image_index = 'Attack1'
                if event.key == pygame.K_a:
                    self.horizontal_velocity -= self.velocity
                    self.dest_rect_index = 0
                if event.key == pygame.K_d:
                    self.horizontal_velocity += self.velocity
                    self.dest_rect_index = 0
                if event.key == pygame.K_SPACE:
                    if not self.jumping:
                        self.vertical_velocity = -self.jump_hight
                    self.dest_rect_index = 0
                    self.rect.y -= 1
                    self.jumping = True
                    print("Jump", self.vertical_velocity, self.rect.bottom - 75 )

            if event.type == pygame.KEYUP:
                if not self.attacking:
                    if event.key == pygame.K_a:
                        self.horizontal_velocity += self.velocity
                    if event.key == pygame.K_d:
                        self.horizontal_velocity -= self.velocity

    def updata_pos(self, dt, screen):
        # Updata Position
        self.vertical_velocity += 2500 * dt 

        # not using pygame spritecollide due to it giving problems like not getting collisions each timeits called maybe due to it being slow or any other reason

        for floor in self.ground_group:
            if self.rect.bottom >= floor.rect.top and self.rect.bottom <= floor.rect.bottom:
                if self.rect.right >= floor.rect.left and self.rect.right <= floor.rect.right:
                    if self.vertical_velocity >= 0:
                        self.rect.bottom = floor.rect.top
                        self.vertical_velocity = 0
                        self.jumping = False
            if self.rect.top <= floor.rect.bottom and self.rect.top >= floor.rect.top:
                if self.rect.right >= floor.rect.left and self.rect.right <= floor.rect.right:
                    if self.vertical_velocity <= 0:
                        self.rect.top = floor.rect.bottom
                        self.vertical_velocity = 0



        if not self.attacking:
            self.x_position += self.horizontal_velocity * dt 
            self.y_position += self.vertical_velocity * dt 
        self.body_rect.x = int(math.ceil(self.x_position))
        self.body_rect.y = int(self.y_position)

    def def_animation(self):
        # Update animation
        if not self.attacking:

            if self.jumping:
                self.image_index= 'Jump'
            if self.vertical_velocity > 0:
                self.image_index = 'Fall'
            elif self.vertical_velocity == 0:
                self.image_index = 'Idle'
                if self.horizontal_velocity > 0:
                    self.image_index = 'Run'
                    self.direction = 0
                elif self.horizontal_velocity < 0:
                    self.image_index = 'Run'
                    self.direction = 1
                else:
                    self.image_index = 'Idle'


    def draw(self, screen):
        self.blit_rect = pygame.Rect(self.body_rect.x - 75, self.body_rect.y - 75, self.image_size, self.image_size)
        currentThingy = self.image_dest_rect[self.image_index][self.direction]

        if self.dest_rect_index > len(currentThingy):
            self.dest_rect_index = len(currentThingy)-0.01
        # pygame.draw.rect(screen, (255, 255, 255), self.body_rect)
        screen.blit(
                    self.images[self.image_index][self.direction], # Imgae ( images, which image, what dirrection )
                    self.blit_rect, # Draw rect ( where to draw )
                    self.image_dest_rect[self.image_index][self.direction][int(self.dest_rect_index)] # Which tile ( destination rects, for which image, what direction )
                )

    def update_indexes(self, dt):
        # checks if frame is less than 8 (needs optimisation for all animation lengths)
        self.dest_rect_index += dt * self.animation_speed 
        # print(f"{int(self.dest_rect_index)}, {str(len(self.image_dest_rect)): <5}, {self.image_index}, ")
        if self.dest_rect_index >= len(self.image_dest_rect[self.image_index][self.direction]):
            self.dest_rect_index = 0
            if self.attacking:
                self.attacking = False
                self.vertical_velocity = 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_d]:
                    self.horizontal_velocity += self.velocity
                    print("d is pressed", self.horizontal_velocity, self.velocity)
                
                if keys[pygame.K_a]:
                    self.horizontal_velocity -= self.velocity
                    print("a is pressed", self.horizontal_velocity, self.velocity)
    def update(self, screen, dt):
        self.rect = self.body_rect
        self.clock += dt
        
        self.updata_pos(dt, screen)
        self.update_indexes(dt)
        self.def_animation()
        
        self.draw(screen)
        
        t = (f"{str(self.jumping): <6}, {str(self.vertical_velocity): <20}, {str(self.rect.bottom): <10}")
        debug(t)
