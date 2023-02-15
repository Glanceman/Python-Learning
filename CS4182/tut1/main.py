from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBegin(GL_LINES)                    
    glColor4f(1.0, 0.0, 0.0, 1.0)        
    glVertex3f(-0.8, 0.0, 0.0)           
    glVertex3f(0.8, 0.0, 0.0)            
    glColor4f(0.0, 1.0, 0.0, 1.0)        
    glVertex3f(0.0, -0.8, 0.0)           
    glVertex3f(0.0, 0.8, 0.0)            
    glColor4f(0.0, 0.0, 1.0, 1.0)
    glVertex3f(0.0, 0.0, -0.8)
    glVertex3f(0.0, 0.0, 0.8)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor4f(1.0, 0.0, 0.0, 1.0)
    glVertex3f(-0.5, -0.366, -0.5)
    glColor4f(0.0, 1.0, 0.0, 1.0)
    glVertex3f(0.5, -0.366, -0.5)
    glColor4f(0.0, 0.0, 1.0, 1.0)
    glVertex3f(0.0, 0.5, -0.5)
    glEnd()
    glFlush()
    
    glutSwapBuffers()


def Init():
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)

if __name__ == "__main__":
    glutInit()
    ###
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGBA|GLUT_DEPTH)
    glutInitWindowSize(500,500)
    glutInitWindowPosition(0,0)
    ###
    glutCreateWindow('My OpenGL')
    ###
    Init()
    ###
    glutDisplayFunc(draw) # register the callback function
    glutMainLoop()