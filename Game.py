import arcade

from Bomb import BombG
from Bomberman import Bomberman
from Solid import Solid

ROWS = 11
COLUMNS = 11
TILE_SIZE = 65



class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bomberman1 = Bomberman(width / 2, height / 2, 2.5, (0, 255, 24))
        self.bomberman2 = Bomberman(0, 0, 1.5, (255, 0, 24))
        self.bg = arcade.load_texture('Blocks/BackgroundTile.png')
        self.solidlist = arcade.SpriteList()
        self.bomblist = arcade.SpriteList()
        self.flamelist = arcade.SpriteList()
        self.bombermen = arcade.SpriteList()
        # self.bombermen.append(Bomberman(width / 2, height / 2, P1_SPEED))
        self.create_solidB()

    def on_draw(self):
        self.clear()
        self.draw_bg()
        self.solidlist.draw()
        self.bomberman1.draw()
        self.bomberman2.draw()
        self.bomblist.draw()
        self.flamelist.draw()

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
            self.bomberman1.go_back()

        if symbol == arcade.key.A:
            self.bomberman1.go_left()

        if symbol == arcade.key.S:
            self.bomberman1.go_front()

        if symbol == arcade.key.D:
            self.bomberman1.go_right()

        if symbol == arcade.key.Q:
            self.bomberman1.place_bomb(self.bomblist, self.flamelist)



        if symbol == arcade.key.UP:
            self.bomberman2.go_back()

        if symbol == arcade.key.LEFT:
            self.bomberman2.go_left()

        if symbol == arcade.key.DOWN:
            self.bomberman2.go_front()

        if symbol == arcade.key.RIGHT:
            self.bomberman2.go_right()

        if symbol == arcade.key.RCTRL:
            self.bomberman2.place_bomb(self.bomblist, self.flamelist)


    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.A or symbol == arcade.key.D or symbol == arcade.key.W or symbol == arcade.key.S:
            self.bomberman1.stop()
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT or symbol == arcade.key.UP or symbol == arcade.key.DOWN:
            self.bomberman2.stop()

    def update(self, delta_time: float):

        self.bomblist.on_update(delta_time)
        self.flamelist.on_update(delta_time)

        list = [self.bomberman1, self.bomberman2]
        for i in list:

            if i.left < 0 and i.navigation == 4:
                i.stop()

            if i.right > self.width and i.navigation == 2:
                i.stop()

            if i.top > self.height and i.navigation == 1:
                i.stop()

            if i.bottom < 0 and i.navigation == 3:
                i.stop()

            solids = arcade.check_for_collision_with_list(i, self.solidlist)
            if len(solids) > 0:
                for block in solids:

                    if i.left < block.right < i.right and i.navigation == 4:
                        i.stop()
                        # self.bomberman.left = block.right

                    if i.left < block.left < i.right and i.navigation == 2:
                        i.stop()

                    if i.bottom < block.bottom < i.top and i.navigation == 1:
                        i.stop()

                    if i.bottom < block.top < i.top and i.navigation == 3:
                        i.stop()
                # arcade.colli
                # self.bomberman.stop()

            i.oopdate(delta_time)
