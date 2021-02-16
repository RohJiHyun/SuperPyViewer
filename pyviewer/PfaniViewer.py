import sys, math, numpy
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import time
from numpy import linalg as LA


scale_factor = 0.2

# import net_utils.draw_utils as draw_utils
# import net_utils.mmMath as mm


#double color_set[9][3] = 
#{
  #{202. / 255., 84. / 255., 110. / 255.},
  #{0., 0.4 ,1.0},
  #{0.6, 0.6 ,0.0},
  #{0.2, 0.5 ,0.2},
  #{0. / 255., 136. / 255., 124. / 255.},
  #{178./ 255., 122. / 255., 180. / 255.},
  #{246. / 255., 139. / 255., 51. / 255.},
  #{130. / 255., 0. / 255., 80. / 255.},
  #{24. / 255., 148. / 255., 184. / 255.}
#};
    
motion_color = np.array([[210/255.,  105/255., 30./255.],
                 [123./255., 112./255., 255./255.],
                 [255./ 255., 218. / 255., 175. / 255.],
                 [178./255., 122./255., 180./255.],
                 [130. / 255., 0. / 255., 80. / 255.],
                 [0. / 255., 136. / 255., 124. / 255.],
                 [24./255., 148./255., 184./255.], 
                 [39./255., 139./255., 239./255.]]).astype(np.float32)

# class MultiMotion:
#     def __init__(self, animations, use_rootxzr = False):
#         self.animations = animations
#         self.motions = []
#         self.use_rootxzr = use_rootxzr
#         self.init()
        
#     def init(self, ignore_root=False):
#         for ai in range(len(self.animations)): # the number of animation is three (Xnoise, Xorig, Xrecn)
#             motion = []
#             anim = np.swapaxes(self.animations[ai][0].copy(), 0, 1)
#             #print 'anim.shape: ', anim.shape # (240L, 69L)
#             joints, root_x, root_z, root_r = anim[:,:-3], anim[:,-3], anim[:,-2], anim[:,-1]
#             joints = joints.reshape((len(joints), -1, 3)) 
#             if self.use_rootxzr == True:
#                 #print 'joints.shape: ', joints.shape # (240L, 22L, 3L)
#                 rotation = Quaternions.id(1)
#                 translation = np.array([[0,0,0]])
                
#                 if not ignore_root:
#                     for i in range(len(joints)):
#                         joints[i,:,:] = rotation * joints[i]
#                         joints[i,:,0] = joints[i,:,0] + translation[0,0]
#                         joints[i,:,2] = joints[i,:,2] + translation[0,2]
#                         rotation = Quaternions.from_angle_axis(-root_r[i], np.array([0,1,0])) * rotation
#                         translation = translation + rotation * np.array([root_x[i], 0, root_z[i]])
#                         motion.append(Posture(joints[i]))
                
#             else:
#                 if not ignore_root:
#                     for i in range(len(joints)):
#                         motion.append(Posture(joints[i]))
            
#             #print 'len(motion): ',  len(motion)
#             self.motions.append(motion)
class MultiMotion:
    def __init__(self, animations, use_rootxzr = False):
        self.animations = animations
        self.motions = []
        self.use_rootxzr = use_rootxzr
        self.init()
        
    def init(self, ignore_root=False):
        for ai in range(len(self.animations)): # the number of animation is three (Xnoise, Xorig, Xrecn)
            motion = []
            # anim = np.swapaxes(self.animations[ai][0].copy(), 0, 1)
            anim = self.animations[ai][0].copy()
            #print 'anim.shape: ', anim.shape # (240L, 69L)
            joints = anim[:, :63]
            
            joints = joints.reshape((len(joints), -1, 3)) 
            print(joints.shape)
            if not ignore_root:
                for i in range(len(joints)):
                    motion.append(Posture(joints[i]))
            
            #print 'len(motion): ',  len(motion)
            self.motions.append(motion)

