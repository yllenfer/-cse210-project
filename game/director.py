import arcade
import random
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MOVEMENT_SPEED, NO_MOVEMENT, Y_COUNT, Y_SPACING, \
    Y_START, LIFE_COUNT, LIFE_POSITION_START, LIFE_SPACING, NUM_CARS_PER_ROW
from game.player import Player
from game.score import Score
from game.coin import Coin
from game.car import Car
from game.lives import Lives


class Director(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game_over = False
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()
        self.life_list = arcade.SpriteList()
        # self.game_state = PLAY_GAME
        self.car_collision_sound = arcade.load_sound(":resources:sounds/hit1.wav")
        self.coin_collision_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.coin = None
        self.player = None
        self.score = 0
        self.car = None
        # self.lives = None
        # TODO: Where shall we create the time? Director or another class?
        self.total_time = 0.0
        self.output = "00:00:00"
        self.run_timer = True

    def setup(self):
        self.player = Player()
        self.coin = Coin()
        self.score = Score()
        self.total_time = 0.0
        # self.lives = Lives()
        bottom_cars_velocity = [2, 5, -2, -5]
        middle_cars_velocity = [6, 9, -6, -9]
        for i in range(0, NUM_CARS_PER_ROW):
            self.car_creation(bottom_cars_velocity, Y_START, 250)                                       #(velocity, 100, 250)
            self.car_creation((middle_cars_velocity), (Y_START + 250), 500)                             #(velocity, 350, 500)


        self.life_creation()
        self.points_earned_reaching_top()

        self.player_list.append(self.player)
        self.coin_list.append(self.coin)
        # self.life_list.append(self.lives)
        # self.score = Score()

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
        self.coin_list.draw()
        self.car_list.draw()
        self.life_list.draw()
        # self.draw_timer()
        arcade.draw_text(self.output,
                         45, 30,
                         arcade.color.WHITE, 12,
                         anchor_x="center")

        gameOver = f"Game Over"
        if self.game_over:
            arcade.draw_text(gameOver, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                             arcade.color.RED, 100,
                             anchor_x="center")

    def on_update(self, delta_time):
        if not self.game_over:

            self.player_list.update()
            self.coin_list.update()
            self.car_list.update()
            self.life_list.update()
            self.points_earned_reaching_top()

            coin_collision_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
            for coin in coin_collision_list:
                self.coin_list.remove(coin)
                # coin.remove_from_sprite_lists()
                self.coin_collision_sound.play()
                # TODO: We need to verify why a life needs to be lost in order to earn one
                life = Lives(LIFE_SPACING * (len(self.life_list) + 1))
                self.life_list.append(life)
                # if self.game_state == GAME_OVER:
                #     return

            if arcade.check_for_collision_with_list(self.player, self.car_list):
                self.player.center_y = 0
                self.car_collision_sound.play()
                if self.life_list:
                    self.life_list.pop()
                else:
                    # TODO: Work on game over
                    self.game_over = True
                    print("Game Over")
                    self.player_list.remove(self.player)

            # TODO: Work on timer and score  so it increases number of points
            # TODO: Track time to determine the number of points

            if self.run_timer:
                self.total_time += delta_time
                minutes = int(self.total_time) // 60
                seconds = int(self.total_time) % 60
                seconds_100s = int((self.total_time - seconds) * 100)
                self.output = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

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

    def car_creation(self, velocity, start, stop):
        for y in range(start, (stop + 1), Y_SPACING):
            self.car = Car(y, (random.choice(velocity)))
            self.car_list.append(self.car)

    def life_creation(self):
        for x in range(LIFE_POSITION_START, (LIFE_SPACING * LIFE_COUNT), LIFE_SPACING):
            life = Lives(x)
            self.life_list.append(life)

    def points_earned_reaching_top(self):

        # Track of time, we need to bring back the already track time from the on_update function
        # We need to set a number of points according to seconds
        # Set a number of points per tracked time. AKA if sec < xxx we get xxx score and so on
        # Once player reached the top we display the score
        if self.player.center_y == SCREEN_HEIGHT - 100:
            self.run_timer = False
            # self.output.pause()
