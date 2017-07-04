
import math
import checkers as ck
from matplotlib.pyplot import *


ZERO = 0
CIRCUMFERENCE_OF_THE_EQUATOR = 40075
CIRCUMFERENCE_ALONG_A_MERIDIAN = 40007


class Approximation(object):

    # Initialization function
    def __init__(self, file_path):
        self.file_path = file_path
        self.pre_processing(file_path)


    def pre_processing(self, file_path):
        """
        Pre-processing the file and get useful info for further approximation

        :param file_path: the path of the file we want to process
        :return: None
        """
        self.xs,self.ys = [],[]
        #list of lists to store the elevation of each point
        self.elevation = []

        # Open file and read x,y,z values
        with open(file_path) as f:
            for line in f:
                yxz = line.split()
                if ck.yxz_checker(yxz):
                    y,x = float(yxz[0]),float(yxz[1])
                    # If the y value (latitude) not in the ys list, then append y into the ys list.
                    # In addition, add a empty list in the elevation list.
                    if y not in self.ys:
                        self.ys.append(y)
                        self.elevation.append([])
                    # If the x value (longitude) not in the xs list, then append x into the xs list.
                    if x not in self.xs:
                        self.xs.append(x)
                    self.elevation[-1].append(float(yxz[2]))
                else:
                    # If the data file not a YXZ format will occur this error message.
                    raise AssertionError('The data file is not YXZ formatted')

        # Obtain the max elevation value from the elevation list.
        self.max_elevation = max([max(i) for i in self.elevation])

        # Calculate the mean horizontal spacing only for approximation 1
        self.h_mean_degree = (self.xs[-1]-self.xs[0])/(len(self.xs)-1)
        self.mean_latitude =  sum(math.cos(math.radians(i)) for i in self.ys)/len(self.ys)
        self.h_mean = self.h_mean_degree*CIRCUMFERENCE_OF_THE_EQUATOR/360*self.mean_latitude

        # Calculate the mean vertical spacing for both approximation 1 and 2
        self.v_mean_degree =(self.ys[0]-self.ys[-1])/(len(self.ys)-1)
        self.v_mean = self.v_mean_degree*CIRCUMFERENCE_ALONG_A_MERIDIAN/360

        # Calculate how many rows and columns we have in the grid
        self.rows  =  len(self.ys)
        self.columns = len(self.xs)


    def first_approximation(self,func):
        """
        Calculate the land area using the first approximation and print out the result

        :param func: the functionality you want to realize using first approximation
        :return:  None
        """

        #ask users if they want to set parameters manully
        manual = ck.get_string("Would you like to set "
                               "the mean spacing manually for first approximation?(Y/N)"
                               ,["Y",'y',"N","n"])

        #get mean horizontal spacing and mean vertical spacing
        if manual =="Y" or manual == "y":
            v_mean = ck.get_float("Enter the mean vertical spacing in km:",0)
            h_mean = ck.get_float("Enter the mean horizontal spacing in km:",0)
        else:
            v_mean = self.v_mean
            h_mean = self.h_mean
        unit_area = v_mean * h_mean

        # If user want to area above certain sea level
        if func == 1:
            self.sea_level = ck.get_float("Enter the sea level:",lower=ZERO)
            sample,q_sample = 0,0

            #since each point has same unit area ,we only need to consider number of points of each category to get the result
            #get all points having positive sea level
            sample = len([unit for row in self.elevation for unit in row if unit>0])
            #get all points above the certain sea level
            q_sample = len([unit for row in self.elevation for unit in row if unit>self.sea_level])

            #print out the result
            print("=======================================")
            print("The result of the first approximation:")
            print("=======================================")
            print("The land area above water in this area at +{} meters will be {:.0f} square kilometers".format(self.sea_level,q_sample*unit_area))
            print("It is {:.2f}% of the current land area above water".format(q_sample/sample*100))

        # If user wants to see the distribution of land area regarding sea level
        if func ==  2:
            self.intervals = ck.get_int("How many intervals you want to divide into?",2)
            sample = len([unit for row in self.elevation for unit in row if unit>0])
            step = self.max_elevation/self.intervals

            self.xCoors1 = [i*step for i in range(100,0,-1)]
            self.yCoors1 = [0]*self.intervals

            for row in self.elevation:
                for unit in row:
                    if unit>0:
                         self.yCoors1[int(math.ceil(unit/step))-1]+=1
            self.yCoors1.reverse()
            for j in range(self.intervals-1):
                self.yCoors1[j+1] += self.yCoors1[j]
            self.yCoors1=[i/sample*100 for i in self.yCoors1]
            # plot(self.xCoors1, self.yCoors1,color = "black")
            # show()



    def second_approximation(self,func):
        """
        Calculate the land area using the second approximation and print out the result

        :param func: the functionality you want to realize using first approximation
        :return:  None
        """

        # If user want to area above certain sea level
        if func == 1:
            total_area, above_area =0,0
            for i in range(self.rows):
                h_mean = CIRCUMFERENCE_OF_THE_EQUATOR*math.cos(math.radians(self.ys[i]))/360*self.h_mean_degree
                unit = h_mean*self.v_mean
                for j in range(self.columns):
                    if self.elevation[i][j]>0:
                        total_area +=unit
                        if self.elevation[i][j]>self.sea_level:
                            above_area+=unit
            print("=======================================")
            print("The result of the second approximation:")
            print("=======================================")
            print("The land area above water in this area at +{} meters will be {:.0f} square kilometers".format(self.sea_level,above_area))
            print("It is {:.2f}% of the current land area above water".format(above_area/total_area*100))

        # If user wants to see the distribution of land area regarding sea level
        if func ==2:
            step = self.max_elevation/self.intervals

            self.xCoors2 = [i*step for i in range(100,0,-1)]
            self.yCoors2 = [0]*self.intervals

            total_area = 0
            for i in range(self.rows):
                h_mean = CIRCUMFERENCE_OF_THE_EQUATOR*math.cos(math.radians(self.ys[i]))/360*self.h_mean_degree
                unit = h_mean*self.v_mean
                for j in range(self.columns):
                    if self.elevation[i][j]>0 :
                        total_area +=unit
                        self.yCoors2[math.ceil(self.elevation[i][j]/step)-1]+=unit
            self.yCoors2.reverse()
            for j in range(self.intervals-1):
                self.yCoors2[j+1] += self.yCoors2[j]
            self.yCoors2=[i/total_area*100 for i in self.yCoors2]


    def draw_graph(self):
        """
        Draw graph to show the distributions of the land area for both approximation

        :return:None
        """

        plot(self.xCoors1,self.yCoors1,linestyle = "solid", color ="black",label = "First Approximation")
        plot(self.xCoors2,self.yCoors2,linestyle = "solid", color ="red",label = "Second Approximation")
        xlabel("sea level increase")
        ylabel("area above water in percentage(%)")
        legend()
        show()

    def connected_land(self,sea_level):
        """
        Calculate how many separate land areas in the area described by the data file

        :param sea_level: the sea level to determine whether two point are connected
        :return: number of separate land areas
        """
        visited , count = set(),0
        for i in range(self.rows):
            for j in range(self.columns):
                if not (i,j) in visited and self.elevation[i][j]>sea_level:
                    visited.update(self.bfs(i,j,sea_level))
                    count+=1
        return count



    def bfs(self,x,y,sea_level = 0):
        """
        Breadth first search the grid from point(x,y) according to the sea_level

        :param x: x coordinate of the start point
        :param y: y coordinate of the start point
        :param sea_level: sea level to determine whether two point are connected
        :return: set of the visited point ,each point is represent as a tuple (x,y)
        """
        queue = [(x,y)]
        res = {(x,y)}


        while queue:
            ##pop out the first element
            point = queue.pop(0)
            i ,j = point[0],point[1]

            #check all 8 directions of the point
            ##top left
            if i-1>=0 and j-1>=0:
                if self.elevation[i-1][j-1]>sea_level and (i-1,j-1) not in res:
                    queue.append((i-1,j-1))
                    res.add((i-1,j-1))

            ##top
            if i-1>=0 and self.elevation[i-1][j]>sea_level and (i-1,j) not in res:
                queue.append((i-1,j))
                res.add((i-1,j))

            ##top right
            if i-1>=0 and j+1<self.columns:
                if self.elevation[i-1][j+1]>sea_level and (i-1,j+1) not in res:
                    queue.append((i-1,j+1))
                    res.add((i-1,j+1))

            ##right
            if j+1<self.columns and self.elevation[i][j+1]>sea_level and (i,j+1) not in res:
                queue.append((i,j+1))
                res.add((i,j+1))

            ##bottom right
            if i+1<self.rows and j+1<self.columns:
                if self.elevation[i+1][j+1]>sea_level and (i+1,j+1) not in res:
                    queue.append((i+1,j+1))
                    res.add((i+1,j+1))

            ##bottom
            if i+1<self.rows and self.elevation[i+1][j]>sea_level and (i+1,j) not in res:
                queue.append((i+1,j))
                res.add((i+1,j))

            ##bottom left
            if i+1<self.rows and j-1>=0:
                if self.elevation[i+1][j-1]>sea_level and (i+1,j-1) not in res:
                    queue.append((i+1,j-1))
                    res.add((i+1,j-1))

            ##right
            if j-1>=0 and self.elevation[i][j-1]>sea_level and (i,j-1) not in res:
                queue.append((i,j-1))
                res.add((i,j-1))

        return res


if __name__ == "__main__":
    print("Welcome to use our software!")
    print("============================")

    while True:
        try:
            file_path =input("Please enter the data file path:")
            appro = Approximation(file_path)
            break
        except:
            print("Error: No such file!")
    print("Processing , please wait...")
    while True:
        print("============================")
        print("What would you like to do ?")
        func = ck.get_int("1. Calculate land area above certain sea level.\n"
                          "2. See land area distribution\n"
                          "3. Calculate number of seperate land\n"
                          "0. Exit\n"
                          "Please select:",0,3)
        if func == 0 :
            break
        elif func == 1:
            appro.first_approximation(func)
            appro.second_approximation(func)
        elif func == 2:
            appro.first_approximation(func)
            appro.second_approximation(func)
            appro.draw_graph()
        else:
            sea_level = ck.get_float("Please enter the sea level you want to check:",0)
            print("============================")
            print("There are {} seperate land areas".format(appro.connected_land(sea_level)))
    print("Thanks for using!")
