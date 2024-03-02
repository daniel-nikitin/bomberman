import arcade

from Game import Game, TILE_SIZE, COLUMNS, ROWS

SCREEN_TITLE = 'bomberman(work in progress)'

window = Game(
    TILE_SIZE * COLUMNS,
    TILE_SIZE * ROWS,
    SCREEN_TITLE)

arcade.run()
