from math import pi
import arcade
import random
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MOVEMENT_SPEED, NO_MOVEMENT, Y_COUNT, Y_SPACING, \
    Y_START, LIFE_COUNT, LIFE_POSITION_START, LIFE_SPACING, NUM_CARS_PER_ROW, PICTURES_PATH, MINIMUM_TIME
from game.player import Player
from game.score import Score
from game.coin import Coin
from game.car import Car
from game.lives import Lives
import os


class Director(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game_over = False
        self.winner = False
        self.background = None
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()
        self.life_list = arcade.SpriteList()
        # self.game_state = PLAY_GAME
        self.car_collision_sound = arcade.load_sound(":resources:sounds/hit1.wav")
        self.coin_collision_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.upgrade = arcade.load_sound(":resources:sounds/upgrade1.wav")
        self.coin = None
        self.player = None
        self.score = 1.0
        self.car = None
        # self.lives = None
        self.total_time = 0.0
        self.output = "00:00:00"
        self.run_timer = True
        self.level = 1

    def setup(self):
        self.level_one()
        # Important: the setup performance has been moved to the levels

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                      self.background)
        self.player_list.draw()
        self.coin_list.draw()
        self.car_list.draw()
        self.life_list.draw()
        # self.points_earned_reaching_top()
        arcade.draw_text(self.output,
                         45, 30,
                         arcade.color.WHITE, 12,
                         anchor_x="center")

        gameOver = f"Game Over"
        if self.game_over:
            arcade.draw_text(gameOver, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                             arcade.color.RED, 100,
                             anchor_x="center")
            minutes = int(self.total_time) // 60
            seconds = int(self.total_time) % 60
            seconds_100s = int((self.total_time - seconds) * 100)
            # score = f"{round(self.score * self.total_time * 1000)}"
            # TODO: Display score once player has lost or moved to the final level score needs to be recalculated
            # final_score = f"Final Score:{score}"
            # arcade.draw_text(final_score, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, arcade.color.WHITE, 15,
            #                  anchor_x="center")
        elif self.winner:
            # TODO: Work on winning scenario
            winner = f"You have won"
            # if self.winner:
            arcade.draw_text(winner, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                             arcade.color.RED, 100,
                             anchor_x="center")
            self.run_timer = False
            minutes = int(self.total_time) // 60
            seconds = int(self.total_time) % 60
            seconds_100s = int((self.total_time - seconds) * 100)
            score = f"{round(MINIMUM_TIME / self.total_time * 10000)}"
            final_score = f"Final Score:{score}"
            arcade.draw_text(final_score, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, arcade.color.WHITE, 15,
                             anchor_x="center")
            # self.game_over = True

    def on_update(self, delta_time):
        if not self.game_over or self.winner:

            self.player_list.update()
            self.coin_list.update()
            self.car_list.update()
            self.life_list.update()
            # self.points_earned_reaching_top()

            coin_collision_list = arcade.check_for_collision_with_list(self.player, self.coin_list)
            for coin in coin_collision_list:
                self.coin_list.remove(coin)
                # coin.remove_from_sprite_lists()
                self.coin_collision_sound.play()

                life = Lives(LIFE_SPACING * (len(self.life_list) + 1))
                self.life_list.append(life)

            if arcade.check_for_collision_with_list(self.player, self.car_list):
                self.player.center_y = 0
                self.car_collision_sound.play()

                if self.life_list:
                    self.life_list.pop()
                else:
                    self.game_over = True
                    print("Game Over")
                    self.player_list.remove(self.player)

            if self.run_timer == True:
                self.total_time += delta_time
                minutes = int(self.total_time) // 60
                seconds = int(self.total_time) % 60
                seconds_100s = int((self.total_time - seconds) * 100)
                self.output = f"{minutes:02d}:{seconds:02d}:{seconds_100s:02d}"

            if self.player.center_y > SCREEN_HEIGHT - 50 and self.level == 1:
                self.level += 1
                self.player_list.pop()
                # self.coin_list.pop()
                self.car_list = arcade.SpriteList()
                self.level_two()
            elif self.player.center_y > SCREEN_HEIGHT - 50 and self.level == 2:
                self.level += 1
                self.coin_list.pop()
                self.car_list = arcade.SpriteList()
                self.level_three()
                # self.game_over
            elif self.player.center_y > SCREEN_HEIGHT - 50 and self.level == 3:
                # TODO: We need to display something nice for winner
                # self.game_over = True
                self.winner = True


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
            car = Car(y, (random.choice(velocity)))
            self.car_list.append(car)

    def life_creation(self):
        for x in range(LIFE_POSITION_START, (LIFE_SPACING * LIFE_COUNT), LIFE_SPACING):
            life = Lives(x)
            self.life_list.append(life)


    def level_one(self):
        self.background = arcade.load_texture(PICTURES_PATH + "Frogger background.PNG")
        print("Level one")
        self.player = Player()
        self.coin = Coin()
        # self.score = Score()
        self.total_time = 0.0
        # self.lives = Lives()
        bottom_cars_velocity = [2, 3, -2, -3]
        middle_cars_velocity = [5, 6, -4, -6]
        for i in range(0, NUM_CARS_PER_ROW):
            self.car_creation(bottom_cars_velocity, Y_START, 250)  # (velocity, 100, 250)
            self.car_creation(middle_cars_velocity, (Y_START + 250), 500)  # (velocity, 350, 500)

        self.life_creation()
        # self.points_earned_reaching_top()

        self.player_list.append(self.player)
        self.coin_list.append(self.coin)

    def level_two(self):
        self.background = arcade.load_texture(PICTURES_PATH + "Frogger background.PNG")
        self.player = Player()
        print("Level two")
        self.coin = Coin()
        bottom_cars_velocity = [4, 6, -4, -6]
        middle_cars_velocity = [5, 6, -5, -6]
        for i in range(0, NUM_CARS_PER_ROW):
            self.car_creation(bottom_cars_velocity, Y_START, 250)  # (velocity, 100, 250)
            self.car_creation(middle_cars_velocity, (Y_START + 250), 500)  # (velocity, 350, 500)

        self.life_creation()
        # self.points_earned_reaching_top()

        self.player_list.append(self.player)
        self.coin_list.append(self.coin)
        # TODO: Display time accumulation
        # self.run_timer = True

    def level_three(self):
        self.background = arcade.load_texture(PICTURES_PATH + "Frogger background.PNG")
        print("Level three")
        self.player = Player()
        self.coin = Coin()
        bottom_cars_velocity = [5, 6, -5, -6]
        middle_cars_velocity = [2, 2, -10, -12]
        for i in range(0, NUM_CARS_PER_ROW):
            self.car_creation(bottom_cars_velocity, Y_START, 250)  # (velocity, 100, 250)
            self.car_creation(middle_cars_velocity, (Y_START + 250), 500)  # (velocity, 350, 500)

        # self.life_creation()
        # self.points_earned_reaching_top()
        # TODO: Display time accumulation
        self.player_list.append(self.player)
        self.coin_list.append(self.coin)
