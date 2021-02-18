
import sys, pygame 
# from pygame.locals import * # Local Key Value and Mod Constant initialize
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



import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QDockWidget, QListWidget)
from PyQt5.QtCore import Qt
from pyviewer import ui
from pyviewer import viewcontrolobj as vco 



class CustomViewer(QMainWindow):
    def __init__(self, title, width, height):
        super().__init__()
        self.resize(width, height)
        self.windows = []
        self.world = dc.WorldContainer()
        self.initUI()

    def add_window(self, window, isdock=True, name=""):
        """
            window is QT Window Object. and window_object has lisener
        """
        if isdock : 
            dock = QDockWidget(name, self)
            dock.setFloating(False)
            self.windows.append(dock)
            self.addDockWidget(Qt.RightDockWidgetArea, dock)
            dock.setWidget(window)


    def initUI(self):
        self.menu = ui.UIMenuBar(self)
        self.menu.initUI()
        self.Inspector = ui.InspectorUI(self)    
        self.Inspector.initUI()


    def set_data(self, V, F):
        # self.data.append( (V,F))
        self.world.add_data(dc.DataContainer(V, F))
        
    def compile(self):
        self._initialize()


    def _initialize(self):
        win = vco.Window("tit")
        win.set_world(self.world)
        self.add_window(win, isdock=True, name=win.name)
    


    def add_menubar(self):
        pass

    def run(self):
        self.show()
    

    # def mouseMoveEvent(self, pos):
    #     print(pos.x(), pos.y(), "pos is :")







if __name__ == "__main__":
    V, F = igl.read_triangle_mesh("pyviewer/cube.obj")
    # a = Viewer("title", 800, 900)
    # a.set_data(V,F)
    # a.add_mouse_down_callback(test_mouse)
    # a.add_mouse_up_callback(test_mouse_pop)
    # a.add_mouse_motion_callback(test_mouse_motion)
    # a.launch()
if __name__ == '__main__':
    QApplication.setAttribute(Qt.AA_UseDesktopOpenGL)

    app = QApplication(sys.argv)
    window = CustomViewer("hee", 800,900)
    window.set_data(V,F)
    window.compile()
    window.run()

    sys.exit(app.exec_())