import arcade


class FlameG(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(filename="Flame/Flame_f00.png", scale=1)
        self.center_x = x
        self.center_y = y

