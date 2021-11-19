import arcade
from game.constants import SPRITE_SCALING_COIN
class Coin: 

    def __init__(self):
        self.coin = None

    def create_coin(self):
        self.coin = arcade.Sprite(":resources:images/items/coinGold.png", SPRITE_SCALING_COIN)