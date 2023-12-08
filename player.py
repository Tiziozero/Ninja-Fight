import pygame, os, sys, time, math
from entity import Entity
from debug import debug, print_debug


class Player(Entity):
    def __init__(self, entity_id, image_bank, groups):
        super().__init__(entity_id, image_bank, groups)
        self.entity_group = groups["entity"]
        self.is_attacking = False
        self.attack_can_damage = True
    def move(self, event):
        if not self.attacking:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    self.horizontal_velocity = 0
                    self.attacking = True
                    self.dest_rect_index = 0
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
                    # self.rect.y -= 1
                    self.jumping = True
                    print("Jump", self.vertical_velocity)

            if event.type == pygame.KEYUP:
                if not self.attacking:
                    if event.key == pygame.K_a:
                        self.horizontal_velocity += self.velocity
                    if event.key == pygame.K_d:
                        self.horizontal_velocity -= self.velocity
    def update_indexes(self, dt):
        self.dest_rect_index += dt * self.animation_speed 
        # debug(f"{str(int(self.dest_rect_index)): <3}, {str(int(len(self.image_bank.image_dest_rect[self.image_index][self.direction])))}")
        debug(str(self.dest_rect_index))
        t = f"attacking: {str(self.attacking): <10}; dest rect index: {str(int(self.dest_rect_index)): <10}; is attacking: {str(self.is_attacking): <10}; attack can damage: {str(self.attack_can_damage): <10}"
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
                


