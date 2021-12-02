import arcade


class Lives(arcade.Sprite):

    def __init__(self, center_x):
        super().__init__(":resources:images/animated_characters/female_person/femalePerson_idle.png", 0.25)
        self.center_x = center_x
        self.center_y = 20

    def update(self):
        pass
