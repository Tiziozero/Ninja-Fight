import pygame, os, sys, time, math
from debug import debug, print_debug


class Image_Bank:
    def __init__(self, path):
        print("image for path", path)
        self.images = {} #contains actual images
        self.images_dirctory_path_relative_to_main_file = path
        self.image_rect = {} # contains images rect
        self.image_dest_offset = 150 # total offset for body rect
        self.image_size = 200 # may vary
        self.image_names = ['Attack1', 'Attack2', 'Death', 'Fall', 'Idle', 'Jump', 'Run', 'Take Hit']
        self.image_indexes = ['Attack1', 'Attack2', 'Death', 'Fall', 'Idle', 'Jump', 'Run', 'Take Hit']
        self.image_dest_rect = {} # image destitanion rects for blitting
        self.images_lef = {} # left images
        self.images_right = {} # right images
        self.image_format = '.png' # image file format
        self.load_img(path)

    def load_img(self, path):
        print(f"loading images for {path}...")
        for name in self.image_names:
            print(f"    loading {name}")
            path_to_image = path + name + self.image_format 

            image_current = pygame.image.load(path_to_image).convert_alpha()

            self.images[name] = [image_current, pygame.transform.flip(image_current, True, False)]
            self.image_rect[name] = self.images[name][0].get_rect()
            self.image_dest_rect[name] = [
                                            [pygame.Rect(self.image_size * i, 0, self.image_size, self.image_size)  for i in range(self.image_rect[name].w // self.image_size)], # right
                                            [pygame.Rect(self.image_rect[name].w - self.image_size - self.image_size * i, 0, self.image_size, self.image_size)  for i in range(self.image_rect[name].w // self.image_size)]  # left
                                            ]


class Entity(pygame.sprite.Sprite):
    def __init__(self, entity_id, image_bank, groups):
        super().__init__()
        # Player ID
        self.entity_id = entity_id

        # Entity Groups
        self.ground_group = groups["ground"]
        self.groups = groups
        self.entity_group = groups["entity"]
        
        # Entity properties
        self.life_points = 10000
        self.attack_points = 750
        self.attacking_damage = False
        self.image = pygame.Surface((200,200))
        self.rect = self.image.get_rect(center=(200, 0))
        # Image Bank
        self.image_bank = image_bank

        # Rectangles
        self.blit_rect = pygame.Rect(200, 0, self.image_bank.image_size, self.image_bank.image_size)
        self.body_rect = pygame.Rect(200, 0, 50, 50)
        # self.rect = pygame.Rect(0,0,0,0)

        # Animation Stuff
        self.image_index = 'Idle'
        self.direction = 0
        self.dest_rect_index = 0
        self.animation_speed = 20
        self.clock = 0
        self.jumping = False

        # Attack
        self.is_attacking = False
        self.attacking = False
        self.temp_attac_rect_surf = pygame.Surface((125, 75))
        self.attack_range_rect = self.temp_attac_rect_surf.get_rect()
        self.attacking_damage = False
        self.is_attacking = False
        self.attack_can_damage = True

        # Test propeties
        self.x_position, self.y_position = 0, 0
        self.velocity = 300
        self.horizontal_velocity = 0
        self.vertical_velocity = 0
        # self.in_air = True
        self.jump_hight = 800
        print(f"Created entity: {self.entity_id}")

    def setup(self):
        pass


    def updata_pos(self, dt, screen):
        # Updata vertical y velocity due to gravity
        self.vertical_velocity += 2500 * dt 
        
        # Update entity's x position due to entity moving
        if not self.attacking:
            self.x_position += self.horizontal_velocity * dt 

        # Entities collisions with floor
        for floor in self.ground_group:
            if self.body_rect.bottom >= floor.rect.top and self.body_rect.bottom <= floor.rect.bottom and self.body_rect.top < floor.rect.top:
                if self.body_rect.right >= floor.rect.left and self.body_rect.left <= floor.rect.right:
                    if self.vertical_velocity >= 0:
                        self.body_rect.bottom = floor.rect.top
                        self.vertical_velocity = 0
                        self.jumping = False
            
            elif self.body_rect.top <= floor.rect.bottom and self.body_rect.top >= floor.rect.top and self.body_rect.bottom > floor.rect.bottom:
                if self.body_rect.right >= floor.rect.left and self.body_rect.right <= floor.rect.right:
                    if self.vertical_velocity <= 0:
                        self.body_rect.top = floor.rect.bottom
                        self.vertical_velocity = 0
            
            elif self.body_rect.right > floor.rect.left and self.body_rect.right < floor.rect.right:
                if ( self.body_rect.top <= floor.rect.top and self.body_rect.bottom >= floor.rect.bottom ) or ( self.body_rect.top >= floor.rect.top and self.body_rect.bottom <= floor.rect.bottom ):
                    self.body_rect.right = floor.rect.left
                    self.x_position = floor.rect.left - 50

            elif self.body_rect.left < floor.rect.right and self.body_rect.left > floor.rect.left:
                if ( self.body_rect.top <= floor.rect.top and self.body_rect.bottom >= floor.rect.bottom ) or ( self.body_rect.top >= floor.rect.top and self.body_rect.bottom <= floor.rect.bottom ):
                    self.body_rect.left = floor.rect.left
                    self.x_position = floor.rect.right


        # Update entity's vertivcal position if not attacking cuz it's cool 
        if not self.attacking:
            self.y_position += self.vertical_velocity * dt 
        self.body_rect.x = int(math.ceil(self.x_position))
        self.body_rect.y = int(self.y_position)

    def attack(self):
        if self.is_attacking:
            print(self.groups["entity"])
            print(self.dest_rect_index)
            for entity in self.groups["entity"]:
                # Checks if entity isn't itself
                if entity.entity_id != self.entity_id:
                    # Checks of attack_range_rect's sides are inside entity's body_rect
                    if ( entity.body_rect.right >= self.attack_range_rect.left and entity.body_rect.left <= self.attack_range_rect.left ) or ( entity.body_rect.right >= self.attack_range_rect.right and entity.body_rect.left <= self.attack_range_rect.right ):
                        # Checks of attack_range_rect's top or bottom  are inside entity's body_rect
                        if ( self.body_rect.top <= entity.body_rect.bottom and self.body_rect.top >= entity.body_rect.top ) or ( self.body_rect.bottom <= entity.body_rect.bottom and self.body_rect.bottom >= entity.body_rect.top ):
                            # If yes then inflict damage
                            print("attack")
                            print(entity.entity_id)
                            entity.attacked(self.attack_points, 0.5)
                else:
                    pass
            self.is_attacking = False

    def attacked(self, attack_points, percentage_extra):
        print("damage: ", end="")
        print(attack_points, percentage_extra, attack_points*percentage_extra, attack_points + attack_points*percentage_extra)
        self.life_points -= (attack_points + attack_points * percentage_extra)


    def def_animation(self):
        # Update animation
        if not self.attacking:
            # Update entity's animation index depending on its velocity vertical and horizontal
            if self.horizontal_velocity > 0:
                self.image_index = 'Run'
                self.direction = 0
            elif self.horizontal_velocity < 0:
                self.image_index = 'Run'
                self.direction = 1
            if self.jumping:
                self.image_index= 'Jump'
            if self.vertical_velocity > 0:
                self.image_index = 'Fall'
            elif self.vertical_velocity == 0 and self.horizontal_velocity == 0:
                self.image_index = 'Idle'


    def draw(self, screen, dt):
        t = f"{self.entity_id}: {str(self.life_points)}"
        debug(t)
        # Update blit rect
        self.blit_rect = pygame.Rect(self.body_rect.x - 75, self.body_rect.y - 75, self.image_bank.image_size, self.image_bank.image_size)
        # Update attack range rect
        self.attack_range_rect.y = self.body_rect.top - 25

        if self.direction == 0:
            self.attack_range_rect.left = self.body_rect.left
        else:
            self.attack_range_rect.right = self.body_rect.right
        
        # Update animation index and dest rect image
        self.def_animation()
        self.update_indexes(dt)
        
        # Try to draw and  catch potential errors
        try:
            pygame.draw.rect(screen, (0, 0, 0), self.attack_range_rect, 2)

            # screen.blit(
            #             self.image_bank.images[self.image_index][self.direction], # Imgae ( images, which image, what dirrection )
            #             self.blit_rect, # Draw rect ( where to draw )
            #             self.image_bank.image_dest_rect[self.image_index][self.direction][math.floor(self.dest_rect_index)] # Which tile ( destination rects, for which image, what direction ) ( use of self.image_idex, self.direction and self.dest_rect_index for reasons undefined for now )
            #         )
        except IndexError:
            print(f"index error: -> {self.dest_rect_index}, {math.floor(self.dest_rect_index)}")
        except:
            print("Unkown error!")

    def update_indexes(self, dt):
        self.dest_rect_index += dt * self.animation_speed 
        # debug(f"{str(int(self.dest_rect_index)): <3}, {str(int(len(self.image_bank.image_dest_rect[self.image_index][self.direction])))}")
        # debug(str(self.dest_rect_index))
        t = f"current index len; {len(self.image_bank.image_dest_rect[self.image_index][self.direction])}, image index: {self.image_index}"
        debug(t)
        # t = f"attacking: {str(self.attacking): <10}; dest rect index: {str(int(self.dest_rect_index)): <10}; is attacking: {str(self.is_attacking): <10}; attack can damage: {str(self.attack_can_damage): <10}"
        # debug(t)
        # Player will attack if:
        #     - he is attacking
        #     - int dest rect is 4
        #     - is attacking is True
        #     - attack can damage is True
        # 
        # In here i check if these conditions are met.
        # If they are, i set is_attacking to true so that
        #     - in the attacking function hte player can check collisions with sprites in entity group
        #     - damage if conditions are met
        # the attcking function will be called after 'update_index'
        # is_attacking should be true only for one loop and onlu between 'ipdate+index' and 'attacking'
        # 'attacking' is called 'attacked' for now
        if self.attacking and int(self.dest_rect_index) == 4 and self.is_attacking == False and self.attack_can_damage:
            print("attacking")
            self.attack_can_damage = False
            self.is_attacking = True

        if self.dest_rect_index >= len(self.image_bank.image_dest_rect[self.image_index][self.direction]):
            self.dest_rect_index = 0
            if self.attacking:
                # for entity in self.entity_group:
                self.vertical_velocity = 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_d]:
                    self.horizontal_velocity += self.velocity
                    print("d is pressed", self.horizontal_velocity, self.velocity)
                
                if keys[pygame.K_a]:
                    self.horizontal_velocity -= self.velocity
                    print("a is pressed", self.horizontal_velocity, self.velocity)
                self.attacking = False
                self.attack_can_damage = True


    def update(self, screen, dt):
        # Update entity
        self.clock += dt
        self.updata_pos(dt, screen)
        self.draw(screen, dt)
        self.image = self.image_bank.images[self.image_index][self.direction].subsurface(self.image_bank.image_dest_rect[self.image_index][self.direction][math.floor(self.dest_rect_index)])
        self.rect = self.blit_rect

        self.attack()
        if self.life_points <= 0:
            print(f"{self.entity_id} died. l bozo")
            self.kill()
        if self.is_attacking: print("is attacking")


class Bullet(pygame.sprite.Sprite):
    def __init__(self, entity_id, groups, x, y, velocity, attack_points = 1000, buffs = [0.5, 0.2, 0.2]):
        super().__init__()
        self.entity_id = entity_id
        self.groups = groups
        self.image = pygame.Surface((10, 10))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = velocity
        self.startcoords = (x, y)
        self.attack_points = attack_points
        self.buffs = 0
        for buff in buffs: self.buffs += buff
    def assoult_entity(self):
        # for entity in self.groups["entity"]:
        collisions = pygame.sprite.spritecollide(self, self.groups["entity"], False)
        for entity in collisions:
            if entity.entity_id != self.entity_id:
                print(entity.entity_id)
                print(f"-- damage: {self.attack_points + self.attack_points*self.buffs}")
                entity.attacked(self.attack_points, self.buffs)
                # entity.life_points -= self.attack_points * self.buffs
                self.kill()
    def update(self, screen,  dt):
        self.rect.x += self.velocity * dt
        self.assoult_entity()
        t = abs(self.startcoords[0] - abs(self.rect.centerx))
        debug(f"updatig bullet; {str( str(self.rect.x)): <30}, {str(t)}")
        if t >= 3000:
            print("bullet killed")
            self.kill()
