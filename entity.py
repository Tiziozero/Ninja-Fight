import pygame, os, sys, time, math
from debug import debug, print_debug
from enum import Enum

class attack_types(Enum):
    meele = 0 
    short_range = 1
    long_range = 2



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
    def __init__(self, entity_id, entity_name,  image_bank, groups):
        super().__init__()
        # Player ID
        self.entity_id = entity_id
        self.entity_name = entity_name

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
        self.attack_index = 0
        self.entity_group = groups["entity"]
        self.is_attacking = False
        self.attack_can_damage = True
        self.attack_animation_sequence_1 = ['Attack1', 'Attack2']
        self.attack_animation_sequence_2 = ['Attack1', 'Attack2']

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


    def updata_pos(self, dt):
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


    def entity_attack_(self, type = 0, extra = None):
        if type == attack_types.meele:
            self.horizontal_velocity = 0
            self.attacking = True
            self.dest_rect_index = 0
            
            # self.image_index = 'Attack1'
            self.image_index = self.attack_animation_sequence_1[self.attack_index]
            self.attack_index += 1
            if self.attack_index >= len(self.attack_animation_sequence_1):
                self.attack_index = 0
        elif type == attack_types.long_range:
            self.horizontal_velocity = 0
            self.attacking = True
            self.dest_rect_index = 0
            
            # self.image_index = 'Attack1'
            self.image_index = self.attack_animation_sequence_2[self.attack_index]
            self.attack_index += 1
            if self.attack_index >= len(self.attack_animation_sequence_2):
                self.attack_index = 0
            b_vel = 1000
            if self.direction == 0:
                print("right")
            elif self.direction == 1:
                print("left")
                b_vel *= -1
            bullet = Bullet(self.entity_id, self.groups, self.body_rect.centerx, self.body_rect.centery, b_vel)
            # self.groups["bullets"].add(bullet)
            self.groups["draw"].add(bullet)
            self.groups["all"].add(bullet)


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
                self.vertical_velocity = 0
                self.attacking = False
                self.attack_can_damage = True

    def __entity_specific__(self):
        debug(f"{self.entity_id}")

    def update(self,screen, dt):
        self.__entity_specific__()
        # Update entity
        self.clock += dt
        self.updata_pos(dt)
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

    def is_collision(self, rect1, rect2):
        x1, y1, width1, height1 = rect1
        x2, y2, width2, height2 = rect2

        # Calculate the right and bottom coordinates of each rectangle
        right1 = x1 + width1
        bottom1 = y1 + height1
        right2 = x2 + width2
        bottom2 = y2 + height2

        # Check for overlap on the x-axis and y-axis
        if x1 < right2 and right1 > x2 and y1 < bottom2 and bottom1 > y2:
            return True
        else:
            return False
    def assoult_entity(self):
        # for entity in self.groups["entity"]:
        collisions = pygame.sprite.spritecollide(self, self.groups["entity"], False)
        # for entity in collisions:
        for entity in self.groups["entity"]:
            if entity.entity_id != self.entity_id:
                if self.is_collision(entity.body_rect, self.rect):
                    print(entity.entity_id)
                    print(f"-- damage: {self.attack_points + self.attack_points*self.buffs}")
                    entity.attacked(self.attack_points, self.buffs)
                    # entity.life_points -= self.attack_points * self.buffs
                    self.kill()

    def __entity_specific__(self):
        debug(f"i: {self.entity_id}")
        pass
    def update(self, screen, dt):
        self.__entity_specific__()
        self.rect.x += self.velocity * dt
        self.assoult_entity()
        t = abs(self.startcoords[0] - abs(self.rect.centerx))
        debug(f"updatig bullet; {str( str(self.rect.x)): <30}, {str(t)}")
        if t >= 3000:
            print("bullet killed")
            self.kill()
