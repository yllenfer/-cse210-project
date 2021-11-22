import arcade
from game.constants import SPRITE_SCALING, SCREEN_HEIGHT, SCREEN_WIDTH
import random


class Car(arcade.Sprite):

    def __init__(self):
        super().__init__(":resources:images/enemies/wormGreen.png", SPRITE_SCALING)
        self.change_x = 2
        self.reset_position()

    def reset_position(self):
        self.center_y = 400#random.randrange(SCREEN_HEIGHT + 20,
                                        # SCREEN_HEIGHT + 100)
        self.center_x = 300#random.randrange(0)

    def update(self):
        # Move the coin
        #self.center_y -= 1

        # See if the coin has fallen off the bottom of the screen.
        # If so, reset it.
        if self.left > SCREEN_WIDTH:
            self.reset_position()

        return super().update()
