#! /usr/bin/python3

import os
import math as ma
from . import tool
import numpy as np



def d2r(degree):
    return ma.radians(degree)

                   
class cpp:
    
    def __init__(self, userdeflist : tool.datatype, filename): 
        
        
        # userdeflist, user define list =
        # [ 
        #   4 points[xy, xy, xy, xy],  4*2 matrix
        #   alt[min, step, final],     3*1 matrix
        #   takeoff[lat, lot, alt],       3*1 matrix
        #   sep_dist                   1*1 matrix
        #   mode                       bool
        # ]
        
        self.__lat = np.array([ [userdeflist.points[0,0]],
                                 [userdeflist.points[1,0]],
                                 [userdeflist.points[2,0]],
                                 [userdeflist.points[3,0]] ])
        
        self.__lon = np.array([ [userdeflist.points[0,1]],
                                 [userdeflist.points[1,1]],
                                 [userdeflist.points[2,1]],
                                 [userdeflist.points[3,1]] ])
        
        self.__alt = np.array([ [userdeflist.alt[0,0]],
                                 [userdeflist.alt[1,0]],
                                 [userdeflist.alt[2,0]] ]) 
            
        self.__takeoff = np.array([ [userdeflist.takeoff[0,0]],
                                  [userdeflist.takeoff[1,0]],
                                  [userdeflist.takeoff[2,0]] ])
        
        self.__home = np.array([ [userdeflist.home[0,0]],
                                  [userdeflist.home[1,0]],
                                  [userdeflist.home[2,0]] ])
        
        self.__step_dist = userdeflist.step_dist
        
        self.__filename = filename
        
        if(userdeflist.mode == True):
            self.__big()
        else:
            self.__sma()
        
    def __sma(self):
        print('small grid')
 
        self.__R = 6371 * 1000
        self.__lat_avg = np.mean(self.__lat)   
        
        self.__delta_lat = self.__R * 2 * ma.pi / 360
        self.__delta_lon = self.__R \
                            * ma.cos( d2r(self.__lat_avg) ) \
                                * 1 /360 * 2 * ma.pi
            
        a = (self.__lat[0,0] - self.__lat[3,0]) * self.__delta_lat
        b = (self.__lon[0,0] - self.__lon[3,0]) * self.__delta_lon
        
        self.__longedge = ma.sqrt(a**2 + b**2)
        
        c = (self.__lat[0,0] - self.__lat[1,0]) * self.__delta_lat
        d = (self.__lon[0,0] - self.__lon[1,0]) * self.__delta_lon
        
        self.__shoredge = ma.sqrt(c**2 + d**2)
        
        self.__alt_elev = ma.ceil( (self.__alt[2,0] - self.__alt[0,0]) / self.__alt[1,0])
        print(self.__alt_elev)
        
# translation & rotation matrix
        self.__transM = np.array([ [ self.__lon[0,0], self.__lat[0,0]] ])   
        
        self.__theta = ma.acos( (self.__lon[3,0] - self.__lon[0,0]) * self.__delta_lon / self.__longedge )    
        
        self.__rotM = np.array([ [ma.cos(self.__theta), -ma.sin(self.__theta)],
                                  [ma.sin(self.__theta),  ma.cos(self.__theta)] ])
        
        
        
        # Mark the input points in local system
        waypts = tool.wayptsss()

        waypts.ref = (np.array( [[0              , 0], 
                                 [0              , self.__shoredge], 
                                 [self.__longedge, self.__shoredge], 
                                 [self.__longedge, 0] ]   ))
        
        
        alpha = ma.acos((87.5 + self.__step_dist) * 0.5 / 87.5)
        
        turnMat_clock = np.array( [ [-ma.sin(alpha)                  , -1 + ma.cos(alpha) - 90/87.5],
                                    [-2 * ma.sin(alpha) - 1 - 90/87.5, self.__step_dist/87.5],
                                    [-ma.sin(alpha)                  , 1 - ma.cos(alpha) + 2 * self.__step_dist/87.5 + 90/87.5],
                                    [0                               , 2 * self.__step_dist/87.5  ] ])
        
        turnMat_ctclk = np.array( [ [ma.sin(alpha)                  , -1 + ma.cos(alpha) - 90/87.5],
                                    [2 * ma.sin(alpha) + 1 + 90/87.5, self.__step_dist/87.5],
                                    [ma.sin(alpha)                  , 1 - ma.cos(alpha) + 2 * self.__step_dist/87.5 + 90/87.5],
                                    [0                               , 2 * self.__step_dist/87.5  ] ])

        radius = 87.5
        radius_large = 11 * self.__step_dist
        
        # print(turnMat_ctclk)
        
