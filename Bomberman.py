import arcade

from Bomb import BombG
from Powerup import Powerup, PowerupType


class Bomberman(arcade.Sprite):

    def __init__(self, x, y, color, number):
        super().__init__(filename="Bomberman/Front/Bman_F_f00.png", scale=1)
        self.number = number
        self.set_hit_box(((-24.0, -49.0), (-15.0, -58.0), (15.0, -58.0), (24.0, -49.0), (24.0, -20), (15.0, -11), (-15.0, -11), (-24.0, -20)))
        self.center_y = y
        self.center_x = x

        self.speed = 2
        self.bomb_disable = 10
        self.radius = 3

        self.color = color
        self.pose = 0
        self.time = 0

        self.cooldown = 0
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

        self.cooldown  -= delta_time
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

    def pick_up_powerup(self, powerup: Powerup):
        if powerup.type == PowerupType.SPEED:
            self.speed += 2
        if powerup.type == PowerupType.BOMB:
            self.bomb_disable -= 2
        if powerup.type == PowerupType.FLAME:
            self.radius += 1

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

    def place_bomb(self, create_bomb):
        if self.cooldown > 0:
            return

        create_bomb(
            self.center_x, self.center_y,self.radius
        )


        self.cooldown = self.bomb_disable
