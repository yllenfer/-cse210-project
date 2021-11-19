import arcade
from game.constants import SPRITE_SCALING
from game.point import Point


class Player(arcade.Sprite):

    def __init__(self):
        self.player = None
        # self.change_x = 0
        # self.change_y = 0
        self.center_x = 0
        self.center_y = 0
        super().__init__()

    # def do_update(self):
    #     pass

    def create_player(self):
        self.player.center_x = 50
        self.player.center_y = 50
        self.player = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                    SPRITE_SCALING)
        # create sprite list and add the player in it