# for even level
        waypts.even_r_local = np.zeros(shape=(10,2)) #local
        waypts.even_r_local[0,:] = waypts.ref[0,:]
        waypts.even_r_local[1:5,:] = waypts.even_r_local[0,:] + turnMat_clock * radius
        waypts.even_r_local[5,:] = waypts.even_r_local[4,:] + np.array([self.__longedge,0])
        waypts.even_r_local[6:10,:] = waypts.even_r_local[5,:] + turnMat_ctclk * radius
        
        waypts.even_b_local = np.zeros(shape=(10,2))
        waypts.even_b_local[0,:] = waypts.ref[3,:] + np.array([0,self.__step_dist])
        waypts.even_b_local[1:5,:]= waypts.even_b_local[0,:] + turnMat_ctclk * radius
        waypts.even_b_local[5,:] = waypts.even_b_local[4,:] - np.array([self.__longedge,0])
        waypts.even_b_local[6:10,:] = waypts.even_b_local[5,:] + turnMat_clock * radius
        
        # print(waypts.even_b_local)
        
# for odd level
        waypts.odd_r_local = np.zeros(shape=(10,2)) #local
        waypts.odd_r_local[0,:] = waypts.ref[3,:] + np.array([0,13 * self.__step_dist])
        waypts.odd_r_local[1:5,:] = waypts.odd_r_local[0,:] - turnMat_clock * radius
        waypts.odd_r_local[5,:] = waypts.odd_r_local[4,:] - np.array([self.__longedge,0])
        waypts.odd_r_local[6:10,:] = waypts.odd_r_local[5,:] - turnMat_ctclk * radius
        
        waypts.odd_b_local = np.zeros(shape=(10,2))
        waypts.odd_b_local[0,:] = waypts.ref[0,:] + np.array([0,12 * self.__step_dist])
        waypts.odd_b_local[1:5,:]= waypts.odd_b_local[0,:] - turnMat_ctclk * radius
        waypts.odd_b_local[5,:] = waypts.odd_b_local[4,:] + np.array([self.__longedge,0])
        waypts.odd_b_local[6:10,:] = waypts.odd_b_local[5,:] - turnMat_clock * radius
        
        # print(waypts.odd_r_local)
        
# now get all the waypts for each cycle 
        waypts.evenCyc_local = waypts.even_r_local
        waypts.oddCyc_local = waypts.odd_r_local
        
       
        
        for i in range (1,3):
            tempx1 = waypts.evenCyc_local
            tempx2 = np.array( waypts.even_r_local + np.ones(shape=(10,1)) * np.array([0, 4*i*self.__step_dist]) )             
            
            tempy1 = waypts.oddCyc_local
            tempy2 = np.array( waypts.odd_r_local - np.ones(shape=(10,1))  * np.array([0, 4*i*self.__step_dist]) )
                        
            waypts.evenCyc_local = np.vstack((tempx1, tempx2)) 
            waypts.oddCyc_local = np.vstack((tempy1, tempy2))
        
                
        tempx1 = waypts.evenCyc_local
        tempx2 = np.array(waypts.ref[0,:] + [-87.5, 12 * self.__step_dist])
        waypts.evenCyc_local = np.vstack((tempx1, tempx2))
        tempx1 = waypts.evenCyc_local
        tempx2 = np.array(waypts.ref[0,:] + [-87.5, 1 * self.__step_dist])
        waypts.evenCyc_local = np.vstack((tempx1, tempx2))
        
        tempx1 = waypts.oddCyc_local
        tempx2 = np.array(waypts.ref[3,:] + [87.5, 1 * self.__step_dist])
        waypts.oddCyc_local = np.vstack((tempx1, tempx2))
        tempx1 = waypts.oddCyc_local
        tempx2 = np.array(waypts.ref[3,:] + [87.5, 12 * self.__step_dist])
        waypts.oddCyc_local = np.vstack((tempx1, tempx2))
        
        
        for i in range(1,4):
            tempx1 = waypts.evenCyc_local
            tempx2 = np.array( waypts.even_b_local + np.ones(shape=(10,1)) * np.array([0,4*(i-1)*self.__step_dist]) )
            
            tempy1 = waypts.oddCyc_local
            tempy2 = np.array( waypts.odd_b_local - np.ones(shape=(10,1)) * np.array([0,4*(i-1)*self.__step_dist]))
            waypts.evenCyc_local = np.vstack((tempx1, tempx2)) 
            waypts.oddCyc_local = np.vstack((tempy1, tempy2))        
        
