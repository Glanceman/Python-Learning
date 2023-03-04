# -*- coding: utf-8 -*-


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

IS_PERSPECTIVE = True  
VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])  
SCALE_K = np.array([1.0, 1.0, 1.0])  
EYE = np.array([0.0, 0.0, 2.0])  
LOOK_AT = np.array([0.0, 0.0, 0.0])  
EYE_UP = np.array([0.0, 1.0, 0.0])  
WIN_W, WIN_H = 640, 480  
LEFT_IS_DOWNED = False  
MOUSE_X, MOUSE_Y = 0, 0  

light0_Position = [0.0, 1.0, 1.0, 1.0]
light0_Intensity = [0.75, 0.75, 0.75, 0.25]
i=0

def SetupLights():
    ambientLight = [0.2, 0.2, 0.2, 1.0]  
    diffuseLight = [0.9, 0.9, 0.9, 1.0]  
    specularLight = [1.0, 1.0, 1.0, 1.0]  
    lightPosition = [9.0, 9.0, 9.0, 1.0]  
    ambient = [0.05, 0.05, 0.05, 1.0]
    diffuse = [0.8, 0.8, 0.8, 1.0]
    specular = [0.6, 0.6, 0.6, 1.0]


    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0,GL_AMBIENT,ambientLight)
    glLightfv(GL_LIGHT0,GL_DIFFUSE,diffuseLight)
    glLightfv(GL_LIGHT0,GL_SPECULAR,specularLight)
    glLightfv(GL_LIGHT0,GL_POSITION,lightPosition)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)

    glClearColor(0.5,0.5,0.5,1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_SMOOTH)

def getposture():
    global EYE, LOOK_AT

    dist = np.sqrt(np.power((EYE - LOOK_AT), 2).sum())
    if dist > 0:
        phi = np.arcsin((EYE[1] - LOOK_AT[1]) / dist)
        theta = np.arcsin((EYE[0] - LOOK_AT[0]) / (dist * np.cos(phi)))
    else:
        phi = 0.0
        theta = 0.0

    return dist, phi, theta


DIST, PHI, THETA = getposture()  


def init():
    ambientLight = [0.2, 0.2, 0.2, 1.0]  
    diffuseLight = [0.8, 0.8, 0.8, 1.0]  
    specularLight = [0.3, 0.8, 0.6, 1.0]  
    lightPosition = [9.0, 9.0, 9.0, 1.0]  
    ambient = [0.05, 0.05, 0.05, 1.0]
    diffuse = [0.8, 0.8, 0.8, 1.0]
    specular = [0.6, 0.6, 0.6, 1.0]
    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specularLight)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
    glEnable(GL_LIGHT0)
    #
    glEnable(GL_COLOR_MATERIAL)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)

    glClearColor(0.5, 0.5, 0.5, 1.0)  
    glEnable(GL_DEPTH_TEST)  
    glDepthFunc(GL_LEQUAL)  
    glShadeModel(GL_SMOOTH)


