import pygame, os, sys, time, math
from debug import debug, print_debug, log
from enum import Enum

class attack_types(Enum):
    meele = 0 
    short_range = 1
    long_range = 2


class Sound_Bank:
    def __init__(self, path):
        log("loading sounds for path " + path + "...", level=1)
        self.sounds = {}
        self.load_sounds(path)

    def load_sounds(self, path):
        names = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        log(f"files for {path}: {names}", level=1)
        for name in names:
            self.sounds[name.split(".mp3")[0]] = pygame.mixer.Sound(path+name)
            self.sounds[name.split(".mp3")[0]].set_volume(0.1)
        log(f"sounds loaded: {self.sounds}", level=2)

class Image_Bank:
    def __init__(self, path):
        log("image for path " + path, level=1)
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
        log(f"loading images for {path}...", level=1)
        for name in self.image_names:
            log(f"loading {name}", level=2)
            path_to_image = path + name + self.image_format 

            image_current = pygame.image.load(path_to_image).convert_alpha()

            self.images[name] = [image_current, pygame.transform.flip(image_current, True, False)]
            self.image_rect[name] = self.images[name][0].get_rect()
            self.image_dest_rect[name] = [
                                            [pygame.Rect(self.image_size * i, 0, self.image_size, self.image_size)  for i in range(self.image_rect[name].w // self.image_size)], # right
                                            [pygame.Rect(self.image_rect[name].w - self.image_size - self.image_size * i, 0, self.image_size, self.image_size)  for i in range(self.image_rect[name].w // self.image_size)]  # left
                                            ]


class Entity(pygame.sprite.Sprite):
    def __init__(self, entity_id, entity_name,  image_bank, groups, blit_rect_offset_x = 0, blit_rect_offset_y = 0, game_class = None):
        super().__init__()
        # Player ID
        self.entity_id = entity_id
        self.entity_name = entity_name

        # Image Bank
        self.image_bank = image_bank
        if game_class != None:
            self.game_class = game_class
            self.image_bank = self.game_class.image_bank
            self.sound_bank = self.game_class.sound_bank

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
        self.blit_rect_offsets = [blit_rect_offset_x, blit_rect_offset_y]

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
        self.position = [0, 0]
        self.entity_sprint_velocity = 5000
        self.entity_sprint_time = 0.03
        self.ml = 1
        self.sprint_time = time.time()
        self.sprinting = False
        # self.position[0], self.position[1] = 0, 0
        self.velocity = 300
        self.horizontal_velocity = 0
        self.vertical_velocity = 0
        # self.in_air = True
        self.jump_hight = 800
        log(f"Created entity: {self.entity_id}", level=1)

    def entity_timers(self):
        ttime = time.time()
        time_difference = self.sprint_time - time.time() 
        # debug(str(time_difference))
        # debug(f"{str(self.horizontal_velocity): >7}")
        # log(abs(time_difference))
        if self.sprinting:
            if self.attacking:
                self.sprinting = False
                log("attacking in sprint", level=3)
            if abs(time_difference) >= self.entity_sprint_time:
                log("time! sprint", level=3)
                self.horizontal_velocity -= self.entity_sprint_velocity * self.ml
                self.sprinting = False
    def setup(self):
        pass


    def updata_pos(self, dt):
        # Updata vertical y velocity due to gravity
        self.vertical_velocity += 2500 * dt 
        
        # Update entity's x position due to entity moving
        if not self.attacking:
            self.position[0] += self.horizontal_velocity * dt 

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
                    self.position[0] = floor.rect.left - 50

            elif self.body_rect.left < floor.rect.right and self.body_rect.left > floor.rect.left:
                if ( self.body_rect.top <= floor.rect.top and self.body_rect.bottom >= floor.rect.bottom ) or ( self.body_rect.top >= floor.rect.top and self.body_rect.bottom <= floor.rect.bottom ):
                    self.body_rect.left = floor.rect.left
                    self.position[0] = floor.rect.right


        # Update entity's vertivcal position if not attacking cuz it's cool 
        if not self.attacking:
            self.position[1] += self.vertical_velocity * dt 
        self.body_rect.x = int(math.ceil(self.position[0]))
        self.body_rect.y = int(self.position[1])


    def entity_sprint(self):
        log("sprint", level=3)
        self.sprint_time = time.time()
        log("time: {self.sprint_time}", level=3)
        if not self.sprinting:
            self.ml = 1
            if self.direction == 0:
                log("sprint right", level=3)
            elif self.direction == 1:
                log("sprint left", level=3)
                self.ml *= -1
            self.horizontal_velocity += self.entity_sprint_velocity * self.ml
            self.sprinting = True

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
                log("attack to right: long-range", level=3)
            elif self.direction == 1:
                log("attack to left: long-range", level=3)
                b_vel *= -1
            bullet = Bullet(self.entity_id, self.groups, self.body_rect.centerx, self.body_rect.centery, b_vel, entity_class=self)
            # self.groups["bullets"].add(bullet)
            self.groups["draw"].add(bullet)
            self.groups["all"].add(bullet)


    def attack(self):
        if self.is_attacking:
            self.sound_bank.sounds["sword_wave"].play()
            log(self.groups["entity"], level=4)
            log(self.dest_rect_index, level=4)
            for entity in self.groups["entity"]:
                # Checks if entity isn't itself
                if entity.entity_id != self.entity_id:
                    # Checks of attack_range_rect's sides are inside entity's body_rect
                    if ( entity.body_rect.right >= self.attack_range_rect.left and entity.body_rect.left <= self.attack_range_rect.left ) or ( entity.body_rect.right >= self.attack_range_rect.right and entity.body_rect.left <= self.attack_range_rect.right ):
                        # Checks of attack_range_rect's top or bottom  are inside entity's body_rect
                        if ( self.body_rect.top <= entity.body_rect.bottom and self.body_rect.top >= entity.body_rect.top ) or ( self.body_rect.bottom <= entity.body_rect.bottom and self.body_rect.bottom >= entity.body_rect.top ):
                            # If yes then inflict damage
                            log("attack", level=4, end='')
                            log(entity.entity_id, level=4)
                            entity.attacked(self.attack_points, 0.5)
                            self.sound_bank.sounds["sword_damage"].play()
                else:
                    pass
            self.is_attacking = False

    def attacked(self, attack_points, percentage_extra):
        log(f"damage: {attack_points}, {percentage_extra}, {attack_points*percentage_extra}, {attack_points + attack_points*percentage_extra}", level=3)
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
        # t = f"{self.entity_id}: {str(self.life_points)}"
        # debug(t)
        # Update blit rect
        self.blit_rect = pygame.Rect(self.body_rect.x - 75 + self.blit_rect_offsets[0], self.body_rect.y - 75 + self.blit_rect_offsets[1], self.image_bank.image_size, self.image_bank.image_size)
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

            # pygame.draw.rect(screen, (0, 0, 0), self.attack_range_rect, 2)
            # pygame.draw.rect(screen, (255, 255, 255), self.body_rect)
            pass
            # screen.blit(
            #             self.image_bank.images[self.image_index][self.direction], # Imgae ( images, which image, what dirrection )
            #             self.blit_rect, # Draw rect ( where to draw )
            #             self.image_bank.image_dest_rect[self.image_index][self.direction][math.floor(self.dest_rect_index)] # Which tile ( destination rects, for which image, what direction ) ( use of self.image_idex, self.direction and self.dest_rect_index for reasons undefined for now )
            #         )
        except IndexError:
            log(f"index error: -> {self.dest_rect_index}, {math.floor(self.dest_rect_index)}", level=5)
        except:
            log("Unkown error!", level=5)

    def update_indexes(self, dt):
        self.dest_rect_index += dt * self.animation_speed 
        # debug(f"{str(int(self.dest_rect_index)): <3}, {str(int(len(self.image_bank.image_dest_rect[self.image_index][self.direction])))}")
        # debug(str(self.dest_rect_index))
        # t = f"current index len; {len(self.image_bank.image_dest_rect[self.image_index][self.direction])}, image index: {self.image_index}"
        # debug(t)
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
            log("attacking", level=3)
            self.attack_can_damage = False
            self.is_attacking = True

        if self.dest_rect_index >= len(self.image_bank.image_dest_rect[self.image_index][self.direction]):
            self.dest_rect_index = 0
            if self.attacking:
                self.vertical_velocity = 0
                self.attacking = False
                self.attack_can_damage = True

    def __entity_specific__(self):
        debug(f"entity specific for: {self.entity_id}")

    def respawn(self):
        self.position = [0, 0]
        self.life_points = 10000

    def update(self,screen, dt):
        self.__entity_specific__()
        # Update entity
        self.clock += dt
        self.updata_pos(dt)
        self.draw(screen, dt)
        self.image = self.image_bank.images[self.image_index][self.direction].subsurface(self.image_bank.image_dest_rect[self.image_index][self.direction][math.floor(self.dest_rect_index)])
        self.rect = self.blit_rect

        self.attack()
        self.entity_timers()
        if self.life_points <= 0:
            log(f"{self.entity_id} died. l bozo", level=1)
            # self.kill()
            self.respawn()
        if self.is_attacking: log("is attacking", level=4)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, entity_id, groups, x, y, velocity, attack_points = 1000, buffs = [0.5, 0.2, 0.2], entity_class=0):
        super().__init__()
        self.entity_id = entity_id
        self.entity_class = entity_class
        if self.entity_class:
            self.sound_bank = self.entity_class.sound_bank
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
                    log(entity.entity_id, level=3)
                    log(f"-- damage: {self.attack_points + self.attack_points*self.buffs}", level=3)
                    entity.attacked(self.attack_points, self.buffs)
                    # entity.life_points -= self.attack_points * self.buffs
                    try:
                        self.sound_bank.sounds["sword_slash2"].play() # Temprary solution
                    except NameError as e:
                        log("ERROR -> {e}", level=0)
                    except:
                        log("ERROR -> Unkown error", level=0)
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
            log("bullet killed", level=3)
            self.kill()
