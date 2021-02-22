import numpy as np 
from pyviewer import viewcontrolobj as vco
from pyviewer import AABB

from OpenGL.GL import * 
from OpenGL.GLU import *
# from OPenGL.arryas import *
import time
import os 
from pyviewer import transforms as trans
from pyviewer import picker 

class WorldContainer():
    def __init__(self):
        self.reference_num = 0
        self.light = []
        self.data_container_list = []
        self.t= False

    def get_world(self):
        self.reference_num += 1
        return self 
    
    def add_data(self, mesh):
        self.data_container_list.append(mesh)
    
    def add_light(self, light):
        self.light.append(light)

    def light_initialize(self):
        for l in self.light:
            l.initialize()
    
    def world_draw(self):
        for d in self.data_container_list:
            d.draw()
        
    def remove_world(self):
        self.reference_num -= 1
        return self

from pyviewer import utils
class RendererContainer():
    """
        Fixed render time Based
    """
    def __init__(self, draw_mesh_opt = True, draw_line_opt = False, draw_point_opt = False, required_frames = 30):
        self.draw_line_opt = draw_line_opt
        self.draw_mesh_opt = draw_mesh_opt
        self.draw_point_opt = draw_point_opt
        self.set_frames(required_frames)
        self.pickmaterial = vco.Material().set_ambient([0.,0.,0.,0.0])

        
    
    def set_frames(self, required_frames):
        if required_frames <= 0:
            required_frames = 30
        
        self.required_frames = int(required_frames)
        self.limit_time_per_update = 1. / self.required_frames



    def set_option(self, draw_point_opt, draw_mesh_opt, draw_line_opt):
        self.draw_line_opt = draw_line_opt
        self.draw_mesh_opt = draw_mesh_opt
        self.draw_point_opt = draw_point_opt


    @utils.print_time
    def draw(self, V, F, material = None, selected_v_idx = []):
        def calc_face_normal(idx1, idx2, idx3):

            edge1 = V[idx2] - V[idx1]
            edge2 = V[idx3] - V[idx1]
            normal_vector = np.cross(edge1, edge2)
            glNormal3fv(list(normal_vector))

        
        def _draw(enum):
            
            for v_indice in F :
                glBegin(enum)


                # calc_face_normal(*v_indice)

                for v_idx in v_indice:

                    glVertex3fv(V[v_idx])
                glEnd()
        start_t = time.time()
        


        if self.draw_mesh_opt:
            # material()
            glColor3f(1.0, 1.0, 1.0)
            _draw(GL_TRIANGLES)
        
        # if self.draw_line_opt : 
        #     # material()
        #     glLineWidth(20)
        #     glDisable(GL_LIGHTING)
        
        #     glDisable(GL_LIGHT0)
        #     glColor3f(0.0, 0.0, 1.0)
        #     self.pickmaterial()
        #     _draw(GL_LINE_LOOP)

        # if self.draw_point_opt:
        #     material()
        #     _draw(GL_POINTS)
        

         
        for idx in selected_v_idx:

            glDisable(GL_LIGHTING)
            glDisable(GL_LIGHT0)
            glDisable(GL_DEPTH_TEST)
            glPointSize(10.0)

            glColor3f(1.0, 0.0, .0)
            glBegin(GL_POINTS)

            glVertex3fv(V[idx])
            glEnd()
            
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_DEPTH_TEST)
            

        # delta = time.time() - start_t
        # if delta < self.limit_time_per_update :
        #     time.sleep( self.limit_time_per_update - delta )

import ctypes 
import  OpenGL.arrays.vbo as glvbo # For GL VAO VBO

