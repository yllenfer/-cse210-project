import arcade
from game.constants import SPRITE_SCALING, SCREEN_HEIGHT, SCREEN_WIDTH
import random


class Car(arcade.Sprite):

    def __init__(self):
        self.cars_list = None
        self.car = None
        super().__init__(":resources:images/enemies/wormGreen.png", SPRITE_SCALING)

    def reset_position(self):
        self.center_y = random.randrange(SCREEN_HEIGHT + 40,
                                         SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):
        # Move the coin
        self.center_y -= 1

        # See if the coin has fallen off the bottom of the screen.
        # If so, reset it.
        if self.top < 0:
            self.reset_position()
