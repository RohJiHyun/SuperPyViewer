class DataContainer():
    def __init__(self):
        self.rot_x = np.eye((3,3))
        self.rot_y = np.eye((3,3))
        self.rot_z = np.eye((3,3))

        self.V = None
        self.F = None
        self.is_initialized = False

    def set_data(self, V, F):
        self.V = V
        self.F = F
        
        

    def update_data(self, updated_data):
        self.data = updated_data


    def rotation_update(self, delta_x, delta_y, delta_z):
        self.rot_x += delta_x
        self.rot_y += delta_y
        self.rot_z += delta_z


    def get_rotation(self):
        return self.rot

    