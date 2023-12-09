from entity import Entity, Image_Bank
import math


class Enemy_1(Entity):
    def __init__(self, entity_id, enemy_name,  image_bank, groups):
        super().__init__(entity_id, enemy_name, image_bank, groups)

    def _ai_(self):
        # print(len(self.groups["player"]))
        for en in self.groups["player"]:
            # print(en.entity_id)
            # print(en.body_rect.center)
            pass
    def __entity_specific__(self):
        self._ai_()
       
