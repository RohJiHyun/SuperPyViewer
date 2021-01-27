from operator import itemgetter, attrgetter
import numpy as np 
class BaseTree():

    def __init__(self):  
        self.is_initialized = False
        self.x_min = 0
        self.x_max = 0
        self.y_min = 0
        self.y_max = 0
        self.z_min = 0
        self.z_max = 0

    def overlaped(self, otherObj):
        return False

    def add_data(self, *args):
        pass

class AABBLeaf(BaseLeaf):
    """
    Primitive : Triangle.
    """
    def __init__(self):
        super().__init__()
        self.f_idx = None

    def add_data(self, f_idx, *args):
        """
            args : v1, v2, v3...
            v{n} is 3-dims vector.
        """
        self.f_idx = f_idx
        assert len(args) == 3, "args list size is Not 3..."
        self.v1 = v1 = args[0]
        self.v2 = v2 = args[1]
        self.v3 = v3 = args[2]
        X = 0
        Y = 1
        Z = 2
        self.x_min = min(v1[X], v2[X], v3[X])
        self.x_max = max(v1[X], v2[X], v3[X])
        self.y_min = min(v1[Y], v2[Y], v3[Y])
        self.y_max = max(v1[Y], v2[Y], v3[Y])
        self.z_min = min(v1[Z], v2[Z], v3[Z])
        self.z_max = max(v1[Z], v2[Z], v3[Z])
        return self

    def overlaped(self, otherObj):
        x_axis_overlaped = False
        y_axis_overlaped = False
        z_axis_overlaped = False
        if self.x_max > otherObj.x_min or self.x_min < otherObj.x_max:
            x_axis_overlaped = True
        if self.y_max > otherObj.y_min or self.y_min < otherObj.y_max :
            y_axis_overlaped = True
        if self.z_max > otherObj.z_min or self.z_min < otherObj.z_max :
            z_axis_overlaped = True
        
        return x_axis_overlaped and y_axis_overlaped and z_axis_overlaped

        # return True or False
    

    # TODO Not Needed Now.    
    def intersect(self, otherObj):
        pass

    def merge(self, otehrObj):
        pass
    
    
    


class AABBTree(BaseTree):
    """
    Bounding Volume Hierarchy Class
    primitive : Triangle.

    """
    MIN_OBJECTS_PER_LEAF = 1

    def __init__(self):
        super().__init__()
        self.data = None
        self.left = None 
        self.right = None

     


        
        


    def insert_entity(self, V, F):
        
        self.V = V 
        self.F = F
        aabb_leaf_list = []
        assert len(self.F) != 0, "Face size is 0 ..."
        for f_idx, face_v_idx in enumerate(self.F) : 
            # f_idx, face_idx := {v_idx1, v_idx2, v_idx3}
            aabb_leaf_list.append(AABBLeaf().add_data(f_idx, *face_v_idx))


        self._insert(aabb_leaf_list)



    
    def _insert(self, aabb_leaf_list):
        """ 
            recursive Method : 
            stop condtion : aabb_leaf_list is 0

        """
        def compute_bound_volume(aabb_leaf_list):
            aabb_leaf = aabb_leaf_list[0]
            min_x = aabb_leaf.min_x
            max_x = aabb_leaf.max_x
            min_y = aabb_leaf.min_y
            max_y = aabb_leaf.max_y
            min_z = aabb_leaf.min_z
            max_z = aabb_leaf.max_z
            

            for aabb_leaf in aabb_leaf_list[1:]:
                min_x = min(aabb_leaf.min_x, min_x)
                max_x = max(aabb_leaf.max_x, max_x)
                min_y = min(aabb_leaf.min_y, min_y)
                max_y = max(aabb_leaf.max_y, max_y)
                min_z = min(aabb_leaf.min_z, min_z)
                max_z = max(aabb_leaf.max_z, max_z)
            return min_x, max_x, min_y, max_y, min_z, max_z
        self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max = compute_bound_volume(aabb_leaf_list)
        
        object_size = len(aabb_leaf_list)
        assert object_size > 0, "aabb_leaf_list is empty!"
        # 0~1
        if object_size <= AABBTree.MIN_OBJECTS_PER_LEAF : 
            self.data = aabb_leaf_list[0]
        else : 
            tmpTree = AABBTree()

            aabb_leaf_list, p_k = partition(aabb_leaf_list)

            self._insert(aabb_leaf_list[    : p_k ])
            self._insert(aabb_leaf_list[p_k :     ])

    def partition(self, aabb_leaf_list):
        """

        """
        #pick first, longest axis.
        # this axis will become a pivot for cutting the plane.
        axis_term = 0
        axis_length = 0 
        axis_min = 0
        axis_max = 0
        x_length = self.x_max - self.x_min
        y_length = self.y_max - self.y_min
        z_length = self.z_max - self.z_min
        l=  [['x',x_length, self.x_max, self.x_min],
            ['y',y_length, self.y_max, self.y_min],
            ['z',z_length, self.z_max, self.z_min]]
        l = sorted(l, key=itemgetter(1) )
        key = l[-1]
        divider = self.x_min + x_length/2

        left_list = []
        right_list = []
        for leaf in aabb_leaf_list:
            axis_min = getattr(leaf, "{}_min".format(key[0]))
            axis_max = getattr(leaf, "{}_max".format(key[0]))
            left =  abs(divider - axis_min) 
            right = abs(divider - axis_max)
            if left > right :
                left_list.append(leaf)
            else : 
                right_list.append(leaf)

        return left_list.extend(right_list), len(left_list)
        
        
        
    def intersect(self, otherObj):
        pass
    
    def merge(self, otherObj):
        pass
    
    def overlaped(self, otherObj):
        self.other


    ##################
    def query(self):
        pass
    
    def test_draw(self):
        pass


if __name__ == "__main__":
    a = AABBLeaf()