import arcade


class Solid(arcade.Sprite):

    def __init__(self):
        super().__init__(filename="Blocks/SolidBlock.png", scale=1)
