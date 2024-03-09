import arcade


class FlameG(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(filename="Flame/Flame_f00.png", scale=1)
        self.second_to_extuniguish = 2
        self.center_x = x
        self.center_y = y
        self.frame = 0
        self.time = 0

        for i in range(0, 5):
            self.textures.append(arcade.load_texture(f"Flame/Flame_f0{i}.png"))

    def on_update(self, delta_time: float = 1 / 60):
        self.time += delta_time
        if self.time > 0.05:

            self.frame += 1
            if self.frame == 5:
                self.frame = 0
            self.set_texture(self.frame)
            self.time = 0

        self.second_to_extuniguish -= delta_time
        if self.second_to_extuniguish < 0:
            self.kill()
