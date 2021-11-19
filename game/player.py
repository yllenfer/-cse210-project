import arcade
from game.constants import SPRITE_SCALING
class Player:
    
    def __init__(self):
        self.player = None

    def create_player(self):
        self.player = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png", SPRITE_SCALING)