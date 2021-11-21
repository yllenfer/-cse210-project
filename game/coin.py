import arcade
from game.constants import SPRITE_SCALING_COIN
import random
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Coin(arcade.Sprite):

    def __init__(self):
        self.coin = None
        self.coin_list = None
        super().__init__(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)
        self.center_x = random.randrange(SCREEN_WIDTH)
        self.center_y = random.randrange(SCREEN_HEIGHT)

    # def create_coin(self):
    #     coin = self.coin = arcade.Sprite(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)
    #     for i in range(2):
    #         coin.center_x = random.randrange(SCREEN_WIDTH)
    #         coin.center_y = random.randrange(SCREEN_HEIGHT)
    #         coin.change_x = random.randrange(0, 1)
    #         coin.change_y = random.randrange(1, 4)
    #         self.coin_list.apped(self.coin)