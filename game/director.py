import arcade
import random
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, MOVEMENT_SPEED, NO_MOVEMENT, Y_COUNT, Y_SPACING, \
    Y_START, LIFE_COUNT, LIFE_POSITION_START, LIFE_SPACING, NUM_CARS_PER_ROW, PICTURES_PATH, MINIMUM_TIME
from game.player import Player
from game.coin import Coin
from game.car import Car
from game.lives import Lives

class Director(arcade.Window):
    """A code template for a person who directs the game. The responsibility of 
    this class of objects is to control the sequence of play.

    Stereotype: 
        Controller

    Attributes:
        self.game_over(False)
        self.winner(False)
        self.player_list: the arcade sprite list used for the players
        self.coin_list: the arcade sprite list used for the coins
        self.car_list: the arcade sprite list used for the cars
        self.life_list: the arcade sprite list used for the lives
        self.car_collision_sound: the sound asset used for the collision between the cars and the player
        self.coin_collision_sound: the sound asset used for the collision between the coin and the player
        self.next_level_sound: the sound asset used when the player advances to the next level.
        self.coin: an instance of coin
        self.player: an instance of player
        self.score: players score
        self.car: an instance of car
        self.level: an instance of level
        self.total_time: setting the total time to 0
        self.output: setting the default ouput of the timer to 00:00:00
        self.run_timer(True)
"""
    def __init__(self):
        """
        The class constructor

        args:
            self(director): an instance of director
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.game_over = False
        self.winner = False
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()
        self.life_list = arcade.SpriteList()
        self.car_collision_sound = arcade.load_sound(":resources:sounds/hit1.wav")
        self.coin_collision_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.next_level_sound = arcade.load_sound(":resources:sounds/upgrade1.wav")
        self.coin = None
        self.player = None
        self.score = 0
        self.car = None
        self.level = 1
        self.total_time = 0.0
        self.output = "00:00:00"
        self.run_timer = True

    def setup(self):
        """
        starts to run the game
        """
        self.level_one()
        
    def on_draw(self):
        """
        Will draw important assets and background for game funcionality. 
        """
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT,
                                      self.background)
        self.player_list.draw()
        self.coin_list.draw()
        self.car_list.draw()
        self.life_list.draw()
        arcade.draw_text(self.output,
                         45, 30,
                         arcade.color.WHITE, 12,
                         anchor_x="center")
        gameOver = f"Game Over"

        if self.game_over:
            arcade.draw_text(gameOver, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                             arcade.color.RED, 100,
                             anchor_x="center")
        elif self.winner:
            winner = f"You have won"
            arcade.draw_text(winner, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                             arcade.color.AO, 80,
                             anchor_x="center")
            self.run_timer = False
            final_score = f"Final Score:{self.score}"
            arcade.draw_text(final_score, SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100, arcade.color.WHITE, 25,
                             anchor_x="center")
            

    def on_update(self, delta_time):
        """
        Will update important game information to follow the sequence of the game.

        args: 
            delta_time: keeps track time
        """
        if not self.game_over or self.winner:
            self.player_list.update()
            self.coin_list.update()
            self.car_list.update()
            self.life_list.update()
            coin_collision_list = arcade.check_for_collision_with_list(self.player, self.coin_list)

            for coin in coin_collision_list:
                self.coin_list.remove(coin)
                self.coin_collision_sound.play()
                life = Lives(LIFE_SPACING * (len(self.life_list) + 1))
                self.life_list.append(life)

            if arcade.check_for_collision_with_list(self.player, self.car_list):
                self.player.center_y = 0
                self.score -= 100
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
                self.score = round(MINIMUM_TIME / self.total_time * 10000)

            if self.player.center_y > SCREEN_HEIGHT - 50 and self.level == 1:
                self.level += 1
                self.player_list.pop()
                self.coin_list = arcade.SpriteList()
                self.car_list = arcade.SpriteList()
                self.level_two()
            elif self.player.center_y > SCREEN_HEIGHT - 50 and self.level == 2:
                self.level += 1
                self.coin_list = arcade.SpriteList()
                self.player_list.pop()
                self.car_list = arcade.SpriteList()
                self.level_three()
            elif self.player.center_y > SCREEN_HEIGHT - 50 and self.level == 3:
                self.coin_list = arcade.SpriteList()
                self.car_list = arcade.SpriteList()
                self.winner = True

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed and will move the player speed by the given movement speed constant.

            args: 
                key: checks what key is being pressed on the keyboard
                modifiers: will modify the event given the key press/release
        """

        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called whenever a key is released and will move the player speed by the given movement speed constant.

        args: 
            key: checks what key is being pressed on the keyboard.
            modifiers: will modify the event given the key press/release
        """

        if key == arcade.key.UP:
            self.player.change_y = NO_MOVEMENT
        elif key == arcade.key.DOWN:
            self.player.change_y = NO_MOVEMENT
        elif key == arcade.key.LEFT:
            self.player.change_x = NO_MOVEMENT
        elif key == arcade.key.RIGHT:
            self.player.change_x = NO_MOVEMENT

    def car_creation(self, velocity, start, stop):
        """
        creates a car sprite

        args:
            velocity: the cars speed and direction for the x coordinate.
            start: defines where the cars will start to create on the grid.
            stop: defines where the cars stop being created on the grid.
        """
        for y in range(start, (stop + 1), Y_SPACING):
            car = Car(y, (random.choice(velocity)))
            self.car_list.append(car)

    def life_creation(self):
        """
        creates the list of lives the player has at the start of the game
        """
        for x in range(LIFE_POSITION_START, (LIFE_SPACING * LIFE_COUNT), LIFE_SPACING):
            life = Lives(x)
            self.life_list.append(life)

    def level_one(self):
        """
        set the environment for level 1 of the game
        """
        self.background = arcade.load_texture(PICTURES_PATH + "frogger_background_starting_levels.PNG")
        print("Level one")
        self.player = Player()
        self.coin = Coin()
        self.total_time = 0.0
        bottom_cars_velocity = [2, 3, -2, -3]
        middle_cars_velocity = [5, 6, -4, -6]
        for i in range(0, NUM_CARS_PER_ROW):
            self.car_creation(bottom_cars_velocity, Y_START, 250)           # (velocity, 100, 250)
            self.car_creation(middle_cars_velocity, (Y_START + 250), 500)   # (velocity, 350, 500)
        self.life_creation()
        self.player_list.append(self.player)
        self.coin_list.append(self.coin)

    def level_two(self):
        """
        set the environment for level 2 of the game
        """
        self.background = arcade.load_texture(PICTURES_PATH + "frogger_background_starting_levels.PNG")
        self.player = Player()
        print("Level two")
        self.coin = Coin()
        first_row_velo = [5, 6, -5 -6]
        second_row_velo = [7, 8, -7, -8]
        for i in range(0, NUM_CARS_PER_ROW):
            self.car_creation(first_row_velo, Y_START, 250)           # (velocity, 100, 250)
            self.car_creation(second_row_velo, (Y_START + 250), 500)  # (velocity, 350, 500)
        self.next_level_sound.play()

        self.player_list.append(self.player)
        self.coin_list.append(self.coin)


    def level_three(self):
        """
        set the environment for level 3 of the game
        """
        self.background = arcade.load_texture(PICTURES_PATH + "frogger_background_finish.PNG")
        print("Level three")
        self.player = Player()
        self.coin = Coin()
        bottom_cars_velocity = [7, 8, -7, -8]
        middle_cars_velocity = [9, 10, -9, -10]

        for i in range(0, NUM_CARS_PER_ROW):
            self.car_creation(bottom_cars_velocity, Y_START, 250)          # (velocity, 100, 250)
            self.car_creation(middle_cars_velocity, (Y_START + 250), 500)  # (velocity, 350, 500)

        self.player_list.append(self.player)
        self.coin_list.append(self.coin)
        self.next_level_sound.play()
