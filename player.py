import pygame, os, sys, time, math
from entity import Entity
from debug import debug, print_debug


class Player(Entity):
    def __init__(self, entity_id, image_bank, img_dir_path, groups, ground_group):
        super().__init__(entity_id, image_bank, groups, ground_group)
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
        if self.dest_rect_index >= len(self.image_bank.image_dest_rect[self.image_index][self.direction]):
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


