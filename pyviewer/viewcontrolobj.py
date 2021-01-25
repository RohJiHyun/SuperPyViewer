import numpy as np 


# NEED GL BUILDER 
class Light():
    def __init__(self, ambient, diffuse, specular):
        self.direcion = [0., 0., -1.]
        self.set_ambient(ambient)
        self.set_diffuse(diffuse)
        self.set_specular(specular)

    

    def set_coeff(self, constant =1.0, linear = 0.09, quadratic = 0.032):
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic


    def set_ambient(self, ambient):
        self.ambient = ambient
        return self 


    def set_diffuse(self, diffuse):
        self.diffuse = diffuse
        return self

    def set_specular(self, specular):
        self.specular = specular
        return self
    
    def initialize(self):

        glLightfv(GL_LGIHT0, GL_AMBIENT, self.ambient)
        glLightfv(GL_LGIHT0, GL_DIFFUSE, self.diffuse)
        glLightfv(GL_LGIHT0, GL_SPECULAR, self.specular)
        #glLightfv(GL_LGIHT0, GL_POSITION, self.position)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

class Material():
    def __init__(self):
        pass

    def set_ambient(self, ambient):
        self.ambient = ambient
        return self
    def set_diffuse(self, diffuse):
        self.diffuse = diffuse
        return self
    def set_specular(self, specular):
        self.specular = specular
        return self

    def set_shininess(self, shininess):
        self.shininess = shininess
        return self
    

    def initialize(self):
        pass
    

    def __call__(self):
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, self.ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, self.specular)
        glMaterialfv(GL_FRONT_AND_BACK)
        glMaterialfv(GL_FRONT_AND_BACK)
        

class VCOCollection():
    """
        View Controll Object Collection Class 


        Controll Cam_lists, Viewer State
    """
    def __init__(self):
        self.cam_list = []
        self.
    

    def read_default_yaml(self, file_name):
        pass

class LayoutOptions():
    def __init__(self):
        pass

    def set_layout(self):
        pass
class GL_Options():
    def __init__(self):
        pass
    

class RootWindow():
    def __init__(self, x, y, width, height, title = None):
        if title == None : 
            title = "No Title"
        self.title = title
        self.set_layout(1,1)

        self.child_group = [[]]
        
        
        
        
    def _set_xywh(self, x, y, width, height):
        cond_function = labmda x : x > 0
        def _set_attribute(x, func):
            if func(x):
                return x
        self.width =  _set_attribute(width, cond_function )
        self.height = _set_attribute(height, cond_function )
        self.x = _set_attribute(x, cond_function )
        self.y = _set_attribute(y, cond_function )

    def reshape(x, y, width, height):
        
        self._set_attribute(x,y,width,height)
        child_width = width / self.cols
        child_height = height / self.rows

        for group_idx, group in enumerate(self.child_group):
            map_col = (group_idx) % self.cols # 0 ~ n - 1 
            map_row = (group_idx) // self.rows  # 0 ~ n - 1
            for window in group :
                window.reshape(x + map_col * child_width, y + map_row * child_height, child_width, child_height)
    

    def draw(self):
        pass

        



    def set_layout(self, rows, cols):
        self.rows = self.rows
        self.cols = self.cols
    

    
    

class Window():
    """
        Class Window Draw World. 
    """
    WIN_NUM = 0
    def __init__(self, viewer_name = None):
        if name == None : 
            name = "NoNameW_" +str(WIN_NUM)
            Window.WIN_NUM += 1
        self.name = name
        self.camera = Camera()

    def reshape(self,x,y, w, h):
        self._set_xywh(self, x, y, w, h)
        
        
    def _set_xywh(self, x, y, width, height):
        cond_function = labmda x : x > 0
        def _set_attribute(x, func):
            if func(x):
                return x
        self.width =  _set_attribute(width, cond_function )
        self.height = _set_attribute(height, cond_function )
        self.x = _set_attribute(x, cond_function )
        self.y = _set_attribute(y, cond_function )

    def draw(self):
        pass


class Camera():
    
    CAM_NUM = 0
    def __init__(self):
        self.cam_pos = [0,0,0]
        self.cam_direct = [0.,0.,-1.]
        self.cam_normal_direction = [0.,1.,0.]
    
    def set_name(self, name=None):
        if name == None : 
            name = "NoNameCam_"+str(Camera.CAM_NUM)
            Camera.CAM_NUM += 1
        self.name = name

    def set_campos(self, x, y, z):
        self.cam_pos[0] = x
        self.cam_pos[1] = y
        self.cam_pos[2] = z

    def update_campos(self, delta_x, delta_y, delta_z):
        self.cam_pos += delta_x
        self.cam_pos += delta_y
        self.cam_pos += delta_z
    
    def set_direction(self, x, y, z):
        if not [(self.cam_pos[x] + self.cam_pos[y] +self.cam_pos[z] - x - y - z) == 0 ]:
            self.cam_direct[x] = x 
            self.cam_direct[y] = y
            self.cam_direct[z] = z

    def __call__(self):
        return self.cam_pos, self.cam_direct, cam_normal_direction

if __name__ == "__main__":
    pass