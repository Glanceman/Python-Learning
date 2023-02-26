# -*- coding: utf-8 -*-

# -------------------------------------------
# Texture mapping
# -------------------------------------------

# -*- coding: utf-8 -*-

# -------------------------------------------
# quidam_02.py 
# -------------------------------------------

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import PIL.Image as Image


def init():
    glClearColor(0.5, 0.5, 0.5, 1.0) 
    glEnable(GL_DEPTH_TEST)          
    glDepthFunc(GL_LEQUAL)           
    glShadeModel(GL_SMOOTH)

# def loadTexture(imageName='./diamondGeo.jpg'):
def loadTexture(imageName='./tree.jpg'):
    texturedImage = Image.open(imageName)
    try:
        imgX = texturedImage.size[0]
        imgY = texturedImage.size[1]
        img = texturedImage.tobytes("raw","RGBX",0,-1)#tostring("raw", "RGBX", 0, -1)
    except Exception, e:
        print "Error:", e
        print "Switching to RGBA mode."
        imgX = texturedImage.size[0]
        imgY = texturedImage.size[1]
        img = texturedImage.tobytes("raw","RGB",0,-1)#tostring("raw", "RGBA", 0, -1)

    glEnable(GL_TEXTURE_2D)
    myTexture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, myTexture)

    glTexImage2D(GL_TEXTURE_2D, 0, 3, imgX, imgY, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
    #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)


    glBegin(GL_POLYGON)
    glTexCoord2f(0,0)
    glVertex3f(-0.5,0.5,0)
    glTexCoord2f(1.0,0)
    glVertex3f(-0.5,-0.5,0)
    glTexCoord2f(1.0,1.0)
    glVertex3f(0.5,-0.5,0)
    glTexCoord2f(0,1.0)
    glVertex3f(0.5,0.5,0)
    glEnd()
    glutSwapBuffers()


def myKeyboard(key, x, y):
    if key =="h":
        print "h is down"


if __name__ == "__main__":
    glutInit()
    glutCreateWindow('My OpenGL')
    glutDisplayFunc(loadTexture)

    glutKeyboardFunc(myKeyboard)

    glutMainLoop()