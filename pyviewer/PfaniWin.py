import math, copy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from fltk import *

import time
import ctypes
import numpy as np
import PfaniViewer as aniv
import mmMath as mm

scale_factor = aniv.scale_factor
class GlWindow(Fl_Gl_Window):
    def __init__(self, x, y, w, h, efs, view = None):
        Fl_Gl_Window.__init__(self, x,y,w,h)
        #self.boxes = None
        self.initGLFlag = True
        self.view = view
        self.efs = efs
        self.dragmode = False
        self.currentframe = -1
        self.selected = None
        self.ray = None

        # self.tmp =None
        #glutInit()
        
        self.camera = {}
        self.mouseX = 0
        self.mouseY = 0
        self.mousePrevX = 0
        self.mousePrevY = 0
        self.postures =  None
        self.ray_near = np.zeros(3, float)
        self.ray_far = np.zeros(3, float)
        self.qobj_sphere = gluNewQuadric() 

        self.camera['rotateX'] = mm.deg2Rad(0.0)
        self.camera['rotateY'] = mm.deg2Rad(-15.0)
        self.camera['centerX'] = 1.
        self.camera['centerY'] = -2.
        self.camera['centerZ'] = -10.
        self.camera['distance'] = -8.0
        
        self.press_1 = False
        self.press_2 = False
        self.press_3 = False


    def initGLColor(self):
        light_ambient =  [0.0, 0.0, 0.0, 1.0]
        light_diffuse = [1.0, 1.0, 1.0, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]
        light_position = [1.0, 1.0, 1.0, 0.0]

        mat_specular = [1.0, 1.0, 1.0, 1.0]
        mat_shininess = 40.0

        glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
        glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

        ambient = [0.6, 0.6, 0.6, 1]
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        #glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        glEnable(GL_POINT_SMOOTH)
        
    def initGL(self):
        
        fogStart = 20; fogEnd = 40 #TWO CHARACTERs
        fogStart = 30; fogEnd = 40 #MULTI-CHARACTER
        fogColor = [1.0, 1.0, 1.0, 1.0]
        glFogf(GL_FOG_DENSITY, 0.003)
        glFogi(GL_FOG_MODE, GL_LINEAR)
        glFogfv(GL_FOG_COLOR, fogColor)   
        glHint(GL_FOG_HINT, GL_NICEST)  
        glFogf(GL_FOG_START, fogStart)
        glFogf(GL_FOG_END, fogEnd)
        glEnable(GL_FOG)
        
        glPointSize(10.)
        #
        glViewport(0,0,self.w(),self.h())
       
        #glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective( 45., float(self.w())/float(self.h()), 0.1, 1000.)
        # glOrtho(-self.w()/100, self.w()/100, -self.h()/100, self.h()/100, 0.1, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        
        # self.camera['zoom'] = 0.6

        # self.camera['tw'] = 0.0
        # self.camera['el'] = -25.0
        # self.camera['az'] = 0 #-20.0
        # # compare 3 or close range
        # # self.camera['tx'] = 0.0
        # # self.camera['ty'] = 1.0
        # # self.camera['tz'] = 0.0
        # # compare 4 with close range
        # self.camera['tx'] = 2.0
        # self.camera['ty'] = 1.0
        # self.camera['tz'] = 0.0
        # compare 4 or walking seq
        # self.camera['tx'] = 1.0
        # self.camera['ty'] = 2.0
        # self.camera['tz'] = -5.0

    def cameraView(self):
        se3_1 = mm.getSE3ByTransV([self.camera['centerX'],self.camera['centerY'],self.camera['centerZ']]).T
        se3_2 = mm.getSE3ByRotY(self.camera['rotateY']).T
        se3_3 = mm.getSE3ByRotX(self.camera['rotateX']).T
        se3_4 = mm.getSE3ByTransV([0,0,self.camera['distance']]).T
        se3 = np.dot(np.dot(np.dot(se3_1,se3_2),se3_3),se3_4)
        glMultMatrixd(se3)

        # glRotated(-self.camera['tw'], 0.0, 1.0, 0.0)
        # glRotated(-self.camera['el'], 1.0, 0.0, 0.0)
        # glRotated(self.camera['az'], 0.0, 1.0, 0.0)

        #glTranslated(1, 2, -5)
        #glTranslated(self.camera['tx'], self.camera['ty'], self.camera['tz'])
        #glScaled(self.camera['zoom'], self.camera['zoom'], self.camera['zoom'])

    def drawGround(self):
        count = 0
        offset = 10
        step = 10
        glDisable(GL_LIGHTING)
        for i in range(-offset*step, (offset+1)*step, step):
            for j in range(-offset*step, (offset+1)*step, step):
                glColor3f(0.88, 0.88, 0.88)
                glBegin(GL_QUADS)
                #glNormal3f(0.,1.,0.)
                glVertex3f(j, 0, i)
                glVertex3f(j, 0, i+step)
                glVertex3f(j+step, 0, i+step)
                glVertex3f(j+step, 0, i)
                glEnd()
                count += 1
        glEnable(GL_LIGHTING)
        
    def drawAxis(self):
        glBegin(GL_LINES)
        glColor3f(1,0,0)
        glVertex3f(0.2,0,0)
        glVertex3f(0,0,0)
        glColor3f(0,1,0)
        glVertex3f(0,0.2,0)
        glVertex3f(0,0,0)
        glColor3f(0,0,1)
        glVertex3f(0,0,0.2)
        glVertex3f(0,0,0)
        glEnd()
    
    def setupFloor(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_ALWAYS,0x1,0x1)
        glStencilOp(GL_REPLACE,GL_REPLACE,GL_REPLACE)
        glStencilMask(0x1)
        
    def draw(self):
        global displayDelay, forceDisplay

        if self.initGLFlag == True:
            self.initGL()
            self.initGLColor() 
            self.initGLFlag = False
            print('initGL')
        glClearColor(1., 1., 1., 0.)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.cameraView()

        self.setupFloor()
        self.drawGround()
        
      
        if self.view != None: self.view()
        #start = time.clock()

        glFlush()

    def picking(self, x, y):
        buff = np.zeros(64, GLuint)
        # buff = arrays.GLuintArray.from_param(buff)
        viewport = np.zeros(4, GLint)
        # viewport = arrays.GLintArray.from_param(viewport)
        # model = np.zeros(16, GLfloat) 
        # glGetFloatv(GL_MODELVIEW_MATRIX, model)

        glSelectBuffer(64, buff)
        glGetIntegerv(GL_VIEWPORT, viewport)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glRenderMode(GL_SELECT)
        glLoadIdentity()
        gluPickMatrix(x, viewport[3]-y, 2, 2, viewport)
        gluPerspective( 45., float(self.w())/float(self.h()), 0.1, 1000.)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -17)
        self.draw()
        hits = glRenderMode(GL_RENDER)
        # print(hits)
        # if len(hits) > 0 :
        #     print(hits)
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        # print(x, y)
        # print(buff)
        # print(viewport)
        near = 1
        for i in hits:
            if len(i.names) != 0 and i.near < near:
                self.selected = i.names[0] - 100 # sub dummy offset 100
                near = i.near
        #     print(i.names, i.near, i.far)
        # print(self.selected)

    def unProject(self, x, y):
        pmat = (GLdouble * 16)()
        mvmat = (GLdouble * 16)()
        viewport = (GLint * 4)()
        glGetIntegerv(GL_VIEWPORT, viewport)
        glGetDoublev(GL_PROJECTION_MATRIX, pmat)
        glGetDoublev(GL_MODELVIEW_MATRIX, mvmat)

        x = float(x)
        y = viewport[3] - float(y) - 1
        ray_near = gluUnProject(x, y, 0.0, mvmat, pmat, viewport)
        ray_far = gluUnProject(x, y, 1.0, mvmat, pmat, viewport)
        
        return np.array(ray_near), np.array(ray_far)


    def get3DPointFromMousePoint(self, mouseX, mouseY):
        ray_near, ray_far = self.unProject(mouseX, mouseY)
        old_p =  scale_factor * self.efs[self.currentframe, self.selected*3:self.selected*3+3]
        new_p = np.linalg.norm(old_p-ray_near)/np.linalg.norm(ray_far-ray_near)*(ray_far-ray_near) + ray_near
        new_p = new_p / scale_factor 
        self.efs[self.currentframe, self.selected*3] = new_p[0]
        self.efs[self.currentframe, self.selected*3+1] = new_p[1]
        self.efs[self.currentframe, self.selected*3+2] = new_p[2]

        # return new_p

    # def dragging(self, x, y):
    #     # print(x, y, z)
    #     # ret = gluUnProject(float(x), float(viewport[3]-y), z, modelmat, projmat, viewport)
    #     # print(ret)
    #     pmat = (GLdouble * 16)()
    #     mvmat = (GLdouble * 16)()
    #     viewport = (GLint * 4)()
    #     glGetIntegerv(GL_VIEWPORT, viewport)
    #     glGetDoublev(GL_PROJECTION_MATRIX, pmat)
    #     glGetDoublev(GL_MODELVIEW_MATRIX, mvmat)

    #     x = float(x)
    #     y = viewport[3] - float(y) - 1
    #     z = self.__z
    #     ray_near = np.array(gluUnProject(x, y, z, mvmat, pmat, viewport))
    #     if self.ray_near is not None:
    #         delta = self.ray_near - ray_near
    #         self.efs[self.currentframe, self.selected*3:self.selected*3+3] -= delta

    #         # self.efs[self.currentframe, self.selected*3] = ray_near[0]
    #         # self.efs[self.currentframe, self.selected*3+1] = ray_near[1]
    #         # self.efs[self.currentframe, self.selected*3+2] = ray_near[2]
    #     self.ray_near = ray_near
    #     # self.efs[self.currentframe, self.selected] *= 5.
   
    def handle(self, e):
        returnVal = 0
        if Fl.event_key(ord('s')) is not 0 :
            self.dragmode = not self.dragmode
            returnVal = 1
            return returnVal
        
        
        if e == FL_RELEASE:
            self.mouseX = Fl.event_x()
            self.mouseY = Fl.event_y()

            returnVal = 1
        pushButton = Fl.event_button()
        if e == FL_PUSH:
            if pushButton == 1:
                self.press_1 = True
            if pushButton == 2:
                self.press_2 = True
            if pushButton == 3:
                self.press_3 = True
            returnVal = 1
		
        if e == FL_RELEASE:
            if pushButton == 1:
                self.press_1 = False
            elif pushButton == 2:
                self.press_2 = False
            elif pushButton == 3:
                self.press_3 = False
            returnVal = 1
        
        elif e == FL_PUSH:
            self.mouseX = Fl.event_x()
            self.mouseY = Fl.event_y()
            self.picking(self.mouseX, self.mouseY)
            if self.dragmode:
            #     self.__viewport = np.zeros(4, GLint)
            #     self.__modelmat = np.zeros(16, GLdouble) 
            #     self.__projmat = np.zeros(16, GLdouble)
            #     glGetIntegerv(GL_VIEWPORT, self.__viewport)
                pmat = (GLdouble * 16)()
                mvmat = (GLdouble * 16)()
                viewport = (GLint * 4)()
                glGetIntegerv(GL_VIEWPORT, viewport)
                glGetDoublev(GL_PROJECTION_MATRIX, pmat)
                glGetDoublev(GL_MODELVIEW_MATRIX, mvmat)

                x = float(self.mouseX)
                y = viewport[3] - float(self.mouseY) - 1
                self.__z = glReadPixels(x, y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
            #     glGetDoublev(GL_MODELVIEW_MATRIX, self.__modelmat)
            #     print(self.__modelmat)
            #     glGetDoublev(GL_PROJECTION_MATRIX, self.__projmat)
            #     print(self.__projmat)

            returnVal = 1
        elif not self.dragmode and e == FL_DRAG:
            self.mouseX = Fl.event_x()
            self.mouseY = Fl.event_y()
            mouseDeltaX = self.mouseX - self.mousePrevX
            mouseDeltaY = self.mouseY - self.mousePrevY

            button = Fl.event_button()
            if self.press_1 == True and self.press_3 == False:
                self.camera['rotateY'] -= mm.deg2Rad(float(mouseDeltaX)) /10.0
                self.camera['rotateX'] -= mm.deg2Rad(float(mouseDeltaY)) /10.0
            elif self.press_2 == False and self.press_3 == True:
                self.camera['centerX'] -= math.cos(self.camera['rotateY'])*float(mouseDeltaX)/32.0
                self.camera['centerZ'] -= -math.sin(self.camera['rotateY'])*float(mouseDeltaX)/32.0
                
                self.camera['centerX'] -= math.sin(self.camera['rotateY'])*float(mouseDeltaY)/32.0
                self.camera['centerZ'] -= math.cos(self.camera['rotateY'])*float(mouseDeltaY)/32.0

            elif self.press_2 == True:
                self.camera['distance'] -= float(mouseDeltaY) / 48.0
                if self.camera['distance'] < 0.0:
                    self.camera['distance'] = 0.0

            returnVal = 1

        elif e == FL_MOUSEWHEEL:
            self.camera['distance'] -= Fl.event_dy()/2.0
            if self.camera['distance'] < 0.0:
                self.camera['distance'] = 0.0
            returnVal = 1

            returnVal = 1
        elif self.dragmode and e == FL_DRAG and self.selected is not None:
            self.mouseX = Fl.event_x()
            self.mouseY = Fl.event_y()
            # self.dragging(self.mouseX, self.mouseY, self.__z, self.__viewport, self.__modelmat, self.__projmat)
            self.get3DPointFromMousePoint(self.mouseX, self.mouseY)
            # self.dragging(self.mouseX, self.mouseY)
            returnVal = 1

        self.mousePrevX = self.mouseX
        self.mousePrevY = self.mouseY

        if returnVal == 1:
            self.redraw()
        return returnVal

class Viewer(Fl_Window):
    def __init__(self, x, y, w, view = None, l = ''):
        self.name = l

        h = int (w / 4.0 * 3.0)  
        Fl_Window.__init__(self, x, y, w, h, l)

        self.begin()
        self.glWindow = GlWindow(0, 0, w, h, view)
        self.end()
            
        self.show()

    def show(self):
        Fl_Window.show(self)
        self.glWindow.show()

class MotionViewer(Fl_Window):
    def __init__(self, x, y, w, net = None, efs=None, boxes = None, l = ''):
        self.boxes = boxes
        self.net = net
        self.name = l
        self.offsetFrame = 0
        self.perFrame = True
        h = 720#int (w / 4.0 * 3.0)
        #h = int (w / 4.0 * 3.0)
        Fl_Window.__init__(self, x, y, w, h + 30, l)
        
        self.begin()
        self.glWindow = GlWindow(0, 0, w, h, efs, None)
        self.glWindow.boxes = self.boxes
            
        self.viewButton = Fl_Button(0, h, 40, 30)
        self.viewButton.label("@> / @||")
        self.viewButton.callback(self.callBack)
        self.viewButton.value(1)

        self.viewSlider = Fl_Hor_Value_Slider( 40, h, w - 40, 30)
        self.viewSlider.bounds(0, 1000)
        self.viewSlider.value(-1)
        self.viewSlider.step(1)
        self.viewSlider.callback(self.callBack)

        self.end()
        Fl.add_timeout(0.0, self.timer)
        
        self.numFrames = len(efs)

        motion = net.realtime_predict(efs[np.newaxis, :])
        self.motions = aniv.MultiMotion([motion]).motions
        if self.perFrame:
            self.efs = []
            for ef in efs:
                self.efs.append(ef)
        
        print ('self.numFrames', self.numFrames)
        if self.numFrames > 0:
            self.setBound()
            self.show()
        
        
    def setBound(self):
        self.viewSlider.bounds(0, self.numFrames - 1)

    def callBack(self, ptr):
        if str(ptr) == str(self.viewButton):
            if self.viewButton.value() == 1:
                self.viewButton.value(0)
            else:
                self.viewButton.value(1)
        elif str(ptr) == str(self.viewSlider):
            if self.viewSlider.value() > self.numFrames - 1:
                self.viewSlider.value(self.numFrames - 1)
            frame = int(self.viewSlider.value())
            
            postures = [m[frame+self.offsetFrame] for m in self.motions]
            currFrame = frame+self.offsetFrame
            if not self.perFrame:
                self.glWindow.currentframe = currFrame
                postures.append(aniv.Posture(self.glWindow.efs[currFrame]))
            else:
                postures.append(aniv.Posture(np.reshape(self.efs[currFrame], [-1, 3])))

            self.glWindow.view = aniv.Motion(postures, self.glWindow.selected, self.boxes,  currFrame).view
            self.glWindow.redraw()

    def timer(self):
        if self.viewButton.value() == 1:
            frame = int(self.viewSlider.value())
            self.viewSlider.value( frame + 1 )
            if self.viewSlider.value() >  self.numFrames - 1: 
                if self.perFrame:
                    self.numFrames += 1
                    self.setBound()
                    ef = np.reshape(self.glWindow.efs[-1],[1, 1, -1])
                    self.efs.append(ef[0, 0].copy())
                    pos = self.net.realtime_predict(ef)
                    self.motions[0].append(aniv.Posture(np.reshape(pos[..., :-3], [21, 3])))
                else:
                    motion = self.net.realtime_predict(np.reshape(self.glWindow.efs, [1, len(self.glWindow.efs), -1]))
                    self.motions = aniv.MultiMotion([motion]).motions
                    self.viewSlider.value(0)
            #start = time.clock()
            postures = [m[frame+self.offsetFrame] for m in self.motions]

            currFrame = frame+self.offsetFrame
            if not self.perFrame:
                self.glWindow.currentframe = currFrame
                postures.append(aniv.Posture(self.glWindow.efs[self.glWindow.currentframe]))
            else:
                postures.append(aniv.Posture(np.reshape(self.efs[currFrame], [-1, 3])))
            # pos = postures[1]
            # for j in range(len(pos.joints)):
            #     print(pos.joints[j])
            #     fl_draw(str(j), int(pos.joints[j, 0]*25)+400, int(pos.joints[j, 1]*25)+100)
            #print('--- copy time: %0.4f' % (time.clock() - start))
            #start = time.clock()
            self.glWindow.view = aniv.Motion(postures, self.glWindow.selected, self.boxes, currFrame).view
            self.glWindow.redraw()
            #print('--- draw time: %0.4f' % (time.clock() - start))

        Fl.repeat_timeout( 1./60. , self.timer)

    def show(self):
        Fl_Window.show(self)
        self.glWindow.show()
