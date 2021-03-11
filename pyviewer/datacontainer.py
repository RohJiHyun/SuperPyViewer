import numpy as np 
from pyviewer import viewcontrolobj as vco
from pyviewer import AABB

from OpenGL.GL import * 
from OpenGL.GLU import *
# from OPenGL.arryas import *
import time
import os 
from pyviewer import picker 
from scipy.sparse import csr_matrix

class WorldContainer():
    def __init__(self):
        self.reference_num = 0
        self.light = []
        self.default_light = vco.Light()
        self.data_container_list = []
        self.t= False

    def get_world(self):
        self.reference_num += 1
        return self 
    

    def clear(self):
        self.data_container_list.clear()

    def add_data(self, mesh):
        self.data_container_list.append(mesh)
    
    def add_light(self, light):
        self.light.append(light)

    def light_initialize(self):
        if self.light == [] :
            self.default_light.initialize()
        for l in self.light:
            l.initialize()
    
    def world_draw(self):
        for d in self.data_container_list:
            d.draw(self.default_light)
        
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


                calc_face_normal(*v_indice)

                for v_idx in v_indice:

                    glVertex3fv(V[v_idx])
                glEnd()
        start_t = time.time()
        


        # if self.draw_mesh_opt:
        #     # material()
        #     glColor3f(1.0, 1.0, 1.0)
        #     _draw(GL_TRIANGLES)
        

        _draw(GL_POINTS)

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
import sys
from pyviewer import utils
class Renderer2():
    def __init__(self, V, F, normal, material):
        """
            normal is vertex normal
        """
        self.vertex = V.astype('float32')
        self.face = F.astype('int32')
        self.normal =normal.astype('float32')
        # self.idx_mapper = self.mapping_index_to_face()
        # self.vertex_and_normal = self.calc_normal()
        
        self.material = material
        # self.vertex_and_normal = np.concatenate([self.vertex, self.vertex_and_normal], axis = -1)

        

        pass
        # glBindBuffer()
    @utils.print_time("mapping : {} {} {}")
    def mapping_index_to_face(self):
        reval = [[] for _ in range(len(self.vertex))]
        for v_idx in range(len(self.vertex)):
            for f_idx, f_v_indice in enumerate(self.face):
                for f_v_idx in f_v_indice:
                    if f_v_idx == v_idx :
                       reval[v_idx].append(f_idx)
        return reval
        
    @utils.print_time("calc_normal {} {} {}")
    def calc_normal_each_v(self, v_idx1, v_idx2, v_idx3):
        
        edge1 = self.vertex[v_idx2] - self.vertex[v_idx1]
        edge2 = self.vertex[v_idx3] - self.vertex[v_idx1]
        normal_vector = np.cross(edge1, edge2)
        return normal_vector/np.linalg.norm(normal_vector)


    @utils.print_time("calc_face_normal {} {} {}")
    def calc_face_normal(self):
        f_norms = []
        for indice in self.face : 
            f_norm = self.calc_normal_each_v(*indice)
            f_norms.append(f_norm)
        
        return np.array(f_norms)
        
    @utils.print_time("calc_vertex normal {} {} {}")
    def calc_vertex_normal(self):
        v_norms = []
        for v_idx in range(len(self.vertex)):
            v_norm = 0
            times = 0
            for f_idx in self.idx_mapper[v_idx]:
                v_norm += self.f_norms[f_idx]
                times += 1
            v_norm=v_norm/( times if times > 0 else 1)
            v_norms.append(v_norm / np.linalg.norm(v_norm))
        return np.array(v_norms)


    def compile(self):

        # self.f_norms = self.calc_face_normal()
        # self.v_norms = self.calc_vertex_normal()
        # print("norms")
        # print(self.f_norms)
        # print(self.v_norms)
        # add Vertex array object 
        # self.vao = GLuint(0)
        # glGenVertexArrays(1, self.vao)
        # glBindVertexArray(self.vao)




        # add vertex buffer for storing vertex and normal
        self.vbo = GLuint(0)
        glGenBuffers(1, self.vbo)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)

        # TODO THIS is Dummy code. will be removed after all.
        all_point = self.vertex[self.face.ravel()].astype(np.float32).flatten()
        self.all_point = all_point
        self.all_point = self.vertex.flatten()
        


        # [x1 y1 z1 nx1 ny1 nz1]
        # [x2 y2 z2 nx2 ny2 nz2]
        # . ...
        # . ...
        # self.vertice_and_normal = np.concatenate([self.vertex, self.v_norms], axis=-1)
        self.vertice_and_normal = self.vertex
        print("v="*10)
        print(self.vertice_and_normal.nbytes)
        print("vnorm",self.vertice_and_normal)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertice_and_normal.nbytes, self.vertice_and_normal.flatten(), GL_DYNAMIC_DRAW)
        
        
        
        
        


        self.ibo = GLuint(0)
        glGenBuffers(1, self.ibo)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.face.nbytes, self.face.flatten(), GL_STATIC_DRAW)
        
        self.nbo = GLuint(0)
        glGenBuffers(1, self.nbo)
        glBindBuffer(GL_ARRAY_BUFFER, self.nbo)
        glBufferData(GL_ARRAY_BUFFER, self.normal.nbytes, self.normal.flatten(), GL_DYNAMIC_DRAW) # =>> NEW TEST


        # Unbind until starting drawing.
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)


        

    def __del__(self):
        if hasattr(self, 'vbo'):
            glDeleteBuffers(1, self.vbo)
    def change_vertex_data_all(self, v, normal):
        self.vertex = v.astype(np.float32)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        print(v.astype(np.float32).flatten().nbytes)
        print(v.shape)
        
        # for idx, v in enumerate(self.vertex):
        #     glBufferSubData(GL_ARRAY_BUFFER, 4*(3+3)* idx , v.flatten().nbytes,v.flatten()) # edit vertex
        
        
        for idx, v in enumerate(self.vertex):
            glBufferSubData(GL_ARRAY_BUFFER, 4*(3)* idx , v.flatten().nbytes,v.flatten()) # edit vertex
        
        # glBufferSubData(GL_ARRAY_BUFFER, 0 , v.flatten().nbytes, v.flatten()) # edit vertex

        #normal
        glBindBuffer(GL_ARRAY_BUFFER, self.nbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0 , normal.flatten().nbytes, normal.flatten()) # edit vertex
        glBindBuffer(GL_ARRAY_BUFFER, 0)



    def change_vertex_data(self, v, idx, normal):
        v = v.astype(np.float32)
        self.vertex[idx] = v

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        print(v.astype(np.float32).flatten().nbytes)
        # glBufferSubData(GL_ARRAY_BUFFER, idx * 4 *(3+3), v.flatten().nbytes,v.flatten()) # edit vertex
        glBufferSubData(GL_ARRAY_BUFFER, idx * 4 *(3), v.flatten().nbytes,v.flatten()) # edit vertex



        glBindBuffer(GL_ARRAY_BUFFER, self.nbo)
        glBufferSubData(GL_ARRAY_BUFFER, idx * 4 *(3), normal.flatten().nbytes, normal.flatten()) # edit vertex
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        

        #TODO normal data need to be change



        

    # @utils.print_time
    def draw(self, fixed_v_idx = [], movable_v_idx=[], *args, **kwargs):


        self.material()
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        normal_offset = ctypes.c_void_p(3*4) # Normal_offset
        stride = 4*(3 + 3) # GL_FLOAT * (xyz_size + xyz_size)
        stride = 4*(3) # GL_FLOAT * (xyz_size + xyz_size)
        
        glVertexPointer(3, GL_FLOAT, stride, None )

        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.nbo) # ---- > NEW
        glNormalPointer(GL_FLOAT, stride, None)
        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        
        
        # glDrawElements(GL_TRIANGLES, len(self.face.flatten()), GL_UNSIGNED_INT, None)
        # print(self.face)
        
        
        # glDrawElements(GL_PATCHES , len(self.face.flatten()), GL_UNSIGNED_INT, None)
        glPolygonMode(GL_FRONT_AND_BACK ,GL_LINE)
        # glPolygonMode(GL_FRONT_AND_BACK ,GL_FILL)
        # glColor3fv([0.1,0.1,0.1])

        glDrawElements(GL_TRIANGLES, len(self.face.flatten()), GL_UNSIGNED_INT, None)

        glPolygonMode(GL_FRONT_AND_BACK ,GL_FILL)
        
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        # glBindVertexArray(0)
        # qad = gluNewQuadric() 
        # for idx in selected_v_idx:
        #     glDisable(GL_DEPTH_TEST)
        #     glEnable(GL_COLOR_MATERIAL) 
        #     glColor(1,0,0)
        #     glTranslatef(*self.vertex[idx])
        #     gluSphere(qad, .04, 10, 3)
        #     glDisable(GL_COLOR_MATERIAL) 
        #     glEnable(GL_DEPTH_TEST)
        for idx in fixed_v_idx : 
            glPointSize(10.0)

            glDisable(GL_DEPTH_TEST)
            glEnable(GL_COLOR_MATERIAL) 
        
            glColor3f(1.0, 0.0, .0)
            glBegin(GL_POINTS)

            glVertex3fv(self.vertex[idx])
            glEnd()
            glDisable(GL_COLOR_MATERIAL) 
            glEnable(GL_DEPTH_TEST)
        
        
        for idx in movable_v_idx : 
            glPointSize(10.0)

            glDisable(GL_DEPTH_TEST)
            glEnable(GL_COLOR_MATERIAL) 
        
            glColor3f(1.0, 1.0, .0)
            glBegin(GL_POINTS)

            glVertex3fv(self.vertex[idx])
            glEnd()
            glDisable(GL_COLOR_MATERIAL) 
            glEnable(GL_DEPTH_TEST)



        
        



        



