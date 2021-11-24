import arcade
from arcade.key import Y
from arcade.sprite import PyMunk
from game.constants import SPRITE_SCALING, SCREEN_HEIGHT, SCREEN_WIDTH, Y_COUNT, Y_SPACING, Y_START, PICTURES_PATH
import random


class Car(arcade.Sprite):

    def __init__(self, center_y):
        super().__init__((PICTURES_PATH + "car.png"), SPRITE_SCALING)
        self.change_x = random.randint(2, 7)
        self.center_y = center_y
        self.center_x = random.choice([0, SCREEN_WIDTH])

    def reset_position(self):
        pass

    def update(self):
        # Move the coin
        #self.center_y -= 1

        # See if the coin has fallen off the bottom of the screen.
        # If so, reset it.
        if self.left > SCREEN_WIDTH:
            self.center_x = 0
        return super().update()
