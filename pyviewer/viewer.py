
import sys 
import numpy as np 
import logging 
import igl

from OpenGL.GL import * 

from OpenGL.GLU import *

# import viewcontrolobj as vco




logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("Viewer Logger")

from pyviewer import datacontainer as dc


from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from pyviewer import ui
from pyviewer import viewcontrolobj as vco 


from pyviewer import controller, data_model

# QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)

# app = QApplication(sys.argv)



import pyviewer.controller as ct 
import pyviewer.data_model as dmodel

QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)
app = QApplication(sys.argv)

class CustomViewer(QMainWindow):
    def __init__(self, title, width, height):
        super().__init__()
        self.resize(width, height)
        # self.layout = BorderLayout()
        self.windows = []
        self.world = dc.WorldContainer()



        self.menu = self.menuBar().addMenu("&File")
        self.menu.addAction('&Open', self.openFile)
        self.menu.addAction('&save', self.saveFile)
        
        # self.initUI()

    def add_window(self, window, isdock=True, name="", allowed_area=Qt.AllDockWidgetAreas, central=False):
        """
            window is QT Window Object. and window_object has lisener
        """
        print("centerla" , central)
        if isdock and not central : 
            dock = QDockWidget(name, self)
            dock.setFloating(False)
            self.windows.append(dock)
            dock.setAllowedAreas(allowed_area)
            dock.setWidget(window)
            dock.widget().setMaximumSize(dock.widget().minimumSize())

            # self.addDockWidget(Qt.RightDockWidgetArea, dock)
            self.addDockWidget(allowed_area, dock)
            
        elif  central:

            self.setCentralWidget(window)
            
    

    def keyPressEvent(self, e):

        if e.key() == Qt.Key.Key_Control:
            self.win.fixed_point_add_flag = True
        elif e.key() == Qt.Key.Key_F:
            self.win.world.data_container_list[0].selected_point_clear()
            
    
    def keyReleaseEvent(self, e):
        
        if e.key() == Qt.Key.Key_Control:
            self.win.fixed_point_add_flag = False
        
            
            


    def initUI(self):
        self.menu = ui.UIMenuBar(self)
        self.menu.initUI()
        self.Inspector = ui.InspectorUI(self)    
        self.Inspector.initUI()
        


    def set_data(self, V, F):
        # self.data.append( (V,F))
        self.world.clear()
        self.world.add_data(dc.DataContainer(V, F))
        
    def compile(self, total_view = 1):
        self._initialize_mainview()
        # self.initUI()

        

        
        # ct.InspectorController(self.win, self.Inspector, dmodel.)
    

    def _initialize_mainview(self):
        self.win = vco.Window("tit")
        self.win.set_world(self.world)
        self.add_window(self.win, isdock=True, name=self.win.name, central=True)
        
    

    def run(self):
                
        self.show()



    def openFile(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Open file', '', "Mesh files (*.obj *.off *.stl *.ply)")
        print(fname)
        if fname[0] :
            V,F = igl.read_triangle_mesh(fname[0])
            self.set_data(V,F)
        
    def saveFile(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save file', '', "Mesh files (*.obj *.off *.stl *.ply)")
        print(fname[0])
        if fname[0]:
            V = self.world.data_container_list[0].V
            F = self.world.data_container_list[0].F
            igl.write_triangle_mesh(fname[0], V, F)
        
    

    def add_picking_function(self, f):
        """
            function args : V, F
        """
        self.win.add_mouse_released_callback(f)
    

    # def mouseMoveEvent(self, pos):
    #     print(pos.x(), pos.y(), "pos is :")







if __name__ == "__main__":
    V, F = igl.read_triangle_mesh("pyviewer/cube.obj")
    V, F = igl.read_triangle_mesh("pyviewer/cube.ply")
    # a = Viewer("title", 800, 900)
    # a.set_data(V,F)
    # a.add_mouse_down_callback(test_mouse)
    # a.add_mouse_up_callback(test_mouse_pop)
    # a.add_mouse_motion_callback(test_mouse_motion)
    # a.launch()
if __name__ == '__main__':

    window = CustomViewer("hee", 800,900)
    window.set_data(V,F)
    window.compile(2)
    window.add_picking_function(lambda x, y : (x, y))
    window.run()




    sys.exit(app.exec_())