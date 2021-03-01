from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

import copy
import igl
import sys
import os 




from pyviewer import datacontainer as dc 

class BaseDataFlowModel(QObject):
    def __init__(self):
        super().__init__()



    

    def compile(self):
        pass



class GlboalWorldModel(BaseDataFlowModel):
    def __init__(self, world):
        super(self, BaseDataFlowModel).__init__()
        self.world = world



    def open_file(self, filename="pyviewer/cube.obj"):
        if not os.path.isabs(filename):
            filename=os.path.abspath(filename)

        V, F = igl.read_triangle_mesh(filename)
        self.world.add_data(dc.DataContainer(V,F))

    def save_data(self, filename="./test"):
        if not os.path.isabs(filename):
            filename=os.path.abspath(filename)

        
        


class LocalWorldModel(BaseDataFlowModel):
    def __init__(self, g_model):
        super().__init__()
        self.world = g_model.world
        self.ref_world = update_from_ref()

        



    def _copy(self, obj):
        
        ref_world = copy.deepcopy(obj.world)
        return ref_world

    def update_from_ref(self):
        self.ref_world = self._copy(self.world)
        return self.ref_world



    def update_local_data(self, rotation):
        
        pass



    def update_face_data(self, s):
        pass