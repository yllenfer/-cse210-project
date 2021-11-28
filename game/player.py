import arcade
from game.constants import SPRITE_SCALING, SCREEN_WIDTH, SCREEN_HEIGHT
import os


class Player(arcade.Sprite):

    def __init__(self):
        # self.player_sprite = None
        super().__init__(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING)

        self.center_x = 400
        self.center_y = 50

    def update(self):

        """ Move the player """

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0

        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0

        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1