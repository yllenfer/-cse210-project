import arcade
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from game.player import Player
from game.score import Score


class Director(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.player = Player()
        self.score = Score()

    def start_game(self):
        self.player.create_player()
        arcade.run()

    def on_draw(self):
        arcade.start_render()
        # self.score.calculate_score()
        self.player.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)


