import random

import arcade

from Bomb import BombG
from Bomberman import Bomberman
from Powerup import Powerup, PowerupType
from Solid import Solid
from expblock import Expblock
from flame import FlameG

ROWS = 11
COLUMNS = 17
TILE_SIZE = 65


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.bomberman1 = Bomberman(width / 2, height / 2, (0, 255, 24), 2)
        self.bomberman2 = Bomberman(0, 0, (255, 0, 24), 1)
        self.bg = arcade.load_texture('Blocks/BackgroundTile.png')
        self.pause = False
        self.Gover_image = arcade.load_texture("win/win1.png")
        self.Gover_image2 = arcade.load_texture("win/win2.png")
        self.stategame = True
        self.winner = -1
        self.solidlist = arcade.SpriteList()
        self.explist = arcade.SpriteList()
        self.bomblist = arcade.SpriteList()
        self.flamelist = arcade.SpriteList()
        self.bombermen = arcade.SpriteList()
        self.powerups = arcade.SpriteList()

        self.create_solidB()
        self.create_expB()

    def on_draw(self):

        self.clear()
        self.draw_bg()
        self.solidlist.draw()
        self.powerups.draw()
        self.explist.draw()
        self.bomberman1.draw()
        # self.bomberman1.draw_hit_box()
        self.bomberman2.draw()
        self.bomblist.draw()
        self.flamelist.draw()

        if self.stategame == False:
            if self.winner == 1:
                image = self.Gover_image
            else:
                image = self.Gover_image2

            arcade.draw_texture_rectangle(
                TILE_SIZE * COLUMNS / 2,
                TILE_SIZE * ROWS / 2,
                self.Gover_image.width,
                self.Gover_image.height,
                image

            )

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
                        self.maybe_place_powerup(block.center_x, block.center_y)

    def maybe_place_powerup(self, x, y):
        if random.randint(1, 2) == 1:
            powerup_type = random.choice(list(PowerupType))

            powerup = Powerup(powerup_type)
            powerup.center_x = x
            powerup.center_y = y

            self.powerups.append(powerup)

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

        if self.stategame == False:
            return

        if symbol == arcade.key.W:
            self.bomberman1.go_back()

        if symbol == arcade.key.A:
            self.bomberman1.go_left()

        if symbol == arcade.key.S:
            self.bomberman1.go_front()

        if symbol == arcade.key.D:
            self.bomberman1.go_right()

        if symbol == arcade.key.Q:
            self.bomberman1.place_bomb(self.create_bomb)

        if symbol == arcade.key.UP:
            self.bomberman2.go_back()

        if symbol == arcade.key.LEFT:
            self.bomberman2.go_left()

        if symbol == arcade.key.DOWN:
            self.bomberman2.go_front()

        if symbol == arcade.key.RIGHT:
            self.bomberman2.go_right()

        if symbol == arcade.key.RCTRL:
            self.bomberman2.place_bomb(self.create_bomb)

    def create_bomb(self, x, y, radius):
        bomb = BombG(
            (x / TILE_SIZE).__floor__() * TILE_SIZE + TILE_SIZE / 2,
            (y / TILE_SIZE).__round__() * TILE_SIZE - TILE_SIZE / 2,
            radius,
            self.explode
        )
        self.bomblist.append(bomb)

    def explode(self, x, y, radius):

        right_collision = False
        left_collision = False
        front_collision = False
        back_collision = False

        for i in range(radius):
            right_flame = FlameG(x + TILE_SIZE * i, y)
            if self.check_flame_with_solid_collision(right_flame):
                right_collision = True
            if not right_collision:
                self.flamelist.append(right_flame)
                if self.check_flame_with_exp_collision(right_flame):
                    right_collision = True

            left_flame = FlameG(x - TILE_SIZE * i, y)
            if self.check_flame_with_solid_collision(left_flame):
                left_collision = True
            if not left_collision:
                self.flamelist.append(left_flame)
                if self.check_flame_with_exp_collision(left_flame):
                    left_collision = True

            front_flame = FlameG(x, y - TILE_SIZE * i)
            if self.check_flame_with_solid_collision(front_flame):
                front_collision = True
            if not front_collision:
                self.flamelist.append(front_flame)
                if self.check_flame_with_exp_collision(front_flame):
                    front_collision = True

            back_flame = FlameG(x, y + TILE_SIZE * i)
            if self.check_flame_with_solid_collision(back_flame):
                back_collision = True
            if not back_collision:
                self.flamelist.append(back_flame)
                if self.check_flame_with_exp_collision(back_flame):
                    back_collision = True

            # self.flamelist.append(
            #     FlameG(x - TILE_SIZE * i, y)
            # )
            # self.flamelist.append(
            #     FlameG(x, y + TILE_SIZE * i)
            # )
            # self.flamelist.append(
            #     FlameG(x, y - TILE_SIZE * i)
            # )

    def check_flame_with_solid_collision(self, flame):
        return len(arcade.check_for_collision_with_list(flame, self.solidlist)) > 0

    def check_flame_with_exp_collision(self, flame):
        return len(arcade.check_for_collision_with_list(flame, self.explist)) > 0

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.A or symbol == arcade.key.D or symbol == arcade.key.W or symbol == arcade.key.S:
            self.bomberman1.stop()
        if symbol == arcade.key.LEFT or symbol == arcade.key.RIGHT or symbol == arcade.key.UP or symbol == arcade.key.DOWN:
            self.bomberman2.stop()

    def update(self, delta_time: float):

        if self.stategame == False:
            return

        self.bomblist.on_update(delta_time)
        self.flamelist.on_update(delta_time)

        self.check_flame_collision()
        self.check_collision(self.bomberman1)
        self.check_collision(self.bomberman2)

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

            self.check_bomberman_collision(self.solidlist, bomberman)
            self.check_bomberman_collision(self.explist, bomberman)

            powerups = arcade.check_for_collision_with_list(bomberman, self.powerups)
            for powerup in powerups:
                bomberman.pick_up_powerup(powerup)
                powerup.kill()

            bomberman.oopdate(delta_time)

    def check_flame_collision(self):
        for expblock in self.explist:
            flames = arcade.check_for_collision_with_list(expblock, self.flamelist)
            if len(flames) > 0:
                expblock.kill()

    def check_bomberman_collision(self, spritelist, bomberman):

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

    def check_collision(self, bomberman:Bomberman):

        check = arcade.check_for_collision_with_list(bomberman, self.flamelist)
        # check = arcade.check_for_collision_with_list(self.bomberman2, self.flamelist)
        if len(check) > 0:
            self.stategame = False
            self.winner = bomberman.number
