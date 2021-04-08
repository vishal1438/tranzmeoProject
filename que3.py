import numpy as np
import time, math
from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import pymysql
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
def que3():
    db=pymysql.connect("localhost","root","","testtranzmeo")
    cursor=db.cursor()
    sql="SELECT * FROM `terraininfo` WHERE terrain NOT LIKE '%civil%';"
    print (sql)
    try:
        cursor.execute(sql)
        res=cursor.fetchall()
        print(res)
    except:
        pass
    la=[]
    lo=[]
    for i in res:
        la.append(i[0])
        lo.append(i[1])
    plt.clf()
    plt.title('Continuous Path')
    plt.xlabel("Latitude")
    plt.ylabel("Longitude")
    plt.scatter(la, lo)
    ##plt.plot(x, y)
    plt.show()
    
que3()
