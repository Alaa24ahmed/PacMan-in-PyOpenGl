import sys
from time import time
from math import hypot

from OpenGL import GL as gl
from OpenGL import GLUT as glut
from OpenGL import GLU as glu

import board
import characters

import OpenGL.GLUT as glut
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

os.system('cls')

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

 #=== draw text ================================================================================

def drawTextGAME(text,x,y,z,r,b,g):
    color = (r, b, g)
    font_style = glut.GLUT_BITMAP_HELVETICA_18
    glColor3ub(color[0],color[1],color[2])
    # line=0
    glRasterPos3f(x, y, z)
    for ch in text:
        glutBitmapCharacter(font_style, ord(ch))

def drawTextBold(ch,xpos,ypos):
    glPushMatrix()
    color = (250,163,27)
    font_style = glut.GLUT_BITMAP_HELVETICA_18
    glColor3ub(color[0],color[1],color[2])
    line=0
    glRasterPos2f (xpos, ypos)
    for i in ch:
        if  i=='\n':
            line=line+1
            glRasterPos2f (xpos, ypos*line)
        else:
            glutBitmapCharacter(font_style, ord(i))  
    glPopMatrix()  
    
#====================================================================================
def start_game():
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glPushMatrix()
        glColor3b(36, 150, 127)
        glLineWidth(3)
        glBegin(GL_LINE_LOOP)
        # glBegin(GL_QUADS)
        glVertex2f(673,475) 
        glVertex2f(673,308) 
        glVertex2f(883,308) 
        glVertex2f(883,475) 
        glEnd()
        glPopMatrix()
        drawTextBold("P L A Y G A M E", 730, 575)
        drawTextBold("P R E S S", 740, 390)
        
            
def init_for_otherscenes():
        glViewport(0, 0, 1450, 600)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, 1450, 0.0, 600, 0.0, 1.0)
        glMatrixMode (GL_MODELVIEW)