class Motion:
    def __init__(self, postures=None, selected=None, boxes = None, currFrame = 0):
        self.postures = postures
        self.boxes = boxes
        self.currFrame = currFrame
        self.selected = selected
        #self.roots = np.load('./data/roots.npz')['roots']
        
    def setupShadow(self):
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glDisable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_STENCIL_TEST)
        glStencilFunc(GL_EQUAL,0x1,0x1)
        glStencilOp(GL_KEEP,GL_ZERO,GL_ZERO)
        glStencilMask(0x1)

        glPushMatrix()
        light1_x = 10.0
        light1_y = -10.0
        light1_z = 20.0
        sm = [1,0,0,0, -(light1_x/light1_z) ,0,-(light1_y/light1_z),0, 0,0,1,0, 0,0,0,1]
        glMultMatrixf(sm)
        
    def unsetupShadow(self):
        glPopMatrix()
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_STENCIL_TEST)
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)

    # def drawBox(self, posture, use_shadow):
    #     #print 'draw box posture'
    #     # COMPUTE TRANSLATION
    #     lefthand_pos = np.array([posture.joints[17,0], posture.joints[17,1], posture.joints[17,2]])
    #     righthand_pos = np.array([posture.joints[21,0], posture.joints[21,1], posture.joints[21,2]])
    #     mid_pos = (lefthand_pos + righthand_pos)/2.
    #     # COMPUTE ROTATION 
    #     x_axis = mm.normalize(righthand_pos - lefthand_pos)
    #     y_axis = np.array([0.,1.,0.])
    #     z_axis = mm.normalize(np.cross(x_axis, y_axis))
    #     SO3 = np.array([[x_axis[0], y_axis[0], z_axis[0]],
    #                     [x_axis[1], y_axis[1], z_axis[1]],
    #                     [x_axis[2], y_axis[2], z_axis[2]]],
    #                      float)
    #     transV = mid_pos
    #     SE3 = mm.SO3ToSE3(SO3, transV)
    #     glPushMatrix()
    #     glScalef(0.2, 0.2, 0.2)
    #     glMultMatrixf(SE3.T)
    #     sx = 8.6; sy = 3.; sz = 14.
    #     glTranslatef(0.,0.,-5.5)
    #     draw_utils.drawCube([0.,0.,0.], sx, sy, sz, use_shadow)
    #     glPopMatrix()
        
    def view(self):
        self.setupShadow()
        offset = -8 * (len(self.postures)) / 2
        for i in range(len(self.postures)):
            glPushMatrix()
            glColor4f(0,0,0,0.15)
            #glTranslatef(6*i, 0, 0) 
            #glTranslatef(8*i, 0, 3*i)
            #if i >= 4: glTranslatef(6., 0., 0.)
            
            #if i == 4: glTranslatef(2, 0, 0) 
            #if i == 5: glTranslatef(-2, 0, 0) 
            #if i%2 == 1: glTranslatef(6, 0, 0)
            
            # glTranslatef(offset + 8*i, 0, 0)


            self.postures[i].view() # POSTURE
            
            #self.drawBox(self.postures[i], True) # BOX
            #if i == 1 or i == 3: self.drawBox(self.postures[i], True) # BOX
            glPopMatrix()
        self.unsetupShadow()                   
        
        for i in range(len(self.postures)):
            glPushMatrix()
            """
            if i%2 == 0: glColor3f(motion_color[0,0],motion_color[0,1],motion_color[0,2])
            if i%2 == 1: glColor3f(motion_color[1,0],motion_color[2,1],motion_color[2,2])
            """
            net = 6
            if i == 3: glColor3f(motion_color[net,0],motion_color[net,1],motion_color[net,2])
            else: glColor3f(motion_color[i,0],motion_color[i,1],motion_color[i,2])
            
            """ if i < 2: glColor3f(motion_color[0,0],motion_color[0,1],motion_color[0,2])
            elif i>= 2 and i < 4: glColor3f(motion_color[2,0],motion_color[2,1],motion_color[2,2]) 
            else: glColor3f(motion_color[1,0],motion_color[1,1],motion_color[1,2])
            """
            # glTranslatef(offset + 8*i, 0, 0)

            #if i%2 == 1: glTranslatef(6, 0, 0)
            
            #if i >= 4: glTranslatef(6., 0., 0.) 
            self.postures[i].view(self.selected) # POSTURE
            """
            # NUMBER
            glPushMatrix()
            pos = self.postures[i].joints[13] # HEAD
            #print 'pos: ', pos
            glScalef(0.2, 0.2, 0.2)
            glTranslatef(pos[0]-1., pos[1], pos[2])
            font=glut.GLUT_STROKE_ROMAN 
            glScaled(0.05, 0.05, 0.05);
            glut.glutStrokeCharacter(font,ord(str(i%6))) 
            glPopMatrix()
            """
            #glColor3f(178./255.,1.,102./255.)
            #self.drawBox(self.postures[i], False) # BOX
            #if i == 1 or i == 3: self.drawBox(self.postures[i], False) # BOX
            glPopMatrix()

