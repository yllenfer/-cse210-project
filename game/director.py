import arcade
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MOVEMENT_SPEED, NO_MOVEMENT
from game.player import Player
from game.score import Score
from game.coin import Coin
from game.car import Car


class Director(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.cart_list = arcade.SpriteList()
        self.coin = None
        self.player = None
        self.score = 0
        self.car = None

    def setup(self):
        self.player = Player()
        self.coin = Coin()
        self.car = Car()
        self.player_list.append(self.player)
        self.coin_list.append(self.coin)
        self.cart_list.append(self.car)
        self.score = Score()

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.coin_list.draw()
        self.cart_list.draw()

    def on_update(self, delta_time):
        self.player_list.update()
        self.coin_list.update()
        self.cart_list.update()
        coin_collision_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coin_collision_list:
            coin.remove_from_sprite_lists()
            # self.score += 1
        if arcade.check_for_collision_with_list(self.player, self.cart_list):
            self.player.center_y = 0

    def on_key_press(self, key, modifiers):

        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED

        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED

        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED

        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):

        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player.change_y = NO_MOVEMENT

        elif key == arcade.key.DOWN:
            self.player.change_y = NO_MOVEMENT

        elif key == arcade.key.LEFT:
            self.player.change_x = NO_MOVEMENT

        elif key == arcade.key.RIGHT:
            self.player.change_x = NO_MOVEMENT
