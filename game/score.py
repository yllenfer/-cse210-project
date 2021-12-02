from game.lives import Lives
from game.player import Player
from game.coin import Coin
import arcade


class Score:

    def __init__(self):
        self.score = 0
        # arcade.draw_text(self.output,
        #                  45, 30,
        #                  arcade.color.WHITE, 12,
        #                  anchor_x="center")

    # def calculate_score(self):
    #     # check for collision is a built-in function from the arcade
    #     hit_coin = arcade.check_for_collision_with_list(self.player,
    #                                                     self.coin)  # it might have to be coin list
    #     for coin in hit_coin:
    #         coin.remove_from_sprite_lists()
    #         self.score += 1
