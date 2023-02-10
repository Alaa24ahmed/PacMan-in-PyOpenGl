from random import choice
from time import time

from OpenGL import GL as gl
from OpenGL import GLUT as glut

from heapq import heappop, heappush

MOVES = "NSWE"
OPPOSITE_MOVES = {
    "N": "S",
    "S": "N",
    "W": "E",
    "E": "W"
}
def set_color(color):
    """Function sets the color."""
    r, g, b = color
    gl.glColor3f(r, g, b)



class PacMan:
    def __init__(self, pos_x, pos_z):
        self.pos_x = pos_x
        self.pos_z = pos_z
        self.direction = ''
        self.next_direction = ''
        self.radius = 0.5
        self.rotate = 0
        self.step = 0.1
        self.color = 1, 1, 0
        self.was_eaten = False

    def move(self):
        if self.direction == 'N':
            self.pos_z -= self.step
            self.rotate = 0
        elif self.direction == 'S':
            self.pos_z += self.step
            self.rotate = 180
        elif self.direction == 'W':
            self.pos_x -= self.step
            self.rotate = 90
        elif self.direction == 'E':
            self.pos_x += self.step
            self.rotate = 270
        self.pos_x, self.pos_z = round(self.pos_x, 2), round(self.pos_z, 2)

    def draw(self):

        set_color(self.color)

        gl.glPushMatrix()
        gl.glTranslatef(self.pos_x + 0.5, 0.0, self.pos_z + 0.5)
        gl.glRotate(self.rotate, 0, 1, 0)
        glut.glutSolidSphere(self.radius, 10, 10)
        gl.glPopMatrix()

class Ghost(PacMan):
    def __init__(self, pos_x, pos_z, direction, color):
        super().__init__(pos_x, pos_z)
        self.primary_color = color
        self.step = 0.1
        self.eatable_time = 0.5
        self.eatable = False
        self.the_way = None
        self.direction = ""
        self.next_direction = direction

    def choice_next_direction(self):
        self.next_direction = choice(MOVES.replace(OPPOSITE_MOVES[self.direction], ""))

    def draw(self):
        set_color(self.color)
        gl.glPushMatrix()
        gl.glTranslatef(self.pos_x + 0.5, 0.0, self.pos_z + 0.5)
        gl.glRotate(self.rotate, 0, 1, 0)
        glut.glutSolidSphere(self.radius, 10, 10)
        gl.glPopMatrix()

    def was_eaten_by_pacman(self):
        self.color = 0.5, 0.5, 0.5
        self.was_eaten = True

    def start_from_nest(self):
        self.eatable_time = 0
        self.eatable = False
        self.the_way = None
        self.was_eaten = False
        self.color = self.primary_color
        self.next_direction = "N"

    def become_eatable(self):
        if not self.eatable:
            self.eatable, self.color = True, (0.75, 0.75, 0.75)
        self.eatable_time = time()

    def become_not_eatable(self):
        if time() - self.eatable_time >= 10 and not self.was_eaten:
            self.eatable, self.color = False, self.primary_color
            self.eatable_time = 0

    @staticmethod
    def heuristic(cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    def find_path(self, maze_graph, goal_position):
        start, goal = (self.pos_z, self.pos_x), goal_position
        pr_queue = []
        heappush(pr_queue, (0 + self.heuristic(start, goal), 0, "", start))
        visited = set()
        graph = maze_graph
        while pr_queue:
            _, cost, path, current = heappop(pr_queue)
            if current == goal:
                self.the_way = path
                break
            if current in visited:
                continue
            visited.add(current)
            for direction, neighbour in graph[current]:
                heappush(
                    pr_queue,
                    (cost + self.heuristic(neighbour, goal),
                     cost + 1, path + direction, neighbour)
                )
