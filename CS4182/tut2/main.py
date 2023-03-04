from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


i=0

def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
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

    glColor4f(0.2,0.6,0.6,1.0)
    glutSolidSphere(0.4,20,20)
    global i
    print(i)
    i=((i+1)%50)
    lightPosition = [9.0, 9.0, 9.0, 1]
    glEnable(GL_LIGHTING)                   
    glLightfv(GL_LIGHT0,GL_POSITION,lightPosition)
    glEnable(GL_LIGHT0)

    glFlush()
    
    glutSwapBuffers()
    glutPostRedisplay()


def Init():
    #Global Setting
    ambientLight = [0.2, 0.2, 0.2, 1.0]  
    diffuseLight = [0.9, 0.9, 0.9, 1.0]   
    specularLight = [1.0, 1.0, 1.0, 1.0]   
    lightPosition = [9.0, 9.0, 9.0, 1.0]  
    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0,GL_AMBIENT,ambientLight)
    glLightfv(GL_LIGHT0,GL_DIFFUSE,diffuseLight)
    glLightfv(GL_LIGHT0,GL_SPECULAR,specularLight)
    glLightfv(GL_LIGHT0,GL_POSITION,lightPosition)
    glEnable(GL_LIGHT0)


    ambient = [0.05, 0.05, 0.05, 1.0]
    diffuse = [0.8, 0.8, 0.8, 1.0]
    specular = [0.6, 0.6, 0.6, 1.0]
    glEnable(GL_COLOR_MATERIAL)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)

    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glShadeModel(GL_SMOOTH)


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
    print("GL Version", glGetString(GL_VERSION))
    ###
    glutDisplayFunc(draw) # register the callback function
    glutMainLoop()