import arcade
from arcade.key import Y
from arcade.sprite import PyMunk
from game.constants import CAR_SPRITE_SCALING, SCREEN_HEIGHT, SCREEN_WIDTH, PICTURES_PATH
import random


class Car(arcade.Sprite):

    def __init__(self, center_y, velocity):
        super().__init__((PICTURES_PATH + "car.png"), CAR_SPRITE_SCALING)
        self.change_x = velocity
        self.center_y = center_y
        self.center_x = random.choice([0, SCREEN_WIDTH])

    def update(self):
        if self.left > SCREEN_WIDTH:
            self.center_x = 0
        elif self.right < 0:
            self.center_x = 800
            
        return super().update()
