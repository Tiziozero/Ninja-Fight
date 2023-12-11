from entity import Entity, Image_Bank
from debug import debug
import math


class Enemy_1(Entity):
    def __init__(self, entity_id, enemy_name,  image_bank, groups):
        super().__init__(entity_id, enemy_name, image_bank, groups)
        self.velocity = 150

    def _ai_(self):
        # print(len(self.groups["player"]))
        for en in self.groups["player"]:
            # print(en.entity_id)
            # print(en.body_rect.center)
            if not self.attacking:
                if abs(en.body_rect.centerx - self.body_rect.centerx) <= 80:
                    if abs(en.body_rect.centery - self.body_rect.centery) < 25:
                        self.horizontal_velocity = 0
                        self.attacking = True
                        self.dest_rect_index = 0
                        
                        # self.image_index = 'Attack1'
                        self.image_index = self.attack_animation_sequence_1[self.attack_index]
                        self.attack_index += 1
                        if self.attack_index >= len(self.attack_animation_sequence_1):
                            self.attack_index = 0

                debug("ai not attacking")
                if en.body_rect.centerx > self.body_rect.centerx:
                    self.horizontal_velocity = self.velocity
                elif en.body_rect.centerx < self.body_rect.centerx:
                    self.horizontal_velocity = -self.velocity
                else:
                    pass

            else:
                pass
    def __entity_specific__(self):
        self._ai_()
       
