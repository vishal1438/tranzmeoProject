import numpy as np
import time, math
from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import pymysql
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
def que4(l1, l2):
    R = 6378.1 #Radius of the Earth
    brng = -1.57 #Bearing is 90 degrees converted to radians.
    d = 25 #Distance in km

    lat1 = math.radians(float(l1)) #Current lat point converted to radians
    lon1 = math.radians(float(l2)) #Current long point converted to radians

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    leftlat = lat2
    leftlon = lon2
    print("Left Longitude: "+str(leftlon))
    print("Left Latitude: "+str(leftlat))
    brng = 1.57 #Bearing is 90 degrees converted to radians.

    lat1 = math.radians(float(l1)) #Current lat point converted to radians
    lon1 = math.radians(float(l2)) #Current long point converted to radians

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
         math.cos(lat1)*math.sin(d/R)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                 math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    rightlat = lat2
    rightlon = lon2
    print("Right Longitude: "+str(rightlon))
    print("Rightt Latitude: "+str(rightlat))

que4(12.7654, 76.90877)
