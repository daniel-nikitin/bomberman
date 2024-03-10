import random

import arcade

from Bomb import BombG
from Bomberman import Bomberman
from Solid import Solid
from expblock import Expblock

ROWS = 11
COLUMNS = 17
TILE_SIZE = 65



class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bomberman1 = Bomberman(width / 2, height / 2, 2.5, (0, 255, 24), TILE_SIZE)
        self.bomberman2 = Bomberman(0, 0, 1.5, (255, 0, 24), TILE_SIZE)
        self.bg = arcade.load_texture('Blocks/BackgroundTile.png')
        self.solidlist = arcade.SpriteList()
        self.explist = arcade.SpriteList()
        self.bomblist = arcade.SpriteList()
        self.flamelist = arcade.SpriteList()
        self.bombermen = arcade.SpriteList()
        # self.bombermen.append(Bomberman(width / 2, height / 2, P1_SPEED))
        self.create_solidB()
        self.create_expB()

    def on_draw(self):
        self.clear()
        self.draw_bg()
        self.solidlist.draw()
        self.explist.draw()
        self.bomberman1.draw()
        #self.bomberman1.draw_hit_box()
        self.bomberman2.draw()
        self.bomblist.draw()
        self.flamelist.draw()

    def create_solidB(self):
        for y in range(ROWS):
            for x in range(COLUMNS):
                if x % 2 == 1 and y % 2 == 1:
                    block = Solid()
                    block.center_x = TILE_SIZE * x + TILE_SIZE / 2
                    block.center_y = TILE_SIZE * y + TILE_SIZE / 2
                    self.solidlist.append(block)

    def create_expB(self):
        for y in range(ROWS):
            for x in range(COLUMNS):
                if not (x % 2 == 1 and y % 2 == 1):
                    if random.randint(1, 5) == 1:
                        block = Expblock()
                        block.center_x = TILE_SIZE * x + TILE_SIZE / 2
                        block.center_y = TILE_SIZE * y + TILE_SIZE / 2
                        self.explist.append(block)

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

        bombermen = [self.bomberman1, self.bomberman2]
        for bomberman in bombermen:

            if bomberman.left < 0 and bomberman.navigation == 4:
                bomberman.stop()

            if bomberman.right > self.width and bomberman.navigation == 2:
                bomberman.stop()

            if bomberman.top > self.height and bomberman.navigation == 1:
                bomberman.stop()

            if bomberman.bottom < 0 and bomberman.navigation == 3:
                bomberman.stop()

            self.check_colliuson(self.solidlist, bomberman)
            self.check_colliuson(self.explist, bomberman)

            bomberman.oopdate(delta_time)

    def check_colliuson(self, spritelist, bomberman):

        blocks = arcade.check_for_collision_with_list(bomberman, spritelist)
        if len(blocks) > 0:
            for block in blocks:

                if bomberman.left < block.right < bomberman.right and bomberman.navigation == 4:
                    bomberman.stop()
                    # self.bomberman.left = block.right

                if bomberman.left < block.left < bomberman.right and bomberman.navigation == 2:
                    bomberman.stop()

                if bomberman.bottom < block.bottom < bomberman.top and bomberman.navigation == 1:
                    bomberman.stop()

                if bomberman.bottom < block.top < bomberman.top and bomberman.navigation == 3:
                    bomberman.stop()
            # arcade.colli
            # self.bomberman.stop()

