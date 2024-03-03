import arcade


class BombG(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(filename="Bomb/Bomb_f00.png", scale=1)
        self.center_x = x
        self.center_y = y
        self.second_to_explode = 5

    def on_update(self, delta_time: float = 1 / 60):
        self.second_to_explode -= delta_time
        if self.second_to_explode < 0:
            self.kill()
