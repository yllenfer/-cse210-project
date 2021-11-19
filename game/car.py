import arcade
from game.constants import SPRITE_SCALING, SPRITE_SIZE


class Car:

    def __init__(self):
        self.cars_list = None
        self.car = None
        # super().__init__()

    def create_car(self):
        self.car = arcade.Sprite(":resources:images/enemies/wormGreen.png", SPRITE_SCALING)
        self.cars_list.append(self.car)
