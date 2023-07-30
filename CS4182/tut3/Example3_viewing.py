
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

EyePosition=[0,0,2]

#Plane
BL=[-1,-1,0]
BR=[1,-1,0]
TL=[-1,1,0]
TR=[1,1,0]


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # sets the canvas background color
    glEnable(GL_DEPTH_TEST)  # open depth test to realize occlusion relationship
    glDepthFunc(GL_LEQUAL)  # set up depth test function

def draw():

    # clear the screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # set the projection mode (Perspective Projection)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-0.8, 0.8, -0.8, 0.8, 1.0, 20.0)  # set the viewing volume

    # glOrtho(-0.8, 0.8, -0.8, 0.8, 1.0, 20.0)  # set the viewing volume

    # set the model_view matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # transformation
    glScale(1.0, 1.0, 1.0)

    # set the camera
    gluLookAt(
        2.0, 0.0, 0.0, # location
        0.0, 0.0, 0.2, # look at location
        0.0, 0.2, 0.0 # up direction
    )

    # set the viewport
    glViewport(0, 0, 640, 640)

    # ---------------------------------------------------------------
    glBegin(GL_LINES)  # draw lines in the world coordinate
    # draw the x axis in red
    glColor4f(1.0, 0.0, 0.0, 1.0)  # set current color
    glVertex3f(-0.8, 0.0, 0.0)  # set the vertex for x axis (negative direction)
    glVertex3f(0.8, 0.0, 0.0)  # set the vertex for x axis (positive direction)
    # draw the y axis in green
    glColor4f(0.0, 1.0, 0.0, 1.0)
    glVertex3f(0.0, -0.8, 0.0)
    glVertex3f(0.0, 0.8, 0.0)
    # draw the z axis in blue
    glColor4f(0.0, 0.0, 1.0, 1.0)
    glVertex3f(0.0, 0.0, -0.8)
    glVertex3f(0.0, 0.0, 0.8)
    glEnd()  # end drawing the line

    glBegin(GL_TRIANGLES)  # start drawing the triangle
    glColor4f(1.0, 0.0, 0.0, 1.0)
    glVertex3f(-0.5, -0.366, -0.5)
    glColor4f(0.0, 1.0, 0.0, 1.0)
    glVertex3f(0.5, -0.366, -0.5)
    glColor4f(0.0, 0.0, 1.0, 1.0)
    glVertex3f(0.0, 0.5, -0.5)
    glEnd()  # end drawing the triangle

    glBegin(GL_TRIANGLES)  # start drawing the triangle
    glColor4f(1.0, 0.0, 0.0, 1.0)
    glVertex3f(-0.5, 0.5, 0.5)
    glColor4f(0.0, 1.0, 0.0, 1.0)
    glVertex3f(0.5, 0.5, 0.5)
    glColor4f(0.0, 0.0, 1.0, 1.0)
    glVertex3f(0.0, -0.366, 0.5)
    glEnd()  # end drawing the triangle
    # ---------------------------------------------------------------
    glutSwapBuffers()
    glutPostRedisplay()


if __name__ == "__main__":
    glutInit()
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
    glutInitDisplayMode(displayMode)
    glutInitWindowSize(640, 640)
    glutInitWindowPosition(300, 200)
    glutCreateWindow('Quidam Of OpenGL')
    init()  # initialize the canvas
    glutDisplayFunc(draw)  # callback function draw()
    glutMainLoop()  # enter event loop