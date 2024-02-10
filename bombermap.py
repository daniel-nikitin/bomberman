import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'bomberman(work in progress)'


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bomberman = Bomberman(100, 100)

    def on_draw(self):
        self.clear()
        self.bomberman.draw()

    def on_key_press(self, symbol: int, modifiers: int):

        if symbol == arcade.key.W:
            self.bomberman.go_back()

        if symbol == arcade.key.A:
            self.bomberman.go_left()

        if symbol == arcade.key.S:
            self.bomberman.go_front()

        if symbol == arcade.key.D:
            self.bomberman.go_right()

    def on_key_release(self, symbol: int, modifiers: int):
        self.bomberman.stop()

    def update(self, delta_time: float):

        if self.bomberman.left < 0 and self.bomberman.navigation == 4:
            self.bomberman.stop()

        if self.bomberman.right > self.width and self.bomberman.navigation == 2:
            self.bomberman.stop()

        if self.bomberman.top > self.height and self.bomberman.navigation == 1:
            self.bomberman.stop()

        if self.bomberman.bottom < 0 and self.bomberman.navigation == 3:
            self.bomberman.stop()

        self.bomberman.oopdate(delta_time)


class Bomberman(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(filename="Bomberman/Front/Bman_F_f00.png", scale=1)
        self.center_y = y
        self.center_x = x
        self.pose = 0
        self.time = 0
        self.moving = False
        self.Left_poses_list = []
        self.Right_poses_list = []
        self.Front_poses_list = []
        self.Back_poses_list = []
        for i in range(0, 8):
            self.Front_poses_list.append(arcade.load_texture(f"Bomberman/Front/Bman_F_f0{i}.png"))
            self.Back_poses_list.append(arcade.load_texture(f"Bomberman/Back/Bman_B_f0{i}.png"))
            self.Right_poses_list.append(arcade.load_texture(f"Bomberman/Side/Bman_S_f0{i}.png"))
            self.Left_poses_list.append(
                arcade.load_texture(f"Bomberman/Side/Bman_S_f0{i}.png", flipped_horizontally=True))
        self.navigation = 3
        self.costume_switch()

    def costume_switch(self):
        if self.navigation == 1:
            self.textures = self.Back_poses_list
        if self.navigation == 2:
            self.textures = self.Right_poses_list
        if self.navigation == 3:
            self.textures = self.Front_poses_list
        if self.navigation == 4:
            self.textures = self.Left_poses_list
        self.set_texture(self.pose)

    def oopdate(self, delta_time: float):

        if self.moving:
            self.time += delta_time
            if self.time > 0.05:

                self.pose += 1
                if self.pose == 8:
                    self.pose = 0
                self.set_texture(self.pose)
                self.time = 0

            speed = 2
            if self.navigation == 1:
                self.center_y = self.center_y + speed

            if self.navigation == 3:
                self.center_y = self.center_y - speed

            if self.navigation == 2:
                self.center_x = self.center_x + speed

            if self.navigation == 4:
                self.center_x = self.center_x - speed

    def go_back(self):
        self.navigation = 1
        self.move()

    def go_right(self):
        self.navigation = 2
        self.move()

    def go_front(self):
        self.navigation = 3
        self.move()

    def go_left(self):
        self.navigation = 4
        self.move()

    def move(self):
        self.moving = True
        self.costume_switch()

    def stop(self):
        self.moving = False


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
