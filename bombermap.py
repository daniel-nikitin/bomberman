import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'bomberman(work in progress)'


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bomberman = Bomberman()

    def on_draw(self):
        self.clear()
        self.bomberman.draw()

    def update(self, delta_time: float):
        self.bomberman.oopdate(delta_time)


class Bomberman(arcade.Sprite):
    pose = 0
    time = 0

    def __init__(self):
        super().__init__(filename="Bomberman/Front/Bman_F_f00.png", scale=1)
        self.center_y = SCREEN_HEIGHT / 2
        self.center_x = SCREEN_WIDTH / 2
        for i in range(1, 8):
            self.append_texture(arcade.load_texture(f"Bomberman/Front/Bman_F_f0{i}.png"))

    def oopdate(self, delta_time: float):

        self.time += delta_time
        if self.time > 0.05:

            self.pose += 1
            if self.pose == 8:
                self.pose = 0
            self.set_texture(self.pose)
            self.time = 0


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
