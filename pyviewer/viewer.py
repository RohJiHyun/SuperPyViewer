
import sys, pygame 
from pygame.locals import * # Local Key Value and Mod Constant initialize
import numpy as np 
import logging 
import igl

from OpenGL.GL import * 

from OpenGL.GLU import *

# import viewcontrolobj as vco
from pyviewer import viewcontrolobj as vco
#CUSTOM SETTINGS.



logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("Viewer Logger")

from pyviewer import datacontainer as dc



from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QDockWidget, QListWidget)
from PyQt5.QtCore import Qt


class Viewer():

    def __init__(self,title, width=300, height=400):
        self.loop_state = False
        
        self.title = title
        self.width = width
        self.height =height
        self.event_handler = []
        self.callback_table = dict()
        self.camera = np.array([0., 0., -1.])
        self.data = []
        
        #for test
        self.world = dc.WorldContainer()
        self.window = vco.Window()
        self.window.reshape(0,0, self.width, self.height)
    def set_data(self, V, F):
        self.data.append( (V,F))
        self.world.add_data(dc.DataContainer(V, F))
        
        
        




    def add_keypressed_callback(self, key, callback):
        """
            
            callback funtion input args : key value
            
        """
        self.callback_table[KEYDOWN] = self._callback_wrapper(callback)

    def add_keyreleased_callback(self, key, callback):
        """
            
            callback funtion input args : key value
            
        """
        self.callback_table[KEYUP] = self._callback_wrapper(callback)
    

    def _callback_wrapper(self, function):
        def idle_funtion(flag):
            if flag : 
                self.loop_state = not self.loop_state
            return 


        def my_little_function(event):
            """
                event 
            """
            if event.type in [MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP]:
                return function(event.type, *event.pos, self.window, self.world)
            elif event.type in [KEYUP, KEYDOWN]:
                return function(event.key)
            elif event.type == QUIT:
                return idle_funtion(True)
            else : 
                return idle_funtion(False)
        
        return my_little_function


    def add_mouse_motion_callback(self, callback):
        """
            callback : it's function.
            callback funtion input args : (x, y)
        """
        self.callback_table[MOUSEMOTION] = self._callback_wrapper(callback)


    def add_mouse_down_callback(self, callback):
        """
            callback : it's function.
            callback funtion input args : (x, y)
        """
        self.callback_table[MOUSEBUTTONDOWN] = self._callback_wrapper(callback)


    def add_mouse_up_callback(self, callback):
        """
            callback : it's function.
            callback funtion input args : (x, y)
        """
        self.callback_table[MOUSEBUTTONUP] = self._callback_wrapper(callback)

    

    
    def _set_default_exit_callback(self):
        self.callback_table[QUIT] = self._callback_wrapper(lambda : pygame.quit())

    def _update_callback_keys(self):
        return list(self.callback_table.keys())


    def _initialize(self):
        self._set_default_exit_callback()
        self.callback_keys = self._update_callback_keys()
        
        pygame.init()
        # self.screen = pygame.display.set_mode((150, 50))
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL| pygame.DOUBLEBUF)
        pygame.display.set_caption(self.title)

        # glClearColor(0.,0.,0.,0.)
        # glShadeModel(GL_FLAT)
        print("light on")
        self.light = vco.Light()
        self.light.initialize()
        print("light_initialize", self.light)
      

        self.material = vco.Material()
        self.material.initialize()
        # self.material()



        # Fill background
        # background = pygame.Surface(self.screen.get_size())
        # self.background = background.convert()
        # self.background.fill((250, 250, 250))


        # # Display some text
        # self.font = pygame.font.Font(None, 36)
        # self.text = self.font.render("Hello There", 1, (10, 10, 10))
        # self.textpos = self.text.get_rect()
        # self.textpos.centerx = self.background.get_rect().centerx
        # self.background.blit(self.text, self.textpos)
        # # Blit everything to the screen
        # self.screen.blit(background, (0, 0))
        # pygame.display.flip()

    def _finalize(self):
        pygame.quit()

    def _event_hanler(self, event):
        # print(event, "test")
        logger.debug("event_hadler : {}".format(event.type))
        if event.type in self.callback_keys:
            self.callback_table[event.type](event)

    def _render_object(self):

        self.window.draw(self.world)
    


    

    def _render__other_UI(self):
        pass

    def launch(self):
        self._initialize()
        import time
        # do something
        self.loop_state = True
        
        # gluPerspective(45, ( self.width / self.height ), 0.1, 50.)
        # glTranslatef(0.,0.,-5)


        while self.loop_state:
            for event in pygame.event.get():
                logger.debug("event is : {}".format(event))
                self._event_hanler(event)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # self.Cube()
            self._render_object()

            pygame.display.flip()
            pygame.time.wait(10)

        print("end")
        self._finalize()



    # def __str__(self):
    #     return "Hello. shawnegade."

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QDockWidget, QListWidget)
from PyQt5.QtCore import Qt
from pyviewer import ui
from pyviewer import viewcontrolobj as vco 
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.resize(800, 600)

		dockWidget = QDockWidget('Dock', self)

		self.textEdit = QTextEdit()
		self.textEdit.setFontPointSize(16)

		self.listWidget = QListWidget()
		self.listWidget.addItem('Google')
		self.listWidget.addItem('Facebook')
		self.listWidget.addItem('Microsoft')
		self.listWidget.addItem('Apple')
		self.listWidget.itemDoubleClicked.connect(self.get_list_item)

		dockWidget.setWidget(self.listWidget)
		dockWidget.setFloating(False)

		self.setCentralWidget(self.textEdit)
		self.addDockWidget(Qt.RightDockWidgetArea, dockWidget)

	def get_list_item(self):
		self.textEdit.setPlainText(self.listWidget.currentItem().text())






