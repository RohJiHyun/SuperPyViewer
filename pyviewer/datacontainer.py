

import AABB
class WorldContainer():
    def __init__(self, data):
        pass


class DataContainer():
    """
        based on local coord 
    """
    def __init__(self):
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0

        self.V = None
        self.F = None
        self.is_initialized = False
        self.aabb = AABB.AABBTree()
        self.aabb.insert_entity(self.V, self.F)


    def set_data(self, V, F):
        self.V = V
        self.F = F
        
        

    def update_data(self, updated_data):
        self.data = updated_data


    def rotation_update(self, delta_x, delta_y, delta_z):
        """
            integer
        """
        self.rot_x += delta_x
        self.rot_y += delta_y
        self.rot_z += delta_z


    def get_rotation(self):
        return self.rot

    