def draw():
    global IS_PERSPECTIVE, VIEW
    global EYE, LOOK_AT, EYE_UP
    global SCALE_K
    global WIN_W, WIN_H

    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    global i
    i=i+1
    print(i)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if WIN_W > WIN_H:
        if IS_PERSPECTIVE:
            glFrustum(VIEW[0] * WIN_W / WIN_H, VIEW[1] * WIN_W / WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
        else:
            glOrtho(VIEW[0] * WIN_W / WIN_H, VIEW[1] * WIN_W / WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
    else:
        if IS_PERSPECTIVE:
            glFrustum(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])
        else:
            glOrtho(VIEW[0], VIEW[1], VIEW[2] * WIN_H / WIN_W, VIEW[3] * WIN_H / WIN_W, VIEW[4], VIEW[5])


    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


    glScale(SCALE_K[0], SCALE_K[1], SCALE_K[2])


    gluLookAt(
        EYE[0], EYE[1], EYE[2],
        LOOK_AT[0], LOOK_AT[1], LOOK_AT[2],
        EYE_UP[0], EYE_UP[1], EYE_UP[2]
    )


    glViewport(0, 0, WIN_W, WIN_H)

    glLineWidth(4)
    # ---------------------------------------------------------------
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

    # ---------------------------------------------------------------
    # glBegin(GL_TRIANGLES)                
    # glColor4f(1.0, 0.0, 0.0, 1.0)        
    # glVertex3f(-0.5, -0.366, -0.5)       
    # glColor4f(0.0, 1.0, 0.0, 1.0)        
    # glVertex3f(0.5, -0.366, -0.5)        
    # glColor4f(0.0, 0.0, 1.0, 1.0)        
    # glVertex3f(0.0, 0.5, -0.5)           
    # glEnd()                              
    # ---------------------------------------------------------------
    # glBegin(GL_POLYGON)
    # glVertex3f(-0.3, 0, 0.2)
    # glVertex3f(0.3, 0, -0.2)
    # glVertex3f(0.0, 0.7, 0.0)
    # glEnd()
    # glutSolidSphere(0.4, 30, 20)
    # glutSolidSphere(1, 3, 2)
    # ambient = [0.05, 0.05, 0.05, 1.0]
    # diffuse = [0.8, 0.8, 0.8, 1.0]
    # specular = [0.6, 0.6, 0.6, 1.0]
    glColor4f(0.2, 0.6, 0.6, 1.0)
    # glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
    # glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
    # glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
    glutSolidCube(0.4)
    # glutSolidTeapot(0.4)
    # glutSolidSphere(0.4, 40, 40)

    # ---------------------------------------------------------------
    # glBegin(GL_TRIANGLES)                

    # glColor4f(1.0, 0.0, 0.0, 1.0)        
    # glVertex3f(-0.5, 0.5, 0.5)           
    # glColor4f(0.0, 1.0, 0.0, 1.0)        
    # glVertex3f(0.5, 0.5, 0.5)            
    # glColor4f(0.0, 0.0, 1.0, 1.0)        
    # glVertex3f(0.0, -0.366, 0.5)         

    # glEnd()                              

    # ---------------------------------------------------------------
    glutSwapBuffers()  


def reshape(width, height):
    global WIN_W, WIN_H

    WIN_W, WIN_H = width, height
    glutPostRedisplay()


def mouseclick(button, state, x, y):
    global SCALE_K
    global LEFT_IS_DOWNED
    global MOUSE_X, MOUSE_Y

    MOUSE_X, MOUSE_Y = x, y
    if button == GLUT_LEFT_BUTTON:
        LEFT_IS_DOWNED = state == GLUT_DOWN
    elif button == 3:
        SCALE_K *= 1.05
        glutPostRedisplay()
    elif button == 4:
        SCALE_K *= 0.95
        glutPostRedisplay()


def mousemotion(x, y):
    global LEFT_IS_DOWNED
    global EYE, EYE_UP
    global MOUSE_X, MOUSE_Y
    global DIST, PHI, THETA
    global WIN_W, WIN_H

    if LEFT_IS_DOWNED:
        dx = MOUSE_X - x
        dy = y - MOUSE_Y
        MOUSE_X, MOUSE_Y = x, y

        PHI += 2 * np.pi * dy / WIN_H
        PHI %= 2 * np.pi
        THETA += 2 * np.pi * dx / WIN_W
        THETA %= 2 * np.pi
        r = DIST * np.cos(PHI)

        EYE[1] = DIST * np.sin(PHI)
        EYE[0] = r * np.sin(THETA)
        EYE[2] = r * np.cos(THETA)

        if 0.5 * np.pi < PHI < 1.5 * np.pi:
            EYE_UP[1] = -1.0
        else:
            EYE_UP[1] = 1.0

        glutPostRedisplay()


def keydown(key, x, y):
    global DIST, PHI, THETA
    global EYE, LOOK_AT, EYE_UP
    global IS_PERSPECTIVE, VIEW

    if key in [b'x', b'X', b'y', b'Y', b'z', b'Z']:
        if key == b'x':  
            LOOK_AT[0] -= 0.01
        elif key == b'X':  
            LOOK_AT[0] += 0.01
        elif key == b'y':  
            LOOK_AT[1] -= 0.01
        elif key == b'Y':  
            LOOK_AT[1] += 0.01
        elif key == b'z':  
            LOOK_AT[2] -= 0.01
        elif key == b'Z':  
            LOOK_AT[2] += 0.01

        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b'\r':  
        EYE = LOOK_AT + (EYE - LOOK_AT) * 0.9
        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b'\x08':  
        EYE = LOOK_AT + (EYE - LOOK_AT) * 1.1
        DIST, PHI, THETA = getposture()
        glutPostRedisplay()
    elif key == b' ':  
        IS_PERSPECTIVE = not IS_PERSPECTIVE
        glutPostRedisplay()


if __name__ == "__main__":
    glutInit()
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
    glutInitDisplayMode(displayMode)

    glutInitWindowSize(WIN_W, WIN_H)
    glutInitWindowPosition(300, 200)
    glutCreateWindow('My OpenGL')

    init()  
    glutDisplayFunc(draw)  
    glutReshapeFunc(reshape)  
    glutMouseFunc(mouseclick)  
    glutMotionFunc(mousemotion)  
    glutKeyboardFunc(keydown)  

    glutMainLoop()  