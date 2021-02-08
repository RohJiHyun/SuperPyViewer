import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

# NEED GL BUILDER
import datacontainer

# TODO 
class Picker():

    def __init__(self):
        pass

    def __call__(self, x, y, width, height, data):

        glGetFloat(GL_PROJECTION_MATRIX, array)

        glGetFloat(GL_MODELVIEW_MATRIX, array2)

    def _toNormailzeCoord(self, x, y, width, height):
        """
            Pygame viewport coord left   top   is (0,0)
                                  bottom right is X_max, Y_Max
        """
        ndc_x = ((x * 2) / res_w - 1 * self.w_factor)
        ndc_y = -((y * 2) / res_h - 1 * self.h_factor)
        return ndc_x, ndc_y

    def _toEyeCoord(self, coord, ss):

        pass

    def toModel(self, coord):
        pass