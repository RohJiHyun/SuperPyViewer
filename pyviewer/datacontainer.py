import numpy as np 
from pyviewer import viewcontrolobj as vco
from pyviewer import AABB

from OpenGL.GL import * 

from OpenGL.GLU import *
import time
import os 
from pyviewer import transforms as trans

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

    def draw(self, V, F, material = None, selected_v_idx = []):
        def calc_face_normal(idx1, idx2, idx3):
            # print("idx is {} {} {} ".format(idx1, idx2, idx3))
            edge1 = V[idx2] - V[idx1]
            edge2 = V[idx3] - V[idx1]
            normal_vector = np.cross(edge1, edge2)
            glNormal3fv(list(normal_vector))
        # material = lambda : -1 if (material == None) else material
        
        def _draw(enum):
            
            for v_indice in F :
                glBegin(enum)


                calc_face_normal(*v_indice)

                for v_idx in v_indice:

                    glVertex3fv(V[v_idx])
                glEnd()
        start_t = time.time()
        


        if self.draw_mesh_opt:
            # material()
            glColor3f(1.0, 1.0, 1.0)
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
            # print("draw selected", idx)
            glDisable(GL_LIGHTING)
            glDisable(GL_LIGHT0)

            glPointSize(10.0)
            # self.pickmaterial()
            glColor3f(1.0, 0.0, .0)
            glBegin(GL_POINTS)

            glVertex3fv(V[idx])
            glEnd()
            
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            
        # glDisable(GL_COLOR_MATERIAL)

        delta = time.time() - start_t
        if delta < self.limit_time_per_update :
            time.sleep( self.limit_time_per_update - delta )
            

class DataContainer():
    """
        based on local coord 
    """
    def __init__(self, V, F, pos=[0.0,0.0,0.0]):
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
        self.aabb.insert_entity(self.V, self.F)
        

    def set_data(self, V, F):
        """ 
            Not Yet Implements

        """
        self.V = V
        self.F = F
        raise NotImplementedError()
        
        

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

        # print("x : {} y : {} z : {}".format(self.rot_x, self.rot_y, self.rot_z))
        glMatrixMode(GL_MODELVIEW)
        glRotatef(self.rot_z, 0, 0, 1)
        glRotatef(self.rot_y, 0, 1, 0)
        glRotatef(self.rot_x, 1, 0, 0)



        self.renderer.draw(self.V, self.F, self.material, self.selected_v_idx)

       




    def query_ray(self, ray):
        """
            return nearest triangle.
        """
        # dummy code. TODO 
        # rot_composite = self.get_rotation()

        # print("rot composite", rot_composite)
        # ray.direction = np.linalg.inv(rot_composite.matrix ).dot( ray.direction)
        # ray.pos = np.linalg.inv(rot_composite.matrix ).dot(ray.pos)

        fid, b_coord, fid_vid,t = self.aabb.ray_intersect(ray)
        if fid == -1:
            return -1, -1, -1, -1
        v_id = self.F[fid][fid_vid]
        print("f_id : {}, f_v_idx : {},\nF[fid] : {}\n v_id : {}".format(fid, fid_vid,self.F[fid], v_id))
        print("v1 : {}\nv2 : {}\nv3 : {}".format(self.V[self.F[fid][0]], self.V[self.F[fid][1]],self.V[self.F[fid][2]]))
        return fid, b_coord, v_id, t

