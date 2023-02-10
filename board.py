#! /usr/bin/env python


from random import choice
from OpenGL import GL as gl
from OpenGL import GLUT as glut

maze = [
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1], 
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0], 
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], 
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1], 
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], 
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], 
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1], 
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1], 
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1], 
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1], 
]


def set_color(color):
    r, g, b = color
    gl.glColor3f(r, g, b)


class Coin:
    def __init__(self, pos_x, pos_z):
        self.pos_x = pos_x
        self.pos_z = pos_z
        self.radius = 0.1
        self.coin_color =  0.9, 0.9, 0  
        self.super_coin = False

    def draw(self):
        set_color(self.coin_color)
        gl.glPushMatrix()
        gl.glTranslatef(self.pos_x + 0.5, 0.0, self.pos_z + 0.5)
        glut.glutSolidSphere(self.radius, 10, 10)
        gl.glPopMatrix()


class SuperCoin(Coin):
    def __init__(self, pos_x, pos_z):
        super().__init__(pos_x, pos_z)
        self.radius = 0.25
        self.coin_color = 0.9, 0.3, 0  # super coins color red
        self.super_coin = True

class Block:
    def __init__(self, pos_xw, pos_zn, walls):
        self.pos_xw = pos_xw
        self.pos_xe = pos_xw + 1
        self.pos_zn = pos_zn
        self.pos_zs = pos_zn + 1
        self.floor_color = 0.0, 0.1, 0.9  # color of floor
        # self.celling_color = 0.0, 0.1, 0.9        # color of celing
        self.floor_level = -1.0

    def draw_block(self):
        gl.glBegin(gl.GL_QUADS)  # Start drawing a polygon
        set_color(self.floor_color)
        gl.glVertex3f(self.pos_xw, 0, self.pos_zn)
        gl.glVertex3f(self.pos_xw, 0, self.pos_zs)
        gl.glVertex3f(self.pos_xe, 0, self.pos_zs)
        gl.glVertex3f(self.pos_xe, 0, self.pos_zn)
        gl.glEnd()

class Board:
    def __init__(self, maze):
        self.maze_len = len(maze)           # len of maze
        self.maze_row_len = len(maze[0])    # width of maze
        self.super_coins_no = 4             # number of super-coins
        self.blocks = []                     # blocks in the board
        self.coins = []                      # coins
        self.ghost_nest_position = 11, 14    # position of the ghost nest

        # dict of knots, key=position, value=possible directions of move
        self.knots = {}
        self.floor_color = 0.15, 0.15, 0.15  # color of floor
        # self.celling_color = 0.0, 0.1, 0.9        # color of celing
        self.floor_level = -1.0

        self._create_board_elements(maze)
        self._create_knots(maze)
        self.super_coins = self._create_super_coins()
        self.block_positions = self._get_block_positions()
        self.maze_graph = self._get_maze2graph(maze)

    def _get_block_positions(self):

        return set((block.pos_xw, block.pos_zn) for block in self.blocks)

    def _get_maze2graph(self, maze):

        self.maze_len = len(maze)
        self.maze_row_len = len(maze[0]) if self.maze_len else 0
        graph = {
            (i, j): []
            for j in range(self.maze_row_len)
            for i in range(self.maze_len)
            if not maze[i][j]
            }
        for row, col in graph.keys():
            if row < self.maze_len - 1 and not maze[row + 1][col]:
                graph[(row, col)].append(("S", (row + 1, col)))
                graph[(row + 1, col)].append(("N", (row, col)))

            if col < self.maze_row_len - 1 and not maze[row][col + 1]:
                graph[(row, col)].append(("E", (row, col + 1)))
                graph[(row, col + 1)].append(("W", (row, col)))
        return graph

    def _create_board_elements(self, maze):
        maze_size = len(maze) - 1
        coins_append = self.coins.append
        blocks_append = self.blocks.append

        for row_no, row in enumerate(maze):
            row_len = len(row) - 1

            for sq_no, square in enumerate(row):
                if not square:
                    coins_append(Coin(sq_no, row_no))
                else:
                    walls = []
                    walls_append = walls.append

                    if not all([row_no, maze[row_no-1][sq_no]]):
                        walls_append("N")

                    if not all([sq_no, maze[row_no][sq_no-1]]):
                        walls_append("W")

                    if sq_no == row_len or not maze[row_no][sq_no+1]:
                        walls_append("E")

                    if row_no == maze_size or not maze[row_no+1][sq_no]:
                        walls_append("S")

                    blocks_append(Block(sq_no, row_no, ''.join(walls)))

    def _create_knots(self, maze):

        for row_no, row in enumerate(maze):
            for sq_no, square in enumerate(row):

                if not bool(square) and bool(row_no) and bool(sq_no) and \
                   row_no != self.maze_len-1 and sq_no != self.maze_row_len-1:

                    direction = ""
                    if not maze[row_no-1][sq_no]:
                        direction += "N"
                    if not maze[row_no][sq_no-1]:
                        direction += "W"
                    if not maze[row_no][sq_no+1]:
                        direction += "E"
                    if not maze[row_no+1][sq_no]:
                        direction += "S"
                    self.knots[(sq_no, row_no)] = direction

    def _create_super_coins(self):
        return [SuperCoin(coin.pos_x, coin.pos_z) for coin in
                [choice(self.coins) for n in range(self.super_coins_no)]]

    def _draw_floor(self):
        gl.glBegin(gl.GL_QUADS)               # Start drawing a polygon
        set_color(self.floor_color)
        gl.glVertex3f(0,  self.floor_level, 0)
        gl.glVertex3f(self.maze_row_len, self.floor_level, 0)
        gl.glVertex3f(self.maze_row_len, self.floor_level, self.maze_len)
        gl.glVertex3f(0,  self.floor_level, self.maze_len)
        gl.glEnd()

    def draw(self):
        self._draw_floor()
        for block in self.blocks:
            block.draw_block()
        for coin in self.coins:
            coin.draw()
        for coin in self.super_coins:
            coin.draw()
