from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import ImportObject


class ribbon:
    obj = 0
    displayList = 0
    
    posX = 0.0
    posY = 0.0
    posZ = 0.0
    length = 1
    sizeX = 5.0
    sizeY = 1.0
    sizeZ = 1.0

    rotation = 0.0
    
    def __init__(self, x, z):
        self.posX = x
        self.posZ = z
        self.posY = 2
        
    def makeDisplayLists(self):
        # set execute function for drawing inside the list
        self.displayList = glGenLists(1)
        glNewList(self.displayList, GL_COMPILE)
        glEnable(GL_COLOR_MATERIAL)
        glColor3f(1,0,0)
        glutSolidCube(self.length)
        glDisable(GL_COLOR_MATERIAL)
        glEndList()
    
    def checkOverlapped(self, pt):
        x=pt[0]
        z=pt[1]

        front=False
        back = False 
        left=False 
        right = False

        frontThreshold =  self.posZ - (self.length*self.sizeZ)/2
        backThreshold =  self.posZ +(self.length*self.sizeZ)/2
        leftThreshold = self.posX - (self.length*self.sizeX)/2
        RightThreshold = self.posX + (self.length*self.sizeX)/2
        if z>frontThreshold:
            front=True
        if z<backThreshold:
            back=True
        if x>leftThreshold:
            left = True
        if x<RightThreshold:
            right = True
        if(front and back and left and right):
            return True
        return False

    def draw(self):
        glPushMatrix()
        
        glTranslatef(self.posX,self.posY,self.posZ)
        glRotatef(self.rotation,0.0,1.0,0.0)
        glScalef(self.sizeX,self.sizeY,self.sizeZ)

        glCallList(self.displayList)
        glPopMatrix()

            
        
