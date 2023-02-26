# -*- coding: utf-8 -*-

# -------------------------------------------
# quidam_02.py 
# -------------------------------------------

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import PIL.Image as Image
import numpy as np

IS_PERSPECTIVE = True                               
VIEW = np.array([-0.8, 0.8, -0.8, 0.8, 1.0, 20.0])  
EYE = np.array([0.0, 0.0, 2.0])                     
LOOK_AT = np.array([0.0, 0.0, 0.0])                 
EYE_UP = np.array([0.0, 1.0, 0.0])                  
WIN_W, WIN_H = 640, 480                             
COUNTER= 0

light0_Position = [0.0, 1.0, 1.0, 1.0]
light0_Intensity = [0.75, 0.75, 0.75, 0.25]

def init():
    ambientLight = [0.2, 0.2, 0.2, 1.0]  
    diffuseLight = [0.8, 0.8, 0.8, 1.0]   
    specularLight = [0.3, 0.8, 0.6, 1.0]  
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

    glClearColor(0.5, 0.5, 0.5, 1.0) 
    glEnable(GL_DEPTH_TEST)         
    glDepthFunc(GL_LEQUAL)           
    glShadeModel(GL_SMOOTH)




def draw():
    global IS_PERSPECTIVE, VIEW
    global EYE, LOOK_AT, EYE_UP
    global SCALE_K
    global WIN_W, WIN_H
    global COUNTER
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
   
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    if WIN_W > WIN_H:
        if IS_PERSPECTIVE:
            glFrustum(VIEW[0]*WIN_W/WIN_H, VIEW[1]*WIN_W/WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
        else:
            glOrtho(VIEW[0]*WIN_W/WIN_H, VIEW[1]*WIN_W/WIN_H, VIEW[2], VIEW[3], VIEW[4], VIEW[5])
    else:
        if IS_PERSPECTIVE:
            glFrustum(VIEW[0], VIEW[1], VIEW[2]*WIN_H/WIN_W, VIEW[3]*WIN_H/WIN_W, VIEW[4], VIEW[5])
        else:
            glOrtho(VIEW[0], VIEW[1], VIEW[2]*WIN_H/WIN_W, VIEW[3]*WIN_H/WIN_W, VIEW[4], VIEW[5])
        
  
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
        
   
    # glScale(SCALE_K[0], SCALE_K[1], SCALE_K[2])
    # glTranslatef(0.5,0.5,-0.7)
    glRotatef(COUNTER,0,1.0,1.0)

 
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
    
 
    glColor4f(0.2, 0.6, 0.6, 1.0)
    glutSolidTeapot(0.4)
    
    # ---------------------------------------------------------------
    glutSwapBuffers()
    COUNTER+=0.1
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
    glutMainLoop()                  