import pygame



class BaseMouseListener():
    """
        Mouse callback function input...
        (x,y)
    """
    def __idle(self, *args):
        pass

    def __init__(self):
        self.mouse_pressed_func = self.__idle
        self.mouse_released_callback = self.__idle
        self.mouse_motion_callback = self.__idle



    def add_mouse_pressed_callback(self, func):
        pass
    def add_mouse_released_callback(self, func):
        pass
    def add_mouse_pressed(self, func):
        pass
    

    




class MouseManager():
    def __init__(self):
        self.mouse_listener_list = []
    

    def process_event(self, event):
        """
            event is pygame event.
        """

        pass

    def _mouse_released(self, event):
        pass

    def _mouse_pressed(self, event):
        pass

    def _mouse_motion(self, event):
        pass