class DataContainer():
    
    """
        based on local coord 
    """
    
    def __init__(self, V, F, pos=[0.0, 0.0, 0.0]):
        self.pos = np.array(pos)
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0

        print("data init")
        self.material = vco.Material()
        self.V = V.astype(np.float32)
        self.F = F.astype(np.int32)
        
        
        
        self.selected_v_idx = [] # fixed + movable_v_idx
        self.fixed_v_idx = []
        self.movable_v_idx = []

        
        self.is_initialized = False
        self.aabb = AABB.AABBTree()
        # self.renderer = RendererContainer(True, True, False)
        self.compile_flag = False

        self.F2V = self.get_F2V(self.V, self.F)
        self.update_normal()

        self.renderer = Renderer2(self.V, self.F, self.normal, self.material)
        # self.renderer.compile()
        self.aabb.insert_entity(self.V, self.F)
        

    def _add_fixed_point(self, idx):
        if idx in self.fixed_v_idx : 
            self.fixed_v_idx.remove(idx)
        self.fixed_v_idx.append(idx)
        
        
    def add_point(self, idx, fixed=False):
        if fixed : 
            self._add_fixed_point(idx)
        else : 
            self._add_movable_point(idx)

    def _add_movable_point(self, idx):
        if idx in self.movable_v_idx:
            self.movable_v_idx.remove(idx)
        self.movable_v_idx.append(idx)

    def selected_point_clear(self):
        self.movable_v_idx.clear()
        self.fixed_v_idx.clear()
    
    def remove_point(self, idx, fixed=False):
        if fixed:
            self._remove_fixed_point(idx)
        else : 
            self._remove_movable_point(idx)
    def _remove_fixed_point(self, idx):
        if idx in self.fixed_v_idx : 
            self.fixed_v_idx.remove(idx)
    def _remove_movable_point(self,idx):
        if idx in self.movable_v_idx:
            self.movable_v_idx.remove(idx)
    
    def check_idx_exists(self, idx, search_space='all'):
        """
            search_space : all or fixed or movable
        """
        is_in_fixed = idx in self.fixed_v_idx
        is_in_moved = idx in self.movable_v_idx
        if search_space == 'all':
            return is_in_fixed or is_in_moved
        elif search_space == 'fixed':
            return is_in_fixed
        elif search_space == 'movable':
            return is_in_moved
            
        

    
    @utils.print_time
    def set_data(self, V):
        """ 
            Not Yet Implements

        """
        self.V = V
        self.update_normal()
        self.aabb = AABB.AABBTree()
        self.aabb.insert_entity(self.V, self.F)
        self.renderer.change_vertex_data_all(V, self.normal)
    
    def get_F2V(self, V, F):
        nV = V.shape[0]
        nF = F.shape[0]
        vf_cnt = np.zeros((nV), 'f')
        Mv = []
        Mi = []
        Mj = []
        for i in range(nF):
            for v in F[i]:
                vf_cnt[v] += 1
        inv = 1./vf_cnt
        for i in range(nF):
            for v in F[i]:
                Mi.append(v)
                Mj.append(i)
                Mv.append(inv[v])
        F2V = csr_matrix((Mv, (Mi, Mj)), shape=(nV, nF))
        return F2V

    def update_normal(self):
        V = self.V
        F = self.F
        edge1 = V[F[:, 1]] - V[F[:, 0]]
        edge2 = V[F[:, 2]] - V[F[:, 0]]
        face_n = np.cross(edge1, edge2)
        norm = np.linalg.norm(face_n, axis=1)
        face_n /= norm[:, np.newaxis]
        vert_n = self.F2V.dot(face_n)
        norm = np.linalg.norm(vert_n, axis=1)
        vert_n /= norm[:, np.newaxis]
        self.normal = vert_n.astype("f4")
        # self.normal = face_n.astype('f4')
        
    def picked_v_update(self, ray):
        """
            picking point only move elements of movable.
        """
        if len(self.movable_v_idx) == 0:
            return
        idx = self.movable_v_idx[-1]
        new_v = picker.Picker.point_edit(ray, self.mat, self.V[ idx ] )
        interval = self.V[idx] - new_v
        self.V[idx] = new_v
        self.V[self.movable_v_idx[:-1],:] -= interval

        # self.renderer.change_vertex_data(new_v,idx)
        self.set_data(self.V)
        self.update_normal()
        self.renderer.change_vertex_data_all(self.V, self.normal)

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

    
    def draw(self, light):
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
        array = (GLfloat *16)()
        glGetFloat(GL_MODELVIEW_MATRIX, array)
        self.mat = np.array(array).reshape(4,4).T     
        glPopMatrix()
        
        glPushMatrix()
        glRotatef(self.rot_z, 0, 0, 1)
        glRotatef(self.rot_y, 0, 1, 0)
        glRotatef(self.rot_x, 1, 0, 0)
        array = (GLfloat *16)()
        # self.renderer.draw(self.V, self.F, self.material, self.selected_v_idx)
        light.enable()
        self.renderer.draw(self.fixed_v_idx, self.movable_v_idx)
        light.disable()
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
