import numpy as np 


# NEED GL BUILDER 

class VCOCollection():
    """
        View Controll Object Collection Class 


        Controll Cam_lists, Viewer State
    """
    def __init__(self):
        self.cam_list = []


    def update_camera_pos(self, delta_pos):
        self.cam_pos += delta_pos
        
    def set_camera_pos(self, new_pos):
        self.cam_pos = new_pos
        


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