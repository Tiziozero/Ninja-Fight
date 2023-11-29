import pygame, os, sys
from pygame.sprite import Sprite


class Entity(pygame.sprite.Sprite):
    def __init__(self, entity_id, img_dir_path, groups):
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

    def draw(self, screen):
        self.offset = 150
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x + self.offset // 2, self.rect.y + self.offset // 2 - 3, self.rect.w // 8 - self.offset, self.rect.h - self.offset))
        screen.blit(self.image, self.rect, self.dest_rect)

    def update(self, screen, dt):
        self.draw(screen)
        #self.dest_rect.x += self.dest_rect.w
        self.x_pos += dt
        self.dest_rect.x = self.x_pos
        print(f"dt: {str(dt):_<50}; x position: {str(self.x_pos):_<50}")
        if self.dest_rect.x >= self.rect.w:
            self.dest_rect.x = 0
            self.x_pos

class Player(pygame.sprite.Sprite):
    def __init__(self, entity_id, img_dir_path, groups, ground_group):
        super().__init__(groups)
        # Player ID
        self.player_id = entity_id
        self.ground_group = ground_group
        print(len(self.ground_group))

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
                        self.vertical_velocity = -1000
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
        if self.in_air:
            self.vertical_velocity += 2500 * dt 

        if not self.attacking:
            self.x_position += self.horizontal_velocity * dt 
            self.y_position += self.vertical_velocity * dt 

# left and right movement
        collision_with_ground = pygame.sprite.spritecollide(self, self.ground_group, dokill=False)

        for ground in collision_with_ground:
            if self.body_rect.bottom > ground.rect.top:
                self.body_rect.bottom = ground.rect.top
                self.y_position = ground.rect.top - self.body_rect.height
                self.vertical_velocity = 0
                self.jumping = False

            elif self.body_rect.top < ground.rect.bottom:
                self.body_rect.top = ground.rect.bottom
                self.y_position = ground.rect.bottom
                self.vertical_velocity = 0

            # Check if the player is on the ground before adjusting x-position
            elif self.body_rect.right > ground.rect.left and self.horizontal_velocity > 0:
                self.body_rect.right = ground.rect.left
                self.x_position = ground.rect.left - self.body_rect.width

            elif self.body_rect.left < ground.rect.right and self.horizontal_velocity < 0:
                self.body_rect.left = ground.rect.right
                self.x_position = ground.rect.right

        self.body_rect.x = int(self.x_position)
        self.body_rect.y = int(self.y_position)

        text = f"{str(self.jumping): <6}, {str(self.vertical_velocity): <10}, {str(self.rect.bottom): <10}"
            # Render text
        text_surface = self.font.render(text, True, (255,255,255))

        # Get the rectangle of the text surface

        text_rect = text_surface.get_rect()

        # Center the text on the screen
        text_rect.topleft = (0, 60)

        # Blit the text surface onto the screen
        screen.blit(text_surface, text_rect)


    def def_animation(self):
        # Update animation
        if not self.attacking:
            if self.horizontal_velocity > 0:
                self.image_index = 'Run'
                self.direction = 0
            elif self.horizontal_velocity < 0:
                self.image_index = 'Run'
                self.direction = 1
            else:
                self.image_index = 'Idle'

            if self.jumping:
                self.image_index= 'Jump'


    def draw(self, screen):
        self.blit_rect = pygame.Rect(self.body_rect.x - 75, self.body_rect.y - 75, self.image_size, self.image_size)
        # pygame.draw.rect(screen, (255, 255, 255), self.body_rect)
        screen.blit(
                    self.images[self.image_index][self.direction], # Imgae ( images, which image, what dirrection )
                    self.blit_rect, # Draw rect ( where to draw )
                    self.image_dest_rect[self.image_index][self.direction][int(self.dest_rect_index)] # Which tile ( destination rects, for which image, what direction )
                )

    def update_indexes(self, dt):
        # checks if frame is less than 8 (needs optimisation for all animation lengths)
        self.dest_rect_index += dt * self.animation_speed 
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
        
        # Update animation
        self.update_indexes(dt)
        self.def_animation()


        self.updata_pos(dt, screen)
        
        self.draw(screen)
        
        # wierd text stuff
        # Draw sprite on screen
        text = f"{str(self.jumping): <6}, {str(self.vertical_velocity): <10}, {str(self.rect.bottom): <10}"
            # Render text
        text_surface = self.font.render(text, True, (255,255,255))

        # Get the rectangle of the text surface

        text_rect = text_surface.get_rect()

        # Center the text on the screen
        text_rect.topleft = (0, 0)

        # Blit the text surface onto the screen
        screen.blit(text_surface, text_rect)

        text = f"{str(self.attacking): <6}, {str(self.horizontal_velocity): <10}, {str(): <10}"
            # Render text
        text_surface = self.font.render(text, True, (255,255,255))

        # Get the rectangle of the text surface

        text_rect = text_surface.get_rect()

        # Center the text on the screen
        text_rect.topleft = (0, 30)

        # Blit the text surface onto the screen
        screen.blit(text_surface, text_rect)
