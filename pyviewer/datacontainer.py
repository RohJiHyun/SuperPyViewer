import numpy as np 
import viewcontrolobj as vco
import AABB

from OpenGL.GL import * 

from OpenGL.GLU import *
import time
import os 


class WorldContainer():
    def __init__(self):
        self.reference_num = 0
        self.light = []
        self.data_container_list = []
    

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
        
    
    def set_frames(self, required_frames):
        if required_frames <= 0:
            required_frames = 30
        
        self.required_frames = int(required_frames)
        self.limit_time_per_update = 1. / self.required_frames



    def set_option(self, draw_point_opt, draw_mesh_opt, draw_line_opt):
        self.draw_line_opt = draw_line_opt
        self.draw_mesh_opt = draw_mesh_opt
        self.draw_point_opt = draw_point_opt

    def draw(self, V, F):
        

        def _draw(enum):
            glBegin(enum)
            for v_indice in F :
                for v_idx in v_indice:
                    glVertex3fv(V[v_idx])
            glEnd()
        start_t = time.time()
        

        if self.draw_mesh_opt:
            _draw(GL_TRIANGLES)
        
        if self.draw_line_opt : 
            _draw(GL_LINES)

        if self.draw_point_opt:
            _draw(GL_POINT)
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


        self.material = None
        self.V = V
        self.F = V
        self.is_initialized = False
        self.aabb = AABB.AABBTree()
        self.renderer = RendererContainer()
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

    def rotation_reset(self):
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0

    def get_rotation(self):
        pass
    
    def draw(self):
        glRotatef(self.rot_x, 1, 0, 0)
        glRotatef(self.rot_y, 0, 1, 0)
        glRotatef(self.rot_z, 0, 0, 1)
        self.renderer.draw(self.V, self.F)

    def query_ray(self, ray):
        """
            return nearest triangle.
        """
        return self.aabb.ray_intersect(ray)

    