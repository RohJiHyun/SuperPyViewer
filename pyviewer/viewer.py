
import sys, pygame 
from pygame.locals import * # Local Key Value and Mod Constant initialize
import numpy as np 
import logging 
import igl

from OpenGL.GL import * 

from OpenGL.GLU import *

import viewcontrolobj as vco
#CUSTOM SETTINGS.
# from pyviewer.viewcontrolobj import  (Light, Material)



logging.basicConfig(level=logging.INFO)
# logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("Viewer Logger")


verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

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



    def set_data(self, V, F):
        self.data.append( (V,F))
        




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
                return function(event.x, event.y)
            elif event.type in [KEYUP, KEYDOWN]:
                print(event , event.key)
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
        self.callback_table[MOUSEBUTTONMOTION] = self._callback_wrapper(callback)


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

        glClearColor(0.,0.,0.,0.)
        # glShadeModel(GL_FLAT)
        self.light = vco.Light()
        self.light.initialize()
      

        self.material = vco.Material()
        self.material.initialize()
        self.material()



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
        print(event, "test")
        logger.debug("event_hadler : {}".format(event.type))
        if event.type in self.callback_keys:
            self.callback_table[event.type](event)
    
    def __tmp_render_function(self, V=None, F = None):
        (V, F) = self.data[0]
        def calc_face_normal(idx1, idx2, idx3):
            # print("idx is {} {} {} ".format(idx1, idx2, idx3))
            edge1 = V[idx2] - V[idx1]
            edge2 = V[idx3] - V[idx1]
            normal_vector = np.cross(edge1, edge2)
            glNormal3fv(list(normal_vector))
            
        
        
        glRotatef(1.0,.0,1.,0)
        glRotatef(0.5,.1,0.,0)

        glBegin(GL_TRIANGLES)

        for face_v_idx in F:
            calc_face_normal(*face_v_idx)
            for v_idx in face_v_idx:
                
                glVertex3fv(list(V[v_idx]))
        glEnd()

    def _render_object(self):
        for data_object in self.data:
            pass
        self.__tmp_render_function()
    

    def _render__other_UI(self):
        pass

    def launch(self):
        self._initialize()
        import time
        # do something
        self.loop_state = True
        
        gluPerspective(45, ( self.width / self.height ), 0.1, 50.)
        glTranslatef(0.,0.,-5)
        
        while self.loop_state:
            for event in pygame.event.get():
                logger.debug("event is : {}".format(event))
                self._event_hanler(event)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # self.Cube()
            self._render_object()
            self._render__other_UI()                





            # self.screen.blit(self.background, (0, 0))
            pygame.display.flip()
            pygame.time.wait(10)

        print("end")
        self._finalize()



    # def __str__(self):
    #     return "Hello. shawnegade."


class CustomViewer(Viewer):
    pass
    






if __name__ == "__main__":
    V, F = igl.read_triangle_mesh("./cube.obj")
    a = Viewer("title", 800, 900)
    a.set_data(V,F)
    a.launch()
