import pygame
import pygame_gui

class UIListener():
    """
        type
        user_type
        ui_element
        ui_object_id
    """
    def __init__(self):
        self.callback = None 

    def add_click_callback(self, func):
        self.callback = func



class UI():
    def __init__(self, x, y, width, height):
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height
        self.auto = True
    

        self.click_callback = UIListener()


    def resize(self, x,y,width, height):
        pass
    
    def set_layout(self, auto = True):
        """
            if auto is True, stack UI.
        """
        self.auto = auto
        if auto :
            pass
        
    def update(self):
        pass
    
    def attach(self, surface):
        pass

    def detach(self):
        pass

    def draw(self):
        pass
