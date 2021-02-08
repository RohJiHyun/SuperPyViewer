import pytest

import pyviewer.transforms as trans
import numpy as np 
#GL MDOEL VIEW TRANSFORM and INVERSE TEST

from OpenGL.GL import * 
from OpenGL.GLU import *



def y_axis_transform_test():
    
    pass





def x_axis_transform_test():
    pass



def z_axis_transform_test():
    pass



def xyz_composition_transform_test():
    x = np.arange(3,3).reshape(3,3)
    rot_z, rot_y, rot_x = np.pi/2.0, np.pi/4.0, np.pi/4.0
    rotation_composition = trans.RotationBuilder.make_euler_rotation(rot_z, rot_y, rot_x) # 90 % 45 % 45 degree
    result_trans = rotation_composition * x

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotatef(rot_z, 0, 0, 1)
    glRotatef(rot_y, 0, 1, 0)
    glRotatef(rot_x, 1, 0, 0)

    array2 = (GLfloat *16)()

    glGetFloat(GL_MODELVIEW_MATRIX, array2)
    toworld = np.array(array2).reshape(4,4)
    result_gl = toworld.dot(x)
    assert np.all(result_trans == result_gl), "np.all no"
    assert result_trans==toworld , "diff"