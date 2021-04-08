import numpy as np
import time, math
from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import pymysql
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
def que2():
    
    print("Q: From the given terrain list with kilometeres, write a python script to generate DB of each latitude and longitude pair with matching terrain information.")
    db=pymysql.connect("localhost","root","","testtranzmeo")
    cursor=db.cursor()
    print("Connecting to the Database..")
    try:
        sql = "CREATE TABLE terraininfo(lat VARCHAR(255) NOT NULL UNIQUE, lon VARCHAR(255) NOT NULL UNIQUE, terrain VARCHAR(255), distance VARCHAR(255))"
        cursor.execute(sql)
        print("Table Created Successfully")
    except Exception as ex:
        print("Exception: ", ex)
        print("Table already created")
        
    tr=pd.read_csv("latitude_longitude_details.csv")
    nd = []
    d = 0

    lt, lo = [], []
    nd.append(str(tr["latitude"][0])+" "+ str(tr["longitude"][0])+" "+ str(d))
    sql="""insert into terraininfo(lat, lon, terrain, distance)values('%s','%s','%s','%s')"""%(str(tr["latitude"][0]),str(tr["longitude"][0]),"boundary wall,road",str(d))
    print (sql)
    try:
        cursor.execute(sql)
        db.commit()
        print ("inserted")
    except Exception as e:
        db.rollback()
        print ("error",e)
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
        if d<0.5:
            s = "road"
        elif d<1.5:
            s = "river side"
        else:
            s = "civil station, road"
        sql="""insert into terraininfo(lat, lon, terrain, distance)values('%s','%s','%s','%s')"""%(str(tr["latitude"][i+1]),str(tr["longitude"][i+1]),s,str(d))
        print (sql)
        try:
            cursor.execute(sql)
            db.commit()
            print ("inserted")
        except Exception as e:
            db.rollback()
            print ("error",e)

    print(nd)
    f = open("res.txt", "w")
    f.write("\n".join(nd))
    f.close()
    print(d)
    print("Total Distance: "+str(d))
que2()
