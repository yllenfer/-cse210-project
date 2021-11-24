import arcade
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MOVEMENT_SPEED, NO_MOVEMENT, Y_COUNT, Y_SPACING, Y_START
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
        self.car_list = arcade.SpriteList()
        self.coin = None
        self.player = None
        self.score = 0
        self.car = None

    def setup(self):
        self.player = Player()
        self.coin = Coin()

        self.car_creation()
        
        self.player_list.append(self.player)
        self.coin_list.append(self.coin) 
        self.score = Score()

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.coin_list.draw()
        self.car_list.draw()

    def on_update(self, delta_time):
        self.player_list.update()
        self.coin_list.update()
        self.car_list.update()
        coin_collision_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coin_collision_list:
            coin.remove_from_sprite_lists()
            # self.score += 1
        if arcade.check_for_collision_with_list(self.player, self.car_list):
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

    def car_creation(self):

        for y in range(Y_START, (Y_SPACING * Y_COUNT), Y_SPACING):
            self.car = Car(y)
            self.car_list.append(self.car)