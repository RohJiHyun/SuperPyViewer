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


#TODO ANIMATION UI CONTROLL CLASS
class AnimeUI():
    pass


class MainUI():
    def __init__(self, x, y, width, height):
        self.x = x 
        self.y = y 
        self.width = width 
        self.height = height
        self.auto = True


        # Main Panel for attch program \
        self.panel = pygame_gui.elements.ui_panel()

        # Name | file_name
        self.status_bar = pygame_gui.elements.
        # translate pos box
        self.xyz_editor = pygame_gui.elements.
        # X Y Z rotation 
        self.xyz_rotation_editor = pygame_gui.elements. 
        # AABB Box
        self.visible_bbox = pygame_gui.elements.UIButton(
                                                        relative_rect=pygame.Rect((0,0),(20,20)),
                                                        text = "Visible",
                                                        manager = self.manager

                                                        )

    

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
        surface.

    def detach(self):
        pass

    def draw(self):
        pass
        
