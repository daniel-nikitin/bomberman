from enum import Enum

import arcade


class PowerupType(Enum):
    BOMB = 1
    FLAME = 2
    SPEED = 3

class Powerup(arcade.Sprite):

    def __init__(self, powerup_type: PowerupType):
        self.type = powerup_type
        if powerup_type == PowerupType.BOMB:
            picture = "BombPowerup"

        if powerup_type == PowerupType.FLAME:
            picture = "FlamePowerup"

        if powerup_type == PowerupType.SPEED:
            picture = "SpeedPowerup"
        super().__init__(filename=f"Powerups/{picture}.png", scale=1)
