from entity import Entity, Image_Bank


class Enemy_1(Entity):
    def __init__(self, entity_id, image_bank, groups):
        super().__init__(entity_id, image_bank, groups)
