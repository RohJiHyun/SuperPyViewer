import numpy as np 



def make_matrix(angle, axis):
    """
        axis = 0 z
        axis = 1 y
        axis = 2 x
    """
    sin = np.sin(angle)
    cos = np.cos(angle)
    def _rot_z():
        return np.array([
                        [ cos,-sin,  0,  0],
                        [ sin,  cos,  0, 0],
                        [  0,     0,  1, 0],
                        [  0,     0,  0, 1]
                        ]).astype(np.float32)
    def _rot_y():
        return np.array([[ cos, 0,sin, 0],
                         [   0, 1,  0, 0],
                         [-sin, 0,cos, 0],
                         [   0, 0,  0, 1]
                        ]).astype(np.float32)
    def _rot_x():
        return np.array([
                        [  1,  0,   0, 0],
                        [  0,cos,-sin, 0],
                        [  0,sin, cos, 0],
                        [  0,  0,   0, 1]
                        ]).astype(np.float32)
    
    if axis == 0:
        return _rot_z()
    elif axis==1:
        return _rot_y()
    elif axis == 2:
        return _rot_x()
    else:
        return np.eye(4,4)

class Rotation():
    def __init__(self, init_theta = 0, axis=0, is_affine=False, other_obj = None):
        if other_obj :
            init_theta = other_obj.theta
            axis = other_obj.axis
            is_affine = other_obj.is_affine

        self.theta = init_theta
        self.axis = axis
        self.is_affine = is_affine
        self.matrix = make_matrix(init_theta, axis)
        if not self.is_affine:
            self.matrix = self.matrix[:3, :3]
        

        print(self.matrix)
            
        
    



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
        matrix=self.matrix
        if isinstance(other, Rotation):
            mat = self.matrix.dot(other.matrix)
        elif isinstance(other, np.ndarray) : 
            
            if other.shape[0] != self.matrix.shape[-1] :
                matrix = self.matrix[:3, : 3] # 3X3
                print("what mat", mat)
            
            mat = matrix.dot(other)
        return mat

    def __imul__(self, other):
        #TODO
        self.matrix = self.matrix.dot(other.matrix)
        return self
        
    
    def __str__(self):
        return "rot_mat : {}".format(self.matrix)
class RotationBuilder():
    """
        Rotation Matrix Builder
    """
    def __init__(self):
        pass

    @staticmethod
    def make_euler_rotation(z_rad=0, y_rad=0, x_rad=0, axis_list = [0,1,2]):
        reval = Rotation()
        rads = [z_rad, y_rad, x_rad]
        for axis in axis_list:
            reval *= Rotation(rads[axis], axis)
        
        
        return reval


    def euler_to_qt(self, eul_mat):
        # TODO
        pass



if __name__ == "__main__":
    reval = RotationBuilder.make_euler_rotation(10, 20, 30)
    
    print(reval)