class Renderer2():
    def __init__(self, V, F):
        self.vertex = V
        self.face = F 
        # self.vertex_and_normal = self.calc_normal()
        
        # self.vertex_and_normal = np.concatenate([self.vertex, self.vertex_and_normal], axis = -1)

        




        pass
        # glBindBuffer()

    def calc_normal_each_v(self, v_idx1, v_idx2, v_idx3):
        
        edge1 = self.vertex[v_idx2] - self.vertex[v_idx1]
        edge2 = self.vertex[v_idx3] - self.vertex[v_idx1]
        normal_vector = np.cross(edge1, edge2)
        return normal_vector/np.linalg.norm(normal_vector)


    def calc_normal(self):
        f_norms = []
        for indice in self.face : 
            f_norm = self.calc_normal_each_v(*indice)
            f_norms.append(f_norm)
        
        return np.array(f_norms)
        

    def compile(self):
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        self.vertex_buffer_object_f_idx = glvbo.VBO(self.face)
        self.vertex_buffer_object_f_idx.bind()
        self.vertex_buffer_object_v_idx =  glvbo.VBO(self.vertex)
        self.vertex_buffer_object_v_idx.bind()
        

        glEnableClientState(GL_VERTEX_ARRAY)
        # glEnableClientState(GL_NORMAL_ARRAY)
        # glEnableClientState(GL_NORMAL_ARRAY)

        buffer_offset = ctypes.c_void_p
        # stride = (3+3)*self.vertex.itemsize
        stride = (3)*self.vertex.itemsize

        # glVertexPointer(3, GL_FLOAT, stride, None )
        glVertexPointer(3, GL_FLOAT, 0, None )
        # glNormalPointer(3, GL_FLOAT, stride, buffer_offset(12))

        glBindVertexArray(0)

    def change_vertex_data(self, v, idx):
        pass

    def draw(self, *args, **kwargs):
        glBindVertexArray(self.vao)
        glDrawElements(GL_TRIANGLES, len(self.face), GL_UNSIGNED_INT, self.face)
        glBindVertexArray(0)

        



class DataContainer():
    
    """
        based on local coord 
    """
    
    def __init__(self, V, F, pos=[0.0, 0.0, 0.0]):
        self.pos = np.array(pos)
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0


        self.material = vco.Material()
        self.V = V
        self.F = F
        self.selected_v_idx = []
        self.is_initialized = False
        self.aabb = AABB.AABBTree()
        self.renderer = RendererContainer(True, True, False)
        self.compile_flag = False
        self.renderer = Renderer2(self.V, self.F)
        # self.renderer.compile()
        self.aabb.insert_entity(self.V, self.F)
        

    def set_data(self, V, F):
        """ 
            Not Yet Implements

        """
        self.V = V
        self.F = F
        raise NotImplementedError()
        
    def picked_v_update(self, ray):
        idx = self.selected_v_idx[0]
        new_v = picker.Picker.point_edit(ray, self.mat, self.V[ idx ] )
        self.V[idx] = new_v

    def update_data(self, updated_data):
        self.data = updated_data


    def rotation_update(self, delta_x, delta_y, delta_z):
        """
            integer
        """
        self.rot_x += delta_x
        self.rot_y += delta_y
        self.rot_z += delta_z

        
        # self.aabb = AABB.AABBTree()
        # self.aabb.insert_entity((self.get_rotation()*self.V.T).T, self.F)

        
    def rotation_reset(self):
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0

    def get_rotation(self):
        return trans.RotationBuilder.make_euler_rotation(self.rot_x, self.rot_y, self.rot_z)

    
    def draw(self):
        # self.rot_x = 3
        # self.rot_y = 3
        # self.rot_z = 3
        if not self.compile_flag :
            self.compile_flag = True
            self.renderer.compile()

        # print("x : {} y : {} z : {}".format(self.rot_x, self.rot_y, self.rot_z))
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glRotatef(self.rot_z, 0, 0, 1)
        glRotatef(self.rot_y, 0, 1, 0)
        glRotatef(self.rot_x, 1, 0, 0)



        self.renderer.draw(self.V, self.F, self.material, self.selected_v_idx)
        array = (GLfloat *16)()
        
        glGetFloat(GL_MODELVIEW_MATRIX, array)
        self.mat = np.array(array).reshape(4,4).T        
        glPopMatrix()
       




    def query_ray(self, ray):
        """
            return nearest triangle.
        """
        # dummy code. TODO 
        # rot_composite = self.get_rotation()

        # print("rot composite", rot_composite)
        # ray.direction = np.linalg.inv(rot_composite.matrix ).dot( ray.direction)
        # ray.pos = np.linalg.inv(rot_composite.matrix ).dot(ray.pos)

        fid, b_coord, fid_vid,t, length = self.aabb.ray_intersect(ray)
        if fid == -1:
            return -1, -1, -1, -1, -1
        v_id = self.F[fid][fid_vid]
        print("f_id : {}, f_v_idx : {},\nF[fid] : {}\n v_id : {}".format(fid, fid_vid,self.F[fid], v_id))
        print("v1 : {}\nv2 : {}\nv3 : {}".format(self.V[self.F[fid][0]], self.V[self.F[fid][1]],self.V[self.F[fid][2]]))
        return fid, b_coord, v_id, t, length