def computeAngleAxis(pos1, pos2):
        dirV = np.empty(3).astype(np.float32)
        dirV[0] = pos2[0]-pos1[0]; dirV[1] = pos2[1]-pos1[1]; dirV[2] = pos2[2]-pos1[2]
        tmpA = np.dot(dirV, np.array([0,0,1]))
        crossV = np.cross(np.array([0,0,1]),dirV)
        tmpB = LA.norm(crossV)
        theta = np.arctan2(tmpB, tmpA)*180./np.pi
        length = LA.norm(dirV) 
        return [theta, crossV, length]

class Posture:
    def __init__(self, joints):
        self.qobj_sphere = gluNewQuadric() 
        self.qobj_cylinder = gluNewQuadric()
        self.joints = joints
        if len(joints) == 21:
            self.parents = np.array([-1,0,1,2,3,4,1,6,7,8,1,10,11,12,12,14,15,16,12,18,19,20])
            self.parents = self.parents[1:] -1
        elif len(joints) == 7: # end effector num
            self.parents = np.array([-1] * 6)
        else:
            raise 'something wrong..'



        #self.parents = np.array([0,0,1,2,3,4,1,6,7,8,1,10,11,12,12,14,15,16,12,18,19,20]) - 1
        #print 'joints.size: ', len(self.joints) # 22
        #print 'parents.size: ', len(self.parents) # 22
        
    def view(self, selectedidx=None):
        glPushMatrix()
        glScalef(scale_factor, scale_factor, scale_factor)
        # draw cylinder (bone)
        for j in range(len(self.parents)):
            if self.parents[j] != -1: #and j != 1:
                pidx = self.parents[j]
                pos1 = [self.joints[pidx,0], self.joints[pidx,1], self.joints[pidx,2]]
                pos2 = [self.joints[j,0], self.joints[j,1], self.joints[j,2]]
                #if j == 17 or j == 21: continue # skip drawing draw hands
                [theta, crossV, length] = computeAngleAxis(pos1, pos2)
                glPushMatrix()	
                glTranslatef(pos1[0], pos1[1], pos1[2])
                glRotatef(theta, crossV[0], crossV[1], crossV[2])
                gluCylinder(self.qobj_cylinder, 0.6, 0.6, length, 15, 15)
                glPopMatrix()
                
    
        # draw sphere (joint)
        # print len(self.joints) # ----> 22
        for j in range(len(self.parents)):
            #if j > 1:
                #if j == 17 or j == 21: continue # skip drawing draw hands
            pos = [self.joints[j,0], self.joints[j,1], self.joints[j,2]]
            colorcond = len(self.parents) == 6 and selectedidx is not None and selectedidx == j
            if colorcond:
                cc = np.zeros(4, GLfloat)
                glGetFloatv(GL_CURRENT_COLOR, cc)
                glColor3f(0.9, 0.2, 0.2)
            if len(self.parents) == 6:
                glPushName(100+j)

            glPushMatrix()
            glTranslatef(pos[0], pos[1], pos[2])
            gluSphere(self.qobj_sphere, 0.8, 15, 15)
            glPopMatrix()
            if len(self.parents) == 6:
                glPopName()
            if colorcond:
                glColor4fv(cc)
        glPopMatrix()
        
    
        """
        glPushMatrix()
        glScalef(0.2, 0.2, 0.2)
        glLineWidth(5.)
        glBegin(GL_LINES)
        for j in range (len(self.parents)):
            if self.parents[j] != -1 and j != 1:
                pidx = self.parents[j]
                glVertex3f(self.joints[pidx,0], self.joints[pidx,1], self.joints[pidx,2])
                glVertex3f(self.joints[j,0], self.joints[j,1], self.joints[j,2])
        glEnd()
        
        glPointSize(15.)
        glBegin(GL_POINTS)
        #for i in range(len(self.joints)):
        glVertex3f(self.joints[1,0], self.joints[1,1], self.joints[1,2])
        glVertex3f(self.joints[10,0], self.joints[10,1], self.joints[10,2])
        glVertex3f(self.joints[11,0], self.joints[11,1], self.joints[11,2])
        #glVertex3f(self.joints[12,0], self.joints[12,1], self.joints[12,2])
        #print(self.joints.shape)
        for j in range(len(self.joints)):
            if j > 1:
                glVertex3f(self.joints[j,0], self.joints[j,1], self.joints[j,2])
                if j == 17 or j == 21: continue # Do not draw hands
        glEnd()    

        glPopMatrix()
        
        """
