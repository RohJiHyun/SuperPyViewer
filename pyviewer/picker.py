import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

# NEED GL BUILDER

from pyviewer import AABB 
from pyviewer import datacontainer

# TODO 
class Picker():
    """
        Class Picker
        picking Helper Class
    """

    # def picking(self, x, y):
    #     buff = np.zeros(64, GLuint)
    #     # buff = arrays.GLuintArray.from_param(buff)
    #     viewport = np.zeros(4, GLint)
    #     # viewport = arrays.GLintArray.from_param(viewport)
    #     # model = np.zeros(16, GLfloat) 
    #     # glGetFloatv(GL_MODELVIEW_MATRIX, model)

    #     glSelectBuffer(64, buff)
    #     glGetIntegerv(GL_VIEWPORT, viewport)
    #     glMatrixMode(GL_PROJECTION)
    #     glPushMatrix()
    #     glRenderMode(GL_SELECT)
    #     glLoadIdentity()
    #     gluPickMatrix(x, viewport[3]-y, 2, 2, viewport)
    #     gluPerspective( 45., float(self.w())/float(self.h()), 0.1, 1000.)
    #     glMatrixMode(GL_MODELVIEW)
    #     glLoadIdentity()
    #     glTranslatef(0, 0, -17)
    #     #self.draw()
    #     hits = glRenderMode(GL_RENDER)
    #     # print(hits)
    #     # if len(hits) > 0 :
    #     #     print(hits)
    #     glMatrixMode(GL_PROJECTION)
    #     glPopMatrix()
    #     glMatrixMode(GL_MODELVIEW)
    #     # print(x, y)
    #     # print(buff)
    #     # print(viewport)
    #     near = 1
    #     for i in hits:
    #         if len(i.names) != 0 and i.near < near:
    #             self.selected = i.names[0] - 100 # sub dummy offset 100
    #             near = i.near
    #     #     print(i.names, i.near, i.far)
    #     # print(self.selected)
    @staticmethod
    def unProject(x, y):
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


    @staticmethod
    def pointToLineDistance3D(a, b, p):
        line_dir = b - a
        t = (p-a).dot(line_dir)/ line_dir.dot(line_dir)
        direction = a + t*line_dir - p 
        return np.linalg.norm(direction)

    
    # double pointToLineDistance3D(cml::vector3d a, cml::vector3d b, cml::vector3d p)
    # {
    # cml::vector3d lineDirection = b - a;
    # double t = (cml::dot(p-a,lineDirection))/(cml::dot(lineDirection,lineDirection));
    # cml::vector3d direction = ((a + t*lineDirection)-p);
    # return direction.length();
    # }


    # // per-vertex
    # for (int i = 0; i < num_vertice; i++){
    # int v_idx = i;
    # vector3 v = vertices[v_idx];
    # cml::vector3d a, b; unProject(mouseX, mouseY, a, b);
    # double len = pointToLineDistance3D(a,b, cml::vector3d(v[0],v[1],v[2]));
    # IntFourMulitples four(j_idx,c_idx,f_idx,v_idx);
    # distances.push_back(make_pair(four, len));
    # }  


    def get3DPointFromMousePoint(mouseX, mouseY):
         ray_near, ray_far = self.unProject(mouseX, mouseY)
         old_p =  0 # TODO tmp value.
         new_p = np.linalg.norm(old_p-ray_near)/np.linalg.norm(ray_far-ray_near)*(ray_far-ray_near) + ray_near
        #  new_p = new_p / scale_factor 
         new_p = new_p / scale_factor 
    
    @staticmethod
    def get_near_far(mouseX, mouseY):
        pmat = (GLdouble * 16)()
        mvmat = (GLdouble * 16)()
        viewport = (GLint * 4)()
        glGetIntegerv(GL_VIEWPORT, viewport)
        glGetDoublev(GL_PROJECTION_MATRIX, pmat)
        glGetDoublev(GL_MODELVIEW_MATRIX, mvmat)

        x = float(mouseX)
        y = viewport[3] - float(mouseY) - 1

        #print(x,y)
        return Picker.unProject(x, y)

    @staticmethod
# <<<<<<< Updated upstream
#     def pick(x, y, width, height, data):
#         ray = Picker.get_ray(x,y, width, height)
# =======
    def pick(x, y, width, height, proj_mat, cam_mat, data):


        ray = Picker.get_ray(x,y, width, height, proj_mat, cam_mat.dot(data.mat))
        print("ray", ray)
# >>>>>>> Stashed changes
        return data.query_ray(ray)


    @staticmethod
    def get_ray( x, y, res_w, res_h, proj_mat, mv_mat):
        """
        INPUT
            viewport coordinate x, y 
        Return
            world coordinate (x,y,z) ray object
         """
    
    # TMP TODO
        from_point, to_vector = Picker._toNormailzeCoord(x,y, res_w, res_h)
        from_point = Picker._toEyeCoord(from_point, proj_mat)
        from_point = Picker._toModel(from_point, mv_mat)
        to_vector = Picker._toEyeCoord(to_vector, proj_mat)
        to_vector = Picker._toModel(to_vector, mv_mat)
        
        ray = AABB.Ray()
        ray.set_direction(to_vector[:3])
        ray.set_pos(from_point[:3])
        
        return ray

    @staticmethod
    def _toNormailzeCoord( x, y, width, height):
        """
            Pygame viewport coord left   top   is (0,0)
                                  bottom right is X_max, Y_Max

            return from, to
        """

        
        ndc_x = ((x * 2) / width - 1)
# <<<<<<< Updated upstream
#         ndc_y = -((y * 2) / height - 1)

#         return np.arary((ndc_x, ndc_y, 0, 1)).astype(np.float),\
#                 np.array((0,0,1,0)).astype(np.float)
# =======
        # ndc_y = -((y * 2) / height - 1)
        # ndc_y = ((y * 2) / height - 1)
        ndc_y = (((height - y - 1) * 2) / height - 1)

        print("nd x : {}, y : {}".format(ndc_x, ndc_y))

        return np.array((ndc_x, ndc_y, 0, 1)).astype(np.float),\
                np.array((0,0,-1,0)).astype(np.float)
# >>>>>>> Stashed changes

    @staticmethod
    def _toEyeCoord( coord, proj_mat):
        
        # array = (GLfloat *16)()
        
# <<<<<<< Updated upstream
#         glGetFloat(GL_PROJECTION_MATRIX, array)
#         proj = np.array(array).T
#         inv_proj = np.linalg.inv(proj)
# =======
        # glGetFloat(GL_PROJECTION_MATRIX, array)
        # # print(list(array))
        # proj = np.array(array).reshape(4,4).T
        # # print("proj to eye : \n", proj)
        inv_proj = np.linalg.inv(proj_mat)
# >>>>>>> Stashed changes
        reval = inv_proj.dot(coord)
        return reval

    @staticmethod
    def _toModel( coord, mv_mat):
        
        # array = (GLfloat *16)()
        
# <<<<<<< Updated upstream
#         glGetFloat(GL_MODELVIEW_MATRIX, array)
#         mview = np.array(array).T
#         inv_mview = np.linalg.inv(mview)
# =======
        # glGetFloat(GL_MODELVIEW_MATRIX, array)
        # mview = np.array(array).reshape(4,4).T
        # # print("eye to world : \n", mview)
        inv_mview = np.linalg.inv(mv_mat)
# >>>>>>> Stashed changes
        reval = inv_mview.dot(coord)
        return reval
        