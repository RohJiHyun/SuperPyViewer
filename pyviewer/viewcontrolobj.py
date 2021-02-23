import numpy as np 
from OpenGL.GL import * 
from OpenGL.GLU import *
from pyviewer import picker

import numpy as np 

# NEED GL BUILDER 
# import datacontainer
from pyviewer import datacontainer
from pyviewer import AABB


class Light():
    def __init__(self):
        self.position = [0.0, 0.0, 1.0, 0.0]
        self.direcion = [0., 0., -1.]
        self.set_ambient([1.0, 1.0, 1.0, 0.0])
        self.set_ambient([0.0, 0.0, 0.0, 0.0])
        self.set_diffuse([1.0, 1.0, 1.0, 0.0])
        self.set_specular([1.0, 1.0, 1.0, 0.0])

        self.set_coeff()

    

    def set_coeff(self, constant =1.0, linear = 0.09, quadratic = 0.032):
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic


    def set_ambient(self, ambient):
        self.ambient = ambient
        return self 


    def set_diffuse(self, diffuse):
        self.diffuse = diffuse
        return self

    def set_specular(self, specular):
        self.specular = specular
        return self
    
    def initialize(self):
        glClearColor(0.,0.,0.,0.)
        glClearDepth(1.0)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_CULL_FACE)
        glFrontFace(GL_CCW)
        glEnable(GL_NORMALIZE)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        
        glEnable(GL_LIGHT0)

        glLightfv(GL_LIGHT0, GL_AMBIENT, self.ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, self.diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, self.specular)
        glLightfv(GL_LIGHT0, GL_POSITION, self.position)

    
    def __call__(self):
        pass

class Material():
    def __init__(self):
        # self.set_ambient([0.2, 0.2 , 0.2 , 0.0])
        self.set_ambient([1., 1. , 1. , 0.0])
        self.set_diffuse([1. , 1, 1., 0.0])
        self.set_specular([0.2, 0.2, 0.2, 0.0])
        self.set_emission([1.0, 0.0, 1.0, 0.0])
        self.set_shininess([1.0])

    def set_ambient(self, ambient):
        self.ambient = ambient
        return self
    def set_diffuse(self, diffuse):
        self.diffuse = diffuse
        return self
    def set_specular(self, specular):
        self.specular = specular
        return self

    def set_shininess(self, shininess):
        self.shininess = shininess
        return self
    def set_emission(self, emission):
        self.emission = emission
    

    def initialize(self):
        glEnable(GL_COLOR_MATERIAL)

    def __call__(self):
        # glEnable(GL_COLOR_MATERIAL)
        
        # disable it. for using glMatrialfv function. not glcolor
        # see also https://www.khronos.org/opengl/wiki/File:Opengl_lighting_flowchart.png
        

        # glDisable(GL_COLOR_MATERIAL)        
        # glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, self.ambient + self.diffuse)
        glEnable(GL_COLOR_MATERIAL)
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, self.shininess)
        glMaterialfv(GL_FRONT, GL_EMISSION, self.emission)
        # glEnable(GL_COLOR_MATERIAL)

        #anti aliasing
        # glEnable(GL_BLEND);
        # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
 



        # glEnable(GL_LINE_SMOOTH)
        # glEnable(GL_POINT_SMOOTH)

        

class VCOCollection():
    """
        View Controll Object Collection Class 


        Controll Cam_lists, Viewer State
    """
    def __init__(self):
        self.world = []
        self.windows =[]
        # self.
    
    def add_window(self):
        pass
    
    def read_default_yaml(self, file_name):
        pass

class LayoutOptions():
    def __init__(self):
        pass

    def set_layout(self):
        pass
class GL_Options():
    def __init__(self):
        pass
    

class RootWindow():
    def __init__(self, x, y, width, height, title = None):
        if title == None : 
            title = "No Title"
        self.title = title
        self.set_layout(1,1)
        self.vco = VCOCollection()
        self.child_group = [[]]
        self.gui = []

        self.x = x 
        self.y = y
        self.width = width 
        self.hegiht = height
        
        
        
        
        
    def _set_xywh(self, x, y, width, height):
        cond_function = lambda x : x > 0
        def _set_attribute(x, func):
            if func(x):
                return x
        self.width =  _set_attribute(width, cond_function )
        self.height = _set_attribute(height, cond_function )
        self.x = _set_attribute(x, cond_function )
        self.y = _set_attribute(y, cond_function )

    def reshape(x, y, width, height):
        
        self._set_attribute(x,y,width,height)
        child_width = width / self.cols
        child_height = height / self.rows

        for group_idx, group in enumerate(self.child_group):
            map_col = (group_idx) % self.cols # 0 ~ n - 1 
            map_row = (group_idx) // self.rows  # 0 ~ n - 1
            for window in group :
                window.reshape(x + map_col * child_width, y + map_row * child_height, child_width, child_height)
    

    def draw(self):
        pass

        



    def set_layout(self, rows, cols):
        self.rows = self.rows
        self.cols = self.cols
    

