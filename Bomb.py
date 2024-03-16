import arcade

from flame import FlameG


class BombG(arcade.Sprite):

    def __init__(self, x, y, flamelist: arcade.SpriteList, flame_size, radius):
        super().__init__(filename="Bomb/Bomb_f00.png", scale=1)
        self.center_x = x
        self.center_y = y
        self.flame_size = flame_size
        self.second_to_explode = 5
        self.frame = 0
        self.time = 0
        self.flamelist = flamelist
        self.radius = radius

        for i in range(0, 3):
            self.textures.append(arcade.load_texture(f"Bomb/Bomb_f0{i}.png"))

    def on_update(self, delta_time: float = 1 / 60):
        self.time += delta_time
        if self.time > 0.05:

            self.frame += 1
            if self.frame == 3:
                self.frame = 0
            self.set_texture(self.frame)
            self.time = 0

        self.second_to_explode -= delta_time
        if self.second_to_explode < 0:
            self.explode()

    def explode(self):
        flame = FlameG(self.center_x, self.center_y)
        self.flamelist.append(flame)

        for i in range(self.radius):
            self.flamelist.append(
                FlameG(self.center_x + self.flame_size * i, self.center_y)
            )
            self.flamelist.append(
                FlameG(self.center_x - self.flame_size * i, self.center_y)
            )
            self.flamelist.append(
                FlameG(self.center_x , self.center_y + self.flame_size * i)
            )
            self.flamelist.append(
                FlameG(self.center_x , self.center_y - self.flame_size * i)
            )
        self.kill()
