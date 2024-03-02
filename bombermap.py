import arcade

ROWS = 9
COLUMNS = 15
TILE_SIZE = 90
SCREEN_TITLE = 'bomberman(work in progress)'
P1_SPEED = 2.5
P2_SPEED = 2.5


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bomberman = Bomberman(width / 2, height / 2, P1_SPEED)
        self.bg = arcade.load_texture('Blocks/BackgroundTile.png')
        self.solidlist = arcade.SpriteList()
        # self.bomberman = arcade.SpriteList
        self.create_solidB()

    def on_draw(self):
        self.clear()
        self.draw_bg()
        self.solidlist.draw()
        self.bomberman.draw()
        self.bomberman.draw_hit_box()

    def create_solidB(self):
        for y in range(10):
            for x in range(15):
                if x % 2 == 1 and y % 2 == 1:
                    block = Solid()
                    block.center_x = TILE_SIZE * x + TILE_SIZE / 2
                    block.center_y = TILE_SIZE * y + TILE_SIZE / 2
                    self.solidlist.append(block)

    def draw_bg(self):
        for y in range(ROWS):
            for x in range(COLUMNS):
                arcade.draw_texture_rectangle(
                    center_x=TILE_SIZE * x + TILE_SIZE / 2,
                    center_y=TILE_SIZE * y + TILE_SIZE / 2,
                    width=TILE_SIZE,
                    height=TILE_SIZE,
                    texture=self.bg
                )

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

        solids = arcade.check_for_collision_with_list(self.bomberman, self.solidlist)
        if len(solids) > 0:
            for block in solids:

                if self.bomberman.left < block.right < self.bomberman.right and self.bomberman.navigation == 4:
                    self.bomberman.stop()
                    # self.bomberman.left = block.right

                if self.bomberman.left < block.left < self.bomberman.right and self.bomberman.navigation == 2:
                    self.bomberman.stop()

                if self.bomberman.bottom < block.bottom < self.bomberman.top and self.bomberman.navigation == 1:
                    self.bomberman.stop()

                if self.bomberman.bottom < block.top < self.bomberman.top and self.bomberman.navigation == 3:
                    self.bomberman.stop()
            # arcade.colli
            # self.bomberman.stop()

        self.bomberman.oopdate(delta_time)


class Bomberman(arcade.Sprite):

    def __init__(self, x, y, s):
        super().__init__(filename="Bomberman/Front/Bman_F_f00.png", scale=1)
        self.center_y = y
        self.center_x = x
        self.speed = s
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

            if self.navigation == 1:
                self.center_y = self.center_y + self.speed

            if self.navigation == 3:
                self.center_y = self.center_y - self.speed

            if self.navigation == 2:
                self.center_x = self.center_x + self.speed

            if self.navigation == 4:
                self.center_x = self.center_x - self.speed

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


class Bomb(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__(filename="Bomb/Bomb_f00.png", scale=1)


class Solid(arcade.Sprite):

    def __init__(self):
        super().__init__(filename="Blocks/SolidBlock.png", scale=1)


window = Game(
    TILE_SIZE * COLUMNS,
    TILE_SIZE * ROWS,
    SCREEN_TITLE)
arcade.run()