class CustomViewer(QMainWindow):
    def __init__(self, title, width, height):
        super().__init__()
        self.resize(width, height)
        self.windows = []
        self.world = dc.WorldContainer()


    def add_window(self,window, isdock=True):
        """
            window is QT Window Object. and window_object has lisener
        """
        if isdock : 
            win = QDockWidget(window.name, self)
            win.setFloating(False)
            self.windows.append(win)
            self.addDockWidget(Qt.RightDockWidgetArea, win)
    
    def set_data(self, V, F):
        # self.data.append( (V,F))
        self.world.add_data(dc.DataContainer(V, F))
        
    def compile(self):
        self._initialize()


    def _initialize(self):
        win = vco.Window("tit")
        win.set_world(self.world)
        self.add_window(win)
    
    def add_menubar(self):
        pass

    def run(self):
        self.show()
    





test_mode = False
tty = False
def test_mouse(e_type, x, y, window, world):
    if e_type == MOUSEBUTTONDOWN:
        global test_mode 
        test_mode = True
        ray = window.get_ray(x,y)
        print(ray)
        fid, b_coord, closest_v_idx, t = world.data_container_list[0].query_ray(ray)
        if fid == -1 : 
            global tty 
            tty = True
            return 
        world.data_container_list[0].selected_v_idx.append(closest_v_idx)


def test_mouse_pop(e_type, x, y, window, world):
    if e_type == MOUSEBUTTONUP:
        global test_mode
        test_mode = False
        global tty
        tty = False
        
        world.data_container_list[0].selected_v_idx.clear()



def test_mouse_motion(e_type, x, y, window, world):
    if  tty and test_mode:
        change = pygame.mouse.get_rel()
        # print(change, "change ")
        
        # ray = window.get_ray(x,y)
        
        # fid, b_coord, closest_v_idx, t = world.data_container_list[0].query_ray(ray)
        # if not fid == -1:
        #     return
        ratio = 0.1
        world.data_container_list[0].rotation_update( -ratio * change[1], -ratio * change[0], 0)
        
    

    
        


if __name__ == "__main__":
    V, F = igl.read_triangle_mesh("pyviewer/cube.obj")
    # a = Viewer("title", 800, 900)
    # a.set_data(V,F)
    # a.add_mouse_down_callback(test_mouse)
    # a.add_mouse_up_callback(test_mouse_pop)
    # a.add_mouse_motion_callback(test_mouse_motion)
    # a.launch()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CustomViewer("hee", 800,900)
    window.set_data(V,F)
    window.compile()
    window.run()

    sys.exit(app.exec_())