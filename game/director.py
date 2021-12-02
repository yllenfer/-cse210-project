import arcade
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MOVEMENT_SPEED, NO_MOVEMENT
from game.player import Player
from game.score import Score
from game.coin import Coin


class Director(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game_over = False
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.coin = None
        self.player = None
        self.score = None

    def setup(self):
        self.player = Player()
        self.coin = Coin()
        self.player_list.append(self.player)
        self.coin_list.append(self.coin)
        # self.score = Score()
        

        output = (f"Score: {self.score}")
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.coin_list.draw()

    def on_update(self, delta_time):
        self.player_list.update()
        self.coin_list.update()
        collision_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in collision_list:
            coin.remove_from_sprite_lists()
            # self.score += 1

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
