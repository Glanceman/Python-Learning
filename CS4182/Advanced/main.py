from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

WindowWidth =600
WindowHeight = 600

counter = 0
speed=0.01
shaderProgramID=None

def CompileShader(type, source):
    id = glCreateShader(type)
    glShaderSource(id, source)
    glCompileShader(id)
    result= glGetShaderiv(id,GL_COMPILE_STATUS)
    if result==GL_FALSE:
        error_msg = glGetShaderInfoLog(id)
        glDeleteShader(id)
        error_msg="\n"+error_msg.decode('utf-8')
        raise Exception(error_msg)
    return id


def CreateProgram(vertexShader,fragmentShader):
    program = glCreateProgram()
    vs = CompileShader(GL_VERTEX_SHADER,vertexShader)
    fs = CompileShader(GL_FRAGMENT_SHADER,fragmentShader)

    glAttachShader(program, vs)
    glAttachShader(program, fs)
    glLinkProgram(program)
    glDeleteShader(vs)
    glDeleteShader(fs)
    return program



def Render():
    global counter,speed
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glBegin(GL_POLYGON)
    glVertex2f(1,1)
    glVertex2f(1,-1)
    glVertex2f(-1,-1)
    glVertex2f(-1,1)
    glEnd()
    location = glGetUniformLocation(shaderProgramID,"u_time")
    if(location == -1):
        raise Exception ("Location is not found")
    glUniform1f(location,counter)

    counter = (counter +speed)%1000 
    glutPostRedisplay()
    glutSwapBuffers()
    return 0

def Reshape(w,h):
    glutReshapeWindow(WindowWidth,WindowHeight)
    return 0

def Main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WindowWidth, WindowHeight)
    glutCreateWindow(b"Advanced Requirement")

    vertexShader ="""
    #version 410 core
    in vec3 in_position;
    void main(){
        gl_Position = vec4(in_position,1);
    }
    """

    fragmentShader = """ 
    #version 410 core
    out vec4 fragColor;
    uniform vec2 u_resolution;
    uniform float u_time;
    #define EULERVAL 2.718
    #define pi 3.14
    void main(){
        vec2 uv = (gl_FragCoord.xy-0.5*u_resolution.xy)/u_resolution.y;
        vec3 col = vec3(0.0);
        float r =0.1;
        float pointNums = 50 + cos(u_time/3)*10;
        for (int i =0; i< pointNums; i++){
            float step = i*(2*pi/pointNums)+(sin(u_time)+1);
            float tempVal= (pow(EULERVAL,cos(step))) -2 * cos(4*step)- pow(sin(step/12),5);
            float dx = r*sin(step)*tempVal;
            float dy = r*(max(cos(u_time/3),0.4))*cos(step)*tempVal;
            col = col + (0.001+(cos(u_time)+1)*0.0005)/length(uv-vec2(dx,dy));
        }
        /*col = col + 0.001/length(uv-vec2(0,0.2));
        col = col + 0.001/length(uv-vec2(0,-0.2));*/
        col *= abs(sin(u_time)+0.2)*vec3(0.8,0.5,0.3);
        fragColor = vec4(col,1.0);
    }
    """
    shaderProgram = CreateProgram(vertexShader,fragmentShader)
    global shaderProgramID 
    shaderProgramID  = shaderProgram
    glUseProgram(shaderProgram)
    location = glGetUniformLocation(shaderProgram,"u_resolution")
    if(location == -1):
        raise Exception ("Location is not found")
    glUniform2f(location,WindowWidth,WindowHeight)
    glutDisplayFunc(Render)
    glutReshapeFunc(Reshape)

    glutCreateMenu(setAnimationSpeedMenu)
    glutAddMenuEntry("add Speed",1)
    glutAddMenuEntry("reduce Speed",2)
    glutAttachMenu(GLUT_RIGHT_BUTTON)
    glutMainLoop()
    return 0

def setAnimationSpeedMenu(value):
    global speed
    if(value==1):
        speed+=0.005
    if(value==2):
        speed-=0.005
    return 0

if __name__ == "__main__":
    Main()