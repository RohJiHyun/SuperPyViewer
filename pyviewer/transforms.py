import numpy as np 
class Rotation():
    def __init__(self, init_theta = 0, axis=0, is_affine=True, other_obj = None):
        if other_obj :
            init_theta = other_obj.theta
            axis = other_obj.axis
            is_affine = other_obj.is_affine

        self.theta = init_theta
        self.axis = axis
        self.is_affine = is_affine
        if self.is_affine:
            self.matrix = np.eye(4,4)
        else :
            self.matrix = np.eye(3,3)
    

    def insert_item(self, axis):
        sin = np.sin(self.theta)
        cos = np.cos(self.theta)
        flag = True
        for row_idx in range(3):
            for col_idx in range(3):
                if row_idx == axis or col_idx == axis:
                    continue
                else : 
                    self.matrix[row_idx, col_idx] = cos if flag else sin
                    flag != flag
                    



    def __call__(self, x):
        if isinstance(x, Rotation):
            return self.matrix.dot(x.matrix)
        return self.matrix.dot(x)

    def __add__(self, other):
        """
            must be added with same axis rotation object.
            return New Rotation Object.
        """
        assert self.axis == other.axis, "they have different axis"
        return Rotation(init_theta=self.theta + other.theta)
    

    def __mul__(self, other):
        """
            x * y : (y numpy obj)
        """
        mat = None
        if isinstance(other, Rotation):
            mat = self.matrix.dot(other.matrix)
        else : 
            mat = self.matrix.dot(other)
        return mat

    def __imul__(self, other):
        #TODO
        pass
        
class RotationBuilder():
    """
        Rotation Matrix Builder
    """
    def __init__(self):
        pass

    @staticmethod
    def make_euler_rotation(x_rad=0, y_rad=0, z_rad=0, axis_list = [0,1,2]):
        reval = Rotation()
        rads = [x_rad, y_rad, z_rad]
        for axis in axis_list:
            reval *= Rotation(rads[axis], axis)
        
        return reval
        