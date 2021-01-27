from operator import itemgetter, attrgetter
import numpy as np 
class Ray():
    def __init__(self):
        pass

    def set_pos(self, pos):
        self.pos = pos
        return self
    def set_direction(self, direcion):
        self.direction = direcion
        return self

    def __call__(self, x):
        """
            x is integer
        """
        return self.pos + self.direction * x

    


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

class AABBLeaf(BaseTree):
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
        print(v1[X], v2[X], v3[X])
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

    def intersect_ray(self, ray):
        """
            ray := pos + direct * t
            point inside triangle P := A + vB + wC #each A,B,C vertex point, u + v + w = 1
            return (flag, barycentric coordinate[w, u, v])
        """
        e1 = self.v2 - self.v1 # let's Consdier as B
        e2 = self.v3 - self.v1 # let's Consider as C
        normal = np.cross(e1, e2)
        parallelogram_area = np.linalg.norm( normal )
        triangle_area = parallelogram / 2 

        angle = normal.dot(ray.direction)
        tmp_Epsilon = 0.00001
        if abs(angle) < tmp_Epsilon: #if parallel ... they don't intersect.
            return False
        

        d = normal.dot(self.v1)


        t = ( normal.dot(ray.pos) + d ) / angle
        if t<0 :
            return False, None

        P = ray.pos + t * ray.direction


        e1 = self.v2-self.v1
        vp1 = P - self.v1
        C1 = np.cross(e1, vp1)

        if normal.dot(C1) <0:
            return False, None

        e2 = self.v3 - self.v2 
        vp2 = P - self.v2
        C2 = np.cross(e2, vp1)
        u = np.linalg.norm(C2) / triangle_area
        if normal.dot(C2) < 0 :
            return False, None

        e3 = self.v1 - self.v3
        vp3 = P - self.v2
        C3 = np.cross(e3, vp3)
        v = np.linalg.norm(C3) / triangle_area
        if normal.dot(C3) < 0 :
            return False, None
        


        return True, (1 - u - v , u, v)









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
        print("initialize AABB Tree ...")
        self.V = V 
        self.F = F
        aabb_leaf_list = []
        assert len(self.F) != 0, "Face size is 0 ..."
        for f_idx, face_v_idx in enumerate(self.F) : 
            # f_idx, face_idx := {v_idx1, v_idx2, v_idx3}
            aabb_leaf_list.append(AABBLeaf().add_data(f_idx, *self.V[face_v_idx]))


        self.insert_primitive(aabb_leaf_list)
        print("AABB Tree end...")


    
    
    def insert_primitive(self, aabb_leaf_list):
        """ 
            recursive Method : 
            stop condtion : aabb_leaf_list is 0

        """
        def compute_bound_volume(aabb_leaf_list):
            aabb_leaf = aabb_leaf_list[0]
            min_x = aabb_leaf.x_min
            max_x = aabb_leaf.x_max
            min_y = aabb_leaf.y_min
            max_y = aabb_leaf.y_max
            min_z = aabb_leaf.z_min
            max_z = aabb_leaf.z_max
            

            for aabb_leaf in aabb_leaf_list[1:]:
                min_x = min(aabb_leaf.x_min, min_x)
                max_x = max(aabb_leaf.x_max, max_x)
                min_y = min(aabb_leaf.y_min, min_y)
                max_y = max(aabb_leaf.y_max, max_y)
                min_z = min(aabb_leaf.z_min, min_z)
                max_z = max(aabb_leaf.z_max, max_z)
            return min_x, max_x, min_y, max_y, min_z, max_z
        self.x_min, self.x_max, self.y_min, self.y_max, self.z_min, self.z_max = compute_bound_volume(aabb_leaf_list)
        
        object_size = len(aabb_leaf_list)
        print("obj size : " ,object_size)
        assert object_size > 0, "aabb_leaf_list is empty!"
        # 0~1
        if object_size <= AABBTree.MIN_OBJECTS_PER_LEAF : 
            self.data = [aabb_leaf_list[0]]
        else : 
            self.leftTree = AABBTree()
            self.rightTree = AABBTree()
            aabb_leaf_list, p_k = self.partition(aabb_leaf_list)
            self.leftTree.insert_primitive(aabb_leaf_list[    : p_k ])
            self.rightTree.insert_primitive(aabb_leaf_list[p_k :     ])
            

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
        divider = key[-1] + key[1]/2

        left_list = []
        right_list = []
        for leaf in aabb_leaf_list:
            left =  abs(divider - getattr(leaf, "{}_min".format(key[0])))
            right = abs(divider - getattr(leaf, "{}_max".format(key[0])))


            if left > right :
                left_list.append(leaf)
            else : 
                right_list.append(leaf)

        partition_idx = len(left_list)
        left_list.extend(right_list)
        print("right list size : {},, left_list size : {}".format(len(right_list), len(left_list) ))
        print("total size : ", len(left_list), "partition :", partition_idx)
        
        return left_list, len(left_list)
        
        
        
    def intersect(self, otherObj):
        pass
    

    def ray_intersect(self, ray):
        """
            return fid
        """
        
        def is_intersect(ray):
            def swap(x, y, cond = True):
                if cond : 
                    return y, x
                return x,y
            t_min_x = (self.x_min - ray.position[0]) / ray.direction[0]
            t_max_x = (self.x_min - ray.position[0]) / ray.direction[0]
        
            tmin = t_min_x
            tmax = t_max_x 
            tmin, tmax = swap(tmin, tmax, tmin > tmax)



            t_min_y = (self.y_min - ray.position[1]) / ray.direction[1]
            t_max_y = (self.y_min - ray.position[1]) / ray.direction[1]
            
            t_min_y, t_max_y = swap(t_min_y, t_max_y, t_min_y > t_max_y)
            
            if tmin > t_max_y or t_max_y > tmax :
                return False
            if  t_min_y > tmin:
                tmin = t_min_y
            if t_max_y < tmax:
                tmax = t_max_y

            
            t_min_z = (self.z_min - ray.position[2]) / ray.direction[2]
            t_max_z = (self.z_min - ray.position[2]) / ray.direction[2]
            
            t_min_z, t_max_z = swap(t_min_z, t_max_z, t_min_z > t_max_z)
                
            if tmin > t_max_z or t_max_z > tmax :
                return False
            if  t_min_z > tmin:
                tmin = t_min_z
            if t_max_z < tmax:
                tmax = t_max_z

            return True

        value_list = []
        
        if is_intersect(ray):
            if self.data == None :
                value_list1 = self.leftTree.ray_intersect(ray)
                value_list2 = self.rightTree.ray_intersect(ray)
                value_list.extend(value_list1)
                value_list.extend(value_list2)
            else : 
                for leaf in self.data:
                    
                    inter_flag, coord = leaf.intersect_ray(ray)
                    if inter_flag:
                        value_list.append([leaf.f_idx, coord])
                
        
        return value_list
    
    def merge(self, otherObj):
        pass
    
    def overlaped(self, otherObj):
        self.other


    ##################
    def query(self):
        pass
    
    def test_draw(self):
        pass

import igl
if __name__ == "__main__":
    V,F = igl.read_triangle_mesh("pyviewer/cube.obj")
    a = AABBTree().insert_entity(V, F)