from PyQt5.QtWidgets import (QApplication, QMainWindow, QOpenGLWidget, QTextEdit, QDockWidget, QListWidget)
from PyQt5.QtCore import Qt

from pyviewer import utils

class Window(QOpenGLWidget):
    """
        Class Window Draw World. 
    """
    WIN_NUM = 0
    def __init__(self, viewer_name = None):
        super().__init__()
        if viewer_name == None : 
            viewer_name = "NoNameW_" +str(Window.WIN_NUM)
            Window.WIN_NUM += 1
        self.name = viewer_name
        self.camera = Camera()
        self.proj = Projection()

        self.x = 0
        self.y = 0
        self.width = -1.
        self.height = -1.


        self.factor_height = 1.0
        self.factor_width = 1.0

        self.is_mouse_pressed = False
        self.is_background_clicked = False #(It is bocome True if Point clicked)
        self.prev_mouse_pos = [0., 0.]

        self.startTimer(100/6)

    def timerEvent(self, event):
        self.update()
        
        

    # def reshape(self,x,y, w, h):
    #     self._set_xywh( x, y, w, h)
        

    def set_world(self, world):
        self.world = world
    
    # def get_ray(self, x, y):
    #     print("sisisisisi size : ", )
    #     return self.camera.get_ray(x,y, self.size().width(), self.size().height())

    # def _set_xywh(self, x, y, width, height):
    #     # glViewport(x,y,width, height)
        
    #     cond_function = lambda x : x > 0
    #     def _set_attribute(x, func):
    #         if func(x):
    #             return x
    #     width =  _set_attribute(width, cond_function )
    #     height = _set_attribute(height, cond_function )
    #     self.factor_width = 1 if self.width == -1 else width/self.width
    #     self.factor_height = 1 if self.width == -1 else width/self.width
    #     self.width =  _set_attribute(width, cond_function )
    #     self.height = _set_attribute(height, cond_function )
    #     self.x = _set_attribute(x, cond_function )
    #     self.y = _set_attribute(y, cond_function )
    # @utils.print_time
    def draw(self):
        # glViewport(self.x, self.y, self.width, self.height)
        # self.camera(self.factor_width, self.factor_height)

        self.camera(1,1)
        self.world.world_draw()
    
    # def initialize_vertex_array(self):
        
    #     self.vbo = glvbo.VBO(np.array([1,2,3]))
    #     self.vbo.bind()

    #     glEnableClientState(GL_VERTEX_ARRAY)
    #     glEnableClientState(GL_COLOR_ARRAY)

    #     buffer_offset = ctypes.c_void_p
    #     # stride = (3+3)*self.vertices.itemsize
    #     stride = (3+3)*4
    #     glVertexPointer(3, GL_FLOAT, stride, None)
    #     glColorPointer(3, GL_FLOAT, stride, buffer_offset(12))
    #     glBindVertexArray(0)

    def initializeGL(self):
        print("init")

        glClearColor(0,0,0,0)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        # self.resizeGL(self.size().width(), self.size().height())

        self.world.light_initialize()




    
    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        self.draw()
        glFlush()
        
    def resizeGL(self, width, height):
        # glViewport(0,0,width,height)
        # array = (GLfloat *16)()

        # glGetFloat(GL_MODELVIEW_MATRIX, array)
        # mview = np.array(array).reshape(4,4).T
        # print("eye to world : \n", mview)
        print("resize" , width, height)
        glViewport(0,0,width,height)
        self.proj.set_mode('ortho').set_aspect_ratio(width, height).set_angle(45.0).compile()
        self.proj()
        


    def mouseMoveEvent(self, pos):
        # picker.Picker.getxy(pos.x(), pos.y())
        # pass
        limit_size = 100
        delta_rot_per_ratio = np.pi/2
        def convert_delta_pos_to_rot(delta_x, delta_y):
            """
                if delta size is full width, then it convert to 3 time rotation.
            """
            x_rot = (abs(delta_x)/self.width )*6*np.pi
            y_rot = (abs(delta_y)/self.height )*6*np.pi
            return x_rot, y_rot



        if self.is_mouse_pressed and self.is_background_clicked : 
            x = pos.x()
            y = pos.y()
            delta_x = x  - self.prev_mouse_pos[0]
            delta_y =  y - self.prev_mouse_pos[1]
            if abs(delta_x) > limit_size :
                self.prev_mouse_pos[0] = x 
                x_rot, y_rot = convert_delta_pos_to_rot(delta_x, delta_y)
            else : 
                delta_x = 1
                x_rot = 0
            

            if abs(delta_y) > limit_size :
                self.prev_mouse_pos[1] = y
                x_rot, y_rot = convert_delta_pos_to_rot(delta_x, delta_y)
            else :
                delta_y = 1
                y_rot = 0
            
            
            self.world.data_container_list[0].rotation_update((delta_x / abs(delta_x)) * x_rot, (delta_y / abs(delta_y)) * y_rot, 0 )

        elif self.is_mouse_pressed and not self.is_background_clicked:
            self.world.data_container_list[0].picked_v_update(picker.Picker.get_ray(pos.x(), pos.y(), self.size().width(), self.size().height(), self.proj.mat, self.camera.mat))




    
    def mousePressEvent(self, pos):