# transform to global
        gwaypts = tool.wayptsss()

        gwaypts.ref = ( np.dot( self.__rotM, np.transpose(waypts.ref) )) \
            / np.array([self.__delta_lon, self.__delta_lat]) [:,None] \
            + np.transpose(self.__transM) * np.ones(shape=(1,waypts.ref.shape[0]))
        gwaypts.ref = np.transpose(gwaypts.ref)
        
        gwaypts.evenCyc = ( np.dot( self.__rotM, np.transpose(waypts.evenCyc_local) )) \
            / np.array([self.__delta_lon, self.__delta_lat]) [:,None] \
            + np.transpose(self.__transM) * np.ones(shape=(1,waypts.evenCyc_local.shape[0]))
        gwaypts.evenCyc = np.transpose(gwaypts.evenCyc)
        
        gwaypts.oddCyc = ( np.dot( self.__rotM, np.transpose(waypts.oddCyc_local) )) \
            / np.array([self.__delta_lon, self.__delta_lat]) [:,None] \
            + np.transpose(self.__transM) * np.ones(shape=(1,waypts.oddCyc_local.shape[0]))
        gwaypts.oddCyc = np.transpose(gwaypts.oddCyc)
        
# get all the path
        
        pathpt = np.transpose(self.__takeoff[:,0])  
        self.__path = pathpt      
        
        pathpt = np.array( [self.__takeoff[0,0], self.__takeoff[1,0], 300])        
        self.__path = np.vstack((self.__path, pathpt))
        
        

        # pathpt = np.stack((gwaypts.evenCyc[:,1], gwaypts.evenCyc[:,0], 301 * np.ones(shape=(gwaypts.evenCyc.shape[0],1))[:,0] ))  
        # pathpt = pathpt.T
        # self.__path = np.vstack((self.__path, pathpt))    
        
        print(self.__alt_elev)
        print(self.__path.shape)

        
        for level in range(0,self.__alt_elev+1):
            height = 300 + level * self.__alt[1,0]
            if level%2 == 0:
                pathpt = np.stack((gwaypts.evenCyc[:,1], gwaypts.evenCyc[:,0], height * np.ones(shape=(gwaypts.evenCyc.shape[0],1))[:,0] ))  
                pathpt = pathpt.T
                self.__path = np.vstack((self.__path, pathpt))                
            else :
                pathpt = np.stack((gwaypts.oddCyc[:,1], gwaypts.oddCyc[:,0], height * np.ones(shape=(gwaypts.oddCyc.shape[0],1))[:,0] ))  
                pathpt = pathpt.T
                self.__path = np.vstack((self.__path, pathpt))  
            print(self.__path.shape)
        
        pathpt = np.array([[gwaypts.oddCyc[0,1], gwaypts.oddCyc[0,0], 200],                                                                 
                               [gwaypts.ref[3,1]   , gwaypts.ref[3,0]   , 200] ])

        # level = level + 1
        
        # print(level)
        
        if level%2 ==0 :
            while height>200:
                pathpt = np.array([[gwaypts.oddCyc[0,1] , gwaypts.oddCyc[0,0] , max(height-120,200)],                                                                 
                                   [gwaypts.ref[3,1]    , gwaypts.ref[3,0]    , max(height-200,200)],
                                   [gwaypts.ref[0,1]    , gwaypts.ref[0,0]    , max(height-320,200)],
                                   [gwaypts.evenCyc[61,1], gwaypts.evenCyc[61,0], max(height-400,200)]])
                self.__path = np.vstack((self.__path, pathpt))  
                height = max(height-400,200)
                
            pathpt = np.array([[gwaypts.oddCyc[0,1], gwaypts.oddCyc[0,0], 200],                                                                 
                               [gwaypts.ref[3,1]   , gwaypts.ref[3,0]   , 200] ])
            self.__path = np.vstack((self.__path, pathpt))  
        else:
            while height>200:
                pathpt = np.array([[gwaypts.ref[0,1]     , gwaypts.ref[0,0]     , max(height-120,200)],                                                                 
                                   [gwaypts.evenCyc[61,1], gwaypts.evenCyc[61,0], max(height-200,200)],
                                   [gwaypts.oddCyc[0,1]  , gwaypts.oddCyc[0,0]  , max(height-320,200)],
                                   [gwaypts.ref[3,1]     , gwaypts.ref[3,0]     , max(height-400,200)]])
                self.__path = np.vstack((self.__path, pathpt))  
                height = max(height-400,200);
        print('-----')
        print(self.__path.shape)
        print('-----')

        
        pathpt = np.array( [self.__takeoff[0,0], self.__takeoff[1,0], 200])  
        self.__path = np.vstack((self.__path, pathpt))  

        pathpt = np.array( [self.__takeoff[0,0], self.__takeoff[1,0], self.__takeoff[2,0]])        
        self.__path = np.vstack((self.__path, pathpt))  
        
        print('-----')
        print(self.__path.shape)
        print('-----')
      
        # print(self.__path.shape)
        
        self.output()
            
        
    def __big(self):
        print('run big grid method')
        
    def output(self):
        print('output and save to file')
        print(self.__path.shape[0])
        os.chdir('./path')
        
        if os.path.exists('./path/' + self.__filename + '.waypoints'):
            os.remove('./path/' + self.__filename + '.waypoints')
        with open(self.__filename + '.waypoints', "w") as generate:            
            generate.write('QGC WPL 110\n')
            generate.write('0\t1\t0\t16\t'  \
                + str(format(0,'.8f')) + '\t' + str(format(0,'.8f')) + '\t' + str(format(0,'.8f')) + '\t' + str(format(0,'.8f')) + '\t' \
                    + str(format(self.__home[0,0],'.8f')) + '\t' \
                        + str(format(self.__home[1,0],'.8f')) + '\t' \
                            + str(format(self.__home[2,0],'.8f')) + '\t' + str(1)  + '\n' )
            
            print(str( format(0,'.6f')  ))
            x = 0
            for t in range(0,self.__path.shape[0] ):
                if t == 0 :
                    generate.write( str(t + 1) + '\t0\t0\t84\t'  \
                        + str(format(0,'.8f')) + '\t' + str(format(0,'.8f')) + '\t' + str(format(0,'.8f')) + '\t' + str(format(0,'.8f')) + '\t' \
                            + str(format(self.__path[t,0],'.8f')) + '\t' \
                                + str(format(self.__path[t,1],'.8f')) + '\t' \
                                    + str(format(self.__path[t,2],'.8f')) + '\t' + str(1) + '\n'  ) 
                elif t+1 == self.__path.shape[0] :
                    generate.write( str(t + 1) + '\t0\t0\t85\t'  \
                    + str(format(0,'.8f')) + '\t' + str(format(0,'.8f')) + '\t' + str(format(0,'.8f')) + '\t' + str(format(0,'.8f')) + '\t' \
                        + str(format(self.__path[t,0],'.8f')) + '\t' \
                            + str(format(self.__path[t,1],'.8f')) + '\t' \
                                + str(format(self.__path[t,2],'.8f')) + '\t' + str(1) + '\n'  ) 
                else:                    
                    generate.write( str(t + 1) + '\t0\t0\t16\t'  \
                    + str(format(0,'.8f')) + '\t' + str(format(0,'.8f')) + '\t' + str(format(0,'.8f')) + '\t' + str(format(0,'.8f')) + '\t' \
                        + str(format(self.__path[t,0],'.8f')) + '\t' \
                            + str(format(self.__path[t,1],'.8f')) + '\t' \
                                + str(format(self.__path[t,2],'.8f')) + '\t' + str(1) + '\n'  )                
        # print(x)
                                                            

if __name__ == '__main__':
    #lat_input = [22.37359465 22.37053155 22.37675465 22.37981775];
    #lon_input = [113.9250661 113.9202338 113.9162891 113.9211214];
    points = np.array([[22.37359465, 113.9250661],
                           [22.37053155, 113.9202338],
                           [22.37675465, 113.9162891],
                           [22.37981775, 113.9211214]])
    alt = np.array([[300],
                        [50],
                        [600]])
    takeoff = np.array([[22.37838290],
                         [113.92457220],
                         [130]])
    
    home = np.array([ [22.378514],
                      [113.924457],
                      [128.98] ])
    step_dist = 50
    mode =  False
    
    x = tool.datatype(points, alt, takeoff, home, step_dist, mode)
    y = cpp(x,'test')
    
     




    
    
