import numpy as np
import time, math
from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

tr=pd.read_csv("latitude_longitude_details.csv")
nd = []
d = 0
lt, lo = [], []
nd.append(str(tr["latitude"][0])+" "+ str(tr["longitude"][0])+" "+ str(d))
for i in range(0, len(tr["latitude"]), 2):
    
    # approximate radius of earth in km
    R = 6373.0


    lat1 = radians(tr["latitude"][i])
    lon1 = radians(tr["longitude"][i])
    lat2 = radians(tr["latitude"][i+1])
    lon2 = radians(tr["longitude"][i+1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    if distance>0.5:
        continue
    
    d+= distance
    lt.append(tr["latitude"][i])
    lo.append(tr["longitude"][i])

    print("Result:", distance)
    nd.append(str(tr["latitude"][i+1])+" "+ str(tr["longitude"][i+1])+" "+ str(d))
f = open("res.txt", "w")
f.write("\n".join(nd))
f.close()
print(d)
plt.clf()
plt.title('Continuous Path')
plt.xlabel("Latitude")
plt.ylabel("Longitude")
plt.scatter(lt, lo)
##plt.plot(x, y)
plt.show()