# <<<<<<< Updated upstream
#         import operator
#         # ray_near, ray_far = picker.Picker.getxy(pos.x(), pos.y())
#         # print(picker.Picker.getxy(pos.x(), pos.y()))
#         # # self.is_mouse_pressed = True
#         # # ray = self.get_ray(pos.x(), pos.y())
#         # # fid, b_coord, closest_v_idx, t = self.world.data_container_list[0].query_ray(ray)
#         # # fid, b_coord, closest_v_idx, t =  picker.Picker.pick(pos.x(), pos.y(),self.size().width(), self.size().height(), self.world.data_container_list[0])
#         # # if fid == -1 : 
#         # #     self.is_background_clicked = True
#         # #     return 
        
#         # # self.world.data_container_list[0].selected_v_idx.append(closest_v_idx)
#         # // per-vertex
#         # for (int i = 0; i < num_vertice; i++){
#         lengths = []
#         for i, vertex in enumerate(self.world.data_container_list[0].V):
            
#             near, far = picker.Picker.get_near_far(pos.x(), pos.y())
#             length = picker.Picker.pointToLineDistance3D(near, far, vertex)
#             lengths.append((length, i))
# =======
        self.is_mouse_pressed = True
        from pyviewer import picker
        # ray = self.get_ray(pos.x(), pos.y())
        # fid, b_coord, closest_v_idx, t = self.world.data_container_list[0].query_ray(ray)
        fid, b_coord, closest_v_idx, t, length =  picker.Picker.pick(pos.x(), pos.y()\
                                                            ,self.size().width()\
                                                            ,self.size().height()\
                                                            ,self.proj.mat, self.camera.mat,\
                                                            self.world.data_container_list[0])
        if fid == -1 : 
            self.is_background_clicked = True
            return 
        print("closest v idx", closest_v_idx)
        print(self.world.data_container_list[0].V[closest_v_idx])
        self.world.data_container_list[0].selected_v_idx.append(closest_v_idx)
# >>>>>>> Stashed changes

        # lengths = sorted(lengths, key=operator.itemgetter(0))
        # print(lengths)

        # self.world.data_container_list[0].selected_v_idx.append(lengths[0][1])


            
        # int v_idx = i;
        # vector3 v = vertices[v_idx];
        # cml::vector3d a, b; unProject(mouseX, mouseY, a, b);
        # double len = pointToLineDistance3D(a,b, cml::vector3d(v[0],v[1],v[2]));
        # IntFourMulitples four(j_idx,c_idx,f_idx,v_idx);
        # distances.push_back(make_pair(four, len));

    def mouseReleaseEvent(self, pos):
        self.is_mouse_pressed = False 
        self.is_background_clicked = False
        self.prev_mouse_pos[0] = 0
        self.prev_mouse_pos[1] = 0
        
        self.world.data_container_list[0].selected_v_idx.clear()



    




        

    



