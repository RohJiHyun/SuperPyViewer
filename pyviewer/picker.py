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

    @staticmethod
    def pick(x, y, width, height, data):
        ray = Picker.get_ray(x,y, width, height)
        return data.query_ray(ray)


    @staticmethod
    def get_ray( x, y, res_w, res_h):
        """
        INPUT
            viewport coordinate x, y 
        Return
            world coordinate (x,y,z) ray object
         """
    
    # TMP TODO
        from_point, to_vector = Picker._toNormailzeCoord(x,y, res_w, res_h)
        from_point = Picker._toEyeCoord(from_point)
        from_point = Picker._toModel(from_point)
        to_vector = Picker._toEyeCoord(to_vector)
        to_vector = Picker._toModel(to_vector)
        
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
        ndc_y = -((y * 2) / height - 1)

        return np.arary((ndc_x, ndc_y, 0, 1)).astype(np.float),\
                np.array((0,0,1,0)).astype(np.float)

    @staticmethod
    def _toEyeCoord( coord):
        
        array = (GLfloat *16)()
        
        glGetFloat(GL_PROJECTION_MATRIX, array)
        proj = np.array(array).T
        inv_proj = np.linalg.inv(proj)
        reval = inv_proj.dot(coord)
        return reval

    @staticmethod
    def toModel( coord):
        array = (GLfloat *16)()
        
        glGetFloat(GL_MODELVIEW_MATRIX, array)
        mview = np.array(array).T
        inv_mview = np.linalg.inv(mview)
        reval = inv_mview.dot(coord)
        return reval
        