class Main:
    def __init__(self, maze):
        self.SCORE = 0
        self.lives = 30
        self.game_over = False
        self.play = False

        self.board = board.Board(maze)
        self.pacman = characters.PacMan(14, 18)
    
        self.ghost1 = characters.Ghost(14, 6, "N", (1.0, 0.0, 1.0))
        self.ghost2 = characters.Ghost(14, 6, "W", (1.0, 0.0, 0.0))
        self.ghost3 = characters.Ghost(14, 6, "E", (0.0, 1.0, 1.0))
        self.ghosts = [self.ghost1, self.ghost2, self.ghost3]

    def key_pressed_special(self, key,x,y):
        if key == 100:
            self.pacman.next_direction = 'W'
        elif key == 102:
            self.pacman.next_direction = 'E'
        elif key == 101:
            self.pacman.next_direction = 'N'
        elif key == 103:
            self.pacman.next_direction = 'S'
    
    def outside_board(self, object):
        if object.pos_x < 0:
            object.pos_x = self.board.maze_row_len-1
        elif object.pos_x > self.board.maze_row_len-1:
            object.pos_x = 0
        if object.pos_z < 0:
            object.pos_z = self.board.maze_len-1
        elif object.pos_z > self.board.maze_len-1:
            object.pos_z = 0

    def gameover(self):
        self.game_over = True
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glPushMatrix()
        glColor3b(36, 150, 127)
        glLineWidth(3)
        glBegin(GL_LINE_LOOP)
        glVertex2f(663,475) 
        glVertex2f(663,308) 
        glVertex2f(893,308) 
        glVertex2f(893,475) 
        glEnd()
        glPopMatrix()
        drawTextBold("G A M E O V E R", 730, 575)
        drawTextBold('YOUR FINAL SCORE: ',690,400) 
        drawTextBold(str(self.SCORE),730,350)
    
    def collision_pacman_coin(self, coin):
        wall1 = self.pacman.pos_x - coin.pos_x
        wall2 = self.pacman.pos_z - coin.pos_z
        radius = self.pacman.radius + coin.radius

        if radius > hypot(wall1, wall2):
            if coin.super_coin:
                self.SCORE += 10
                print("     SUPER COIN     ")
                print("    GHOST ARE SENSIBLE   ")
                self.board.super_coins.remove(coin)
                for one_ghost in self.ghosts:
                    one_ghost.become_eatable()
                    
            else:
                self.SCORE += 5    #regular coin
                self.board.coins.remove(coin)

    def collision_pacman_ghost(self, object):
        wall1 = self.pacman.pos_x - object.pos_x
        wall2 = self.pacman.pos_z - object.pos_z
        radius = self.pacman.radius + object.radius
        if radius > hypot(wall1, wall2):
            if object.eatable:
                print("GREAT, PACMAN ATE GHOST")
                self.SCORE += 10
                object.was_eaten_by_pacman()

            elif isinstance(object, characters.PacMan):     #The isinstance() function returns True if the specified object is of the specified type, otherwise False.
                if self.lives > 0:
                    self.lives -= 1
                elif self.lives == 0:
                    self.pacman.was_eaten = True
                    self.gameover()
                print("GHOST CATCHED PACMAN, TAKE CARE!!!")

    def pacman_move(self):
        directions = self.board.knots.get((self.pacman.pos_x, self.pacman.pos_z))
        if not self.pacman.was_eaten:
            if directions:
                if self.pacman.next_direction in directions:
                    self.pacman.direction = self.pacman.next_direction
                    self.pacman.move()
                elif self.pacman.direction in directions:
                    self.pacman.move()
                else:
                    pass   # PacMan makes no moves
            elif self.pacman.next_direction == OPPOSITE_MOVES[self.pacman.direction]:
                self.pacman.direction = self.pacman.next_direction
                self.pacman.move()
            else:
                self.pacman.move()

    def ghost_move(self, ghost):
        directions = self.board.knots.get((ghost.pos_x, ghost.pos_z))
        if not ghost.was_eaten:
            if directions:
                if len(directions) > 1:
                    if ghost.next_direction in directions:
                        ghost.direction = ghost.next_direction
                        ghost.choice_next_direction()
                        ghost.move()
                    elif ghost.direction in directions:
                        ghost.move()
                    else:
                        ghost.choice_next_direction()

                elif len(directions) == 1:
                    ghost.direction = directions
                    ghost.choice_next_direction()
                    ghost.move()
            else:
                ghost.move()
        else:
            if ghost.the_way:
                if directions:
                    ghost.direction = ghost.the_way[0]
                    ghost.move()
                    ghost.the_way = ghost.the_way[1:]
                else:
                    ghost.move()
            else:
                if directions:
                    ghost.find_path(self.board.maze_graph,self.board.ghost_nest_position)
                    ghost.direction = ghost.the_way[0]
                    ghost.move()
                    ghost.the_way = ghost.the_way[1:]
                else:
                    ghost.move()
            if (ghost.pos_z, ghost.pos_x) == self.board.ghost_nest_position:
                ghost.start_from_nest()
    
    def mouse_func(self,button, state,x,y):       # Click start game
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                if self.game_over:
                    game = Main(board.maze)
                    game.main()
                else:
                    self.game_over= False
                    self.play = True

    def draw_scene(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        glClearColor(255,255,255,1)
        glut.glutReshapeFunc(self.re_size_gl_scene)
        self.init_gl(340, 180)
        gl.glLoadIdentity()
        gl.glTranslatef(-self.board.maze_row_len/2, 10.0, -30.0)
        gl.glRotate(90, 1, 0, 0)

        if self.play == False:
            init_for_otherscenes()
            glLoadIdentity()
            start_game()
        else:
            if not self.game_over:
                drawTextGAME('SCORE : ',0,5,0,247,209,183) 
                drawTextGAME(str(self.SCORE),2.5,5,0,247,209,183)
                self.board.draw()
                self.pacman.draw()
                self.pacman_move()
                self.outside_board(self.pacman)
                for one_ghost in self.ghosts:
                    one_ghost.draw()
                    one_ghost.become_not_eatable()
                    self.ghost_move(one_ghost)
                    self.outside_board(one_ghost)
                    self.collision_pacman_ghost(one_ghost)

                for coin in self.board.coins:
                    self.collision_pacman_coin(coin)

                for coin in self.board.super_coins:
                    self.collision_pacman_coin(coin)
            else:
                init_for_otherscenes()
                self.gameover()
        glut.glutSwapBuffers()

    
    @staticmethod
    def init_gl(width, height):
        gl.glClearColor(0.0, 0.0, 0.0, 0.0)    #Clear The Background Color To Black
        gl.glClearDepth(1.0)  #enable clearing the depth
        gl.glDepthFunc(gl.GL_LESS)  #type of depth test
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45.0, float(width)/float(height), 0.1, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    @staticmethod
    def re_size_gl_scene(width, height):
        # Prevent A Divide By Zero If The Window Is Too Small
        if height == 0:
            height = 1
        # Reset The Current Viewport And Perspective Transformation
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(60.0, float(width)/float(height), 0.1, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def main(self):
        glut.glutInit()
        glut.glutInitDisplayMode(glut.GLUT_RGBA | glut.GLUT_DOUBLE | glut.GLUT_DEPTH)
        glut.glutInitWindowSize(1600, 800)
        glut.glutInitWindowPosition(0, 0)
        glut.glutCreateWindow("PacMan")
        glut.glutSpecialFunc(self.key_pressed_special)
        glut.glutDisplayFunc(self.draw_scene)
        glut.glutIdleFunc(self.draw_scene)
        glutMouseFunc(self.mouse_func)
        glut.glutReshapeFunc(self.re_size_gl_scene)
        self.init_gl(640, 480)
        glut.glutMainLoop()

if __name__ == "__main__":
    print("Hit ESC key to quit.")
    game = Main(board.maze)
    game.main()