class Projection():
    PERSPECTIVE_MODE = "perspect"
    ORTHGONAL_MODE = "ortho"
    def __init__(self):
        
        self.mode = Projection.ORTHGONAL_MODE
        
        self.width = -1
        self.height = -1
        self.width_factor = 1.0
        self.height_factor = 1.0
        self.aspect = self.width / self.height
        self.angle = 45.0

        self.near = -2
        self.far  = 2
        self.top = 1
        self.bottom = -1 
        self.left = -1 
        self.right = 1
        # self.near = -10
        # self.far  = 10
        # self.top = 10
        # self.bottom = -10
        # self.left = -10
        # self.right = 10

    def set_mode(self, mode = "ortho"):
        if Projection.ORTHGONAL_MODE == mode :
            self.mode = mode
        elif Projection.PERSPECTIVE_MODE == mode: 
            self.mode = mode 
        else : 
            self.mode = Projection.ORTHGONAL_MODE
        return self
    
    def set_aspect_ratio(self, width, height):
        

        if self.width == -1 or self.height == -1 :
            self.width = width
            self.height = height
        self.width_factor = width / self.width
        self.height_factor = height / self.height
        self.aspect = width/height

        

        return self

    def set_angle(self, angle):
        self.angle = angle
        return self
    
    def compile(self):
        self.view = self._wrap_proj()

    def _wrap_proj(self):
        def wrap_func():
            if self.mode == Projection.ORTHGONAL_MODE : 
                glOrtho(self.left *  self.aspect, self.right * self.aspect,\
                        self.bottom , self.top,\
                        self.near, self.far)

            elif self.mode == Projection.PERSPECTIVE_MODE:
                gluPerspective(45.0, self.aspect, 1., 100.)
            
            array = (GLfloat *16)()
            glGetFloat(GL_MODELVIEW_MATRIX, array)
            self.mat = np.array(array).reshape(4,4).T

        return wrap_func



    def __call__(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        self.view()

    
        

class Camera():
    
    CAM_NUM = 0
    PERSPECTIVE_MODE = "perspect"
    ORTHGONAL_MODE = "ortho"
    def __init__(self):
        self.default_cam_pos = self.cam_pos = [0.,0., 1.]
        self.default_cam_direct = self.cam_direct = [0.,0., -1.]
        self.default_cam_normal_direction = self.cam_normal_direction = [0.,1.,0.]
        self.mode = Camera.ORTHGONAL_MODE

        # example
        self.near = 0
        self.far = 0


    def set_name(self, name=None):
        if name == None : 
            name = "NoNameCam_"+str(Camera.CAM_NUM)
            Camera.CAM_NUM += 1
        self.name = name

    def set_campos(self, x, y, z):
        self.cam_pos[0] = x
        self.cam_pos[1] = y
        self.cam_pos[2] = z

    def update_campos(self, delta_x, delta_y, delta_z):
        self.cam_pos[0] += delta_x
        self.cam_pos[1] += delta_y
        self.cam_pos[2] += delta_z
        return self
    
    def rotate(self, angle, axis):
        
        return self
    
    def set_direction(self, x, y, z):
        if not [(self.cam_pos[x] + self.cam_pos[y] +self.cam_pos[z] - x - y - z) == 0 ]:
            self.cam_direct[x] = x 
            self.cam_direct[y] = y
            self.cam_direct[z] = z

    def __call__(self, w_factor = 1., h_factor = 1.):
        # #Add transform after....
        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        # self.w_factor = w_factor
        # self.h_factor = h_factor
        # # gluPerspective(45, (1/ 2), 0.1, 50.)

        # glOrtho(-1*w_factor, 1*w_factor, -1*h_factor, 1*h_factor, -2, 2)
        # # glTranslatef(*self.cam_pos)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        # print("cam pos : {} dir : {} normla {}".format(self.cam_pos, self.cam_direct, self.cam_normal_direction))
        gluLookAt(*self.cam_pos, *self.cam_direct, *self.cam_normal_direction)
        
        array = (GLfloat *16)()
        
        glGetFloat(GL_MODELVIEW_MATRIX, array)
        self.mat = np.array(array).reshape(4,4).T
        # print(self.mat, "whatis mat")
        # print("cam\n", self.mat)

        # return self.cam_pos, self.cam_direct, cam_normal_direction
        # print(self.mat)





if __name__ == "__main__":
    testcam = Camera()
    reval = testcam.get_ray(0,0, 300, 400)
    print(reval)
    