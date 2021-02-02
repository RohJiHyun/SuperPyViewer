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

    def __str__(self):
        return "pos : {}, dir : {}".format(self.pos, self.direction)

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
    def get_centroid(self):
        return (self.v1 + self.v2 + self.v3)/3

    # TODO Not Needed Now.    
    def intersect(self, otherObj):
        pass

    def intersect_ray(self, ray):
        """
            ray := pos + direct * t
            point inside triangle P := A + vB + wC #each A,B,C vertex point, u + v + w = 1
            return (flag, barycentric coordinate[w, u, v]), t
            if t < 0, it is back trangle from the ray start direction
            if t > 0, it is front triangle from the ray start direction
        """
        e1 = self.v2 - self.v1 # let's Consdier as B
        e2 = self.v3 - self.v1 # let's Consider as C
        normal = np.cross(e1, e2)
        parallelogram_area = np.linalg.norm( normal )
        triangle_area = parallelogram_area / 2 

        angle = normal.dot(ray.direction)
        tmp_Epsilon = 0.00001
        if abs(angle) < tmp_Epsilon: #if parallel with plane, and 90 degree with normal vector  ... they don't intersect.
            return False, None, None, -1
        

        d = -normal.dot(self.v1)


        t = -( normal.dot(ray.pos) + d ) / angle
        if t<0 : # IF T < 0, IT IS BACK SIDE OF RAY.
            return False, None, None, t

        P = ray.pos + t * ray.direction


        e1 = self.v2 - self.v1
        vp1 = P - self.v1
        C1 = np.cross(e1, vp1)
        C1_tri_area = np.linalg.norm(C1)/2
        w = C1_tri_area / triangle_area

        if normal.dot(C1) <0:
            return False, None, None, t

        e2 = self.v3 - self.v2 
        vp2 = P - self.v2
        C2 = np.cross(e2, vp2) # this is not tri area.
        C2_tri_area = np.linalg.norm(C2)/2
        u = C2_tri_area / triangle_area
        if normal.dot(C2) < 0 :
            return False, None, None, t

        e3 = self.v1 - self.v3
        vp3 = P - self.v3
        C3 = np.cross(e3, vp3)
        C3_tri_area = np.linalg.norm(C3)/2
        v =  C3_tri_area / triangle_area
        if normal.dot(C3) < 0 :
            return False, None, None, t
        
        # 1- u - v = w <= 1
        # u + v <= 1
        return True, (1 - u - v , u, v), self.get_closest_idx(ray,*(1 - u - v , u, v)), t







    def convert_eclidian_coordinate(self, w, u, v):
        return self.v1 * w + self.v2 *w + self.v3 * v


    def get_closest_idx(self, ray, w, u, v):
        def line_equation(ray, point):
            # np.abs(ray.direction.dot(point) + ray.pos)/np.sqrt(-1**2 + ray.direction ** 2)
            p = ray.pos
            d = ray.direction 
            edge_pq = point - p 
            edge_dp = d - p
            # cos( Theta )
            edge_cos = edge_pq.dot(edge_dp) / (np.linalg.norm(edge_pq) * np.linalg.norm(edge_dp))
            theta = np.arccos(edge_cos)
            length = np.linalg.norm(edge_pq) * np.sin(theta)

            return length
            # return np.abs(ray.direction.dot(point) + ray.pos)/np.linalg.norm(ray.direction)

        # if w > u :
        #     if w > v :
        #         return 0
        # else :
        #     if u > v :
        #         return 1
        # return 2
        l = []
        a = line_equation(ray, self.v1)
        print(a)

        l.append([0,a])
        a = line_equation(ray, self.v2)
        l.append([1,a])
        a = line_equation(ray, self.v3)
        l.append([2,a])
        l = sorted(l, key=itemgetter(-1))
        print("fool", l)
        print("small one : ", l[0])
        return l[0][0]
                
        


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


    def _partition(self, aabb_leaf_list):
        t_traversal_cost_const = 1
        t_intersect_cost_const = 2
        def cost_function(left_list, right_list):
            
            t_traversal_cost_const + t_intersect_cost_const*len(left_list) + t_intersect_cost_const*len(right_list)
            return 0
        
        def find_lowwer_cost(idx_list):
            pivot = 0
            for pivot in range(len(idx_list)) : 
                pass
                

            
            

        

        def axis_base_partition(axis):
            """
                return sorted indice.
            """
            idx_list = list(range(len(aabb_leaf_list)))
            assert axis == 0 or axis == 1 or axis == 2, "axis is out of size"
            sorted(idx_list, key = lambda idx : aabb_leaf_list[idx].get_centroid()[axis])
            return idx_list
        pivot = 0
        cost = float("inf")
        selected_idx_list = None
        dims = 3
        for axis in range(len(dims)):
            idx_list = axis_base_partition(axis)
            tmp_cost, tmp_pivot = find_lowwer_cost(idx_list)
            if cost  > tmp_cost :
                cost = tmp_cost
                pivot = tmp_pivot
                selected_idx_list = idx_list

                
                
        

    def add_node(aabb_leaf_list):
        
        
        N = len(aabb_leaf_list)
        if N == 1 :
            self.left = aabb_leaf_list[0]
            self.right = None
        if N == 2 : 
            self.left = aabb_leaf_list[0]
            self.right = aabb_leaf_right[1]

    
    
    def insert_primitive(self, aabb_leaf_list, p_x_min = 9999 , p_x_max = 9999, p_y_min = 9999, p_y_max = 9999, p_z_min = 9999, p_z_max = 9999):
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
        checker =   (self.x_min == p_x_min and self.x_max == p_x_max and \
                     self.y_min == p_y_min and self.y_max == p_y_max and \
                     self.z_min == p_z_min and self.z_max == p_z_max)
        print(compute_bound_volume(aabb_leaf_list))

        if checker : 
            self.data = []
            for data in aabb_leaf_list:
                self.data.append(data)
            return

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
            self.leftTree.insert_primitive(aabb_leaf_list[    : p_k ], self.x_min, self.x_max, self.y_min, self.y_max,self.z_min, self.z_max)
            self.rightTree.insert_primitive(aabb_leaf_list[p_k :     ], self.x_min, self.x_max, self.y_min, self.y_max,self.z_min, self.z_max)
            

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
        print(l)
        key = l[-1]
        divider = key[-1] + key[1]/2
        ida = 0
        if l[0] == 'x':
            ida = 0
        elif l[0] == 'y':
            ida = 1
        elif l[0] == 'z':
            ida = 2
        
        print("ida : ", ida)
        left_list = []
        right_list = []
        for leaf in aabb_leaf_list:
            # left =  abs(divider - getattr(leaf, "{}_min".format(key[0])))
            # right = abs(divider - getattr(leaf, "{}_max".format(key[0])))
            # print(leaf.get_centroid())
            centroid = leaf.get_centroid()[ida]
            

            # print(centroid)
            
            if centroid <= divider :
                left_list.append(leaf)
            else : 
                right_list.append(leaf)
        
        partition_idx = len(left_list)
        print("left_list size : {},, right list size : {}".format(len(left_list), len(right_list) ), "partition :", partition_idx)
        
        left_list.extend(right_list)
        
        return left_list, partition_idx
        
        
        
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
            d1= ray.direction[0]
            if d1 == 0:
                d1 = 0.001
            t_min_x = (self.x_min - ray.pos[0]) / d1
            t_max_x = (self.x_max - ray.pos[0]) / d1

            tmin = t_min_x
            tmax = t_max_x 
            tmin, tmax = swap(tmin, tmax, tmin > tmax)


            d2 = ray.direction[1] 
            if d2 == 0:
                d2 = 0.001
            t_min_y = (self.y_min - ray.pos[1]) / d2
            t_max_y = (self.y_max - ray.pos[1]) / d2
            
            t_min_y, t_max_y = swap(t_min_y, t_max_y, t_min_y > t_max_y)
            
            if tmin > t_max_y or t_min_y > tmax :
                return False
            if  t_min_y > tmin:
                tmin = t_min_y
            if t_max_y < tmax:
                tmax = t_max_y
            
            d3 = ray.direction[2] 
            if d3 == 0:
                d3 = 0.001
            t_min_z = (self.z_min - ray.pos[2]) / d3
            t_max_z = (self.z_max - ray.pos[2]) / d3
            
            t_min_z, t_max_z = swap(t_min_z, t_max_z, t_min_z > t_max_z)
                
            if tmin > t_max_z or t_min_z > tmax :
                return False
            if  t_min_z > tmin:
                tmin = t_min_z
            if t_max_z < tmax:
                tmax = t_max_z

            return True

        value_list = []
        print("check intersect ")
        if is_intersect(ray):
            print("intersect check")
            if self.data == None :
                value_list1 = self.leftTree.ray_intersect(ray)
                value_list2 = self.rightTree.ray_intersect(ray)
                if value_list1[-1] != -1:
                    value_list.extend([value_list1])
                if value_list2[-1] !=  -1:
                    value_list.extend([value_list2])
                
            else : 
                for leaf in self.data:
                    
                    inter_flag, coord, closest_v_idx, t_val = leaf.intersect_ray(ray)
                    if inter_flag:
                        value_list.append([leaf.f_idx, coord, closest_v_idx, t_val])
        print(value_list)

        value_list = sorted(value_list, key=itemgetter(-1))
        print(value_list)
        
        #return closest point from ray_position
        if value_list == []:
            return -1, -1, -1, -1
        fid, b_coord, closest_v_idx, t_value = value_list[0]

        return fid, b_coord, closest_v_idx, t_value # Face_idx, Barycentric Coord, t_value
    
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
import os
if __name__ == "__main__":
    print(__file__)
    V,F = igl.read_triangle_mesh("pyviewer/cube.obj")
    
    a = AABBTree()
    a.insert_entity(V, F)
    t = Ray()
    t.set_direction(np.array([0,0,-1]))
    t.set_pos(np.array([0, 0, 1]))
    result = a.ray_intersect(t)
    print(t)
    print(result)


    
