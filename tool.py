#! /usr/bin/python3

import numpy as np


class datatype(object):
    points = np.zeros(shape=(4,2))
    alt = np.zeros(shape=(3,1))
    takeoff = np.zeros(shape=(3,1))
    home = np.zeros(shape=(3,1))
    step_dist = 0
    mode = 0
    
    # userdeflist, user define list =
        # [ 
        #   4 points[xy, xy, xy, xy],  4*2 matrix
        #   alt[min, step, final],     3*1 matrix
        #   takeoff[lat, lot, alt],       3*1 matrix
        #   home[lat, lot, alt],       3*1 matrix
        #   sep_dist                   1*1 matrix
        #   mode                       bool
        # ]
    
    def __init__(self, 
                 points,
                 alt, 
                 takeoff, 
                 home,
                 step_dist, 
                 mode,):
        self.points = points
        self.alt = alt
        self.takeoff = takeoff
        self.home = home
        self.step_dist = step_dist
        self.mode = mode

class wayptsss():
    pass
class waypts_b():
    pass
    

# def temp(z : datatype):
    
#     print(z.points)
    
if __name__ == '__main__':
    x = np.array([0,0,0])
    print(x)
    
    
     # aaa = tool.wayptsss()
        # aaa.f = 1945
        # print(aaa.f)
        # item = [ tool.wayptsss() for i in range(10) ]
        # item[9].a = np.array( [[1,555], [1,4]])
        # print (item[9].a[1])