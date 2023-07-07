import math
from pickle import NONE
import sys

class Attendee():
    def __init__(self, x, y, tastes):
        self.x = x
        self.y = y
        self.tastes = tastes
    def find_impact(self, array, instrument, bottom_left):
        i = 0
        j = 0
        while i<len(array):
            j = 0
            while j<len(array[i]):
                array[i][j]+=10000000*self.tastes[instrument]/abs(pow(self.x - (j+bottom_left[0]+10),2)+pow(self.y - (i+bottom_left[1]+10),2))
                j+=1
            i+=1

class Coord():

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

    def print(self):
        print(str(self.x)+" "+str(self.y)+" "+str(self.value))

class Instruments():
    def __init__(self):
        self.coord_list = []
    def find_coord_list(self, array):
        maxval = -sys.maxsize
        Max_X = 0
        Max_Y = 0
        for _ in range(0,10):
            i = 0
            while i<len(array):
                j = 0
                while j<len(array[i]):
                    if(array[i][j]>=maxval):
                        maxval = array[i][j]
                        Max_X = j+stage_bottom_left[0]+10
                        Max_Y = i+stage_bottom_left[1]+10
                    j+=1
                i+=1
            self.coord_list.append(Coord(Max_X, Max_Y, maxval))
            maxval = 0
            array[Max_Y-(stage_bottom_left[1]+10)][Max_X-(stage_bottom_left[0]+10)] = 0


room_width = 2000
room_height = 5000
stage_width = 1000
stage_height = 200
stage_bottom_left = [500, 0]
musicians = [0,1,0]
Attendies = [Attendee(100,500, [1000, -1000]),Attendee(200,1000, [200, 200]),Attendee(1100,800, [800, 1500])]
instruments = [Instruments()]
for _ in range(max(musicians)):
    instruments.append(Instruments())
a = 0
while a<len(instruments):
    array = [[0.0]*(stage_width-20)]
    for _ in range(stage_height-20-1):
        array.append([0.0]*(stage_width-20))
    for attend in Attendies:
        attend.find_impact(array,a,stage_bottom_left)
    instruments[a].find_coord_list(array)
    print(str(len(instruments[a].coord_list))+" "+str(a))
    for coord in instruments[a].coord_list:
        coord.print()
    print()
    a+=1



