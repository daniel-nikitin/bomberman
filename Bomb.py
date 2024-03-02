import arcade


class Bomb(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(filename="Bomb/Bomb_f00.png", scale=1)
