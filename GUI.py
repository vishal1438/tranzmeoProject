from tkinter import*
from tkinter import filedialog
import os
from PIL import Image,ImageTk
import numpy as np
import time, math
from math import sin, cos, sqrt, atan2, radians
import pandas as pd
import pymysql
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
np.seterr(over='ignore')
def pp(a):
    global mylist
    mylist.insert(END, a)
    
def que1():
    global inp_img, root
    root.after(500, lambda : pp("Q: Write a python code to find the latitude and longitude coordinates that are out of line and automatically fix the same to form a continuous path."))
    tr=pd.read_csv("latitude_longitude_details.csv")
    root.after(500, lambda : pp("Reading CSV file"))
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
    root.after(500, lambda : pp("Appending only latitude and longitude less than 0.5 value"))
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
    plt.savefig('continuouspath.png')
    root.after(500, lambda : pp("Plotting the continuous path"))
    image3 = Image.open('continuouspath.png')
    image3 = image3.resize((350, 250), Image.ANTIALIAS) ## The (550, 250) is (height, width)
    pic3 = ImageTk.PhotoImage(image3)
    inp_img.config(image=pic3)
    inp_img.image =  pic3
    root.after(500, lambda : pp("----------------------------------------"))

def que2():
    global root
    
    root.after(500, lambda : pp("Q: From the given terrain list with kilometeres, write a python script to generate DB of each latitude and longitude pair with matching terrain information."))
    db=pymysql.connect("localhost","root","","testtranzmeo")
    cursor=db.cursor()
    root.after(500, lambda : pp("Connecting to the Database.."))
    try:
        sql = "CREATE TABLE terraininfo(lat VARCHAR(255) NOT NULL UNIQUE, lon VARCHAR(255) NOT NULL UNIQUE, terrain VARCHAR(255), distance VARCHAR(255))"
        cursor.execute(sql)
        root.after(500, lambda : pp("Table created successfully."))
        print("Table Created Successfully")
    except Exception as ex:
        print("Exception: ", ex)
        root.after(500, lambda : pp("Table already created."))
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
    root.after(500, lambda : pp("Calculating distance and saving to DB."))
    
    f = open("res.txt", "w")
    f.write("\n".join(nd))
    f.close()
    print(d)
    root.after(500, lambda : pp("Total Distance: "+str(d)))
    root.after(500, lambda : pp("----------------------------------------"))

def que3():
    global inp_img, root
    root.after(500, lambda : pp("Q: Write Query to list all the points with terrain road in it without civil station"))
    root.after(500, lambda : pp("Selecting terrain info without civil station road"))
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
    root.after(1500, lambda : pp("Graph Plotted"))
    plt.savefig('terrain.png')
    image3 = Image.open('terrain.png')
    image3 = image3.resize((350, 250), Image.ANTIALIAS) ## The (550, 250) is (height, width)
    pic3 = ImageTk.PhotoImage(image3)
    inp_img.config(image=pic3)
    inp_img.image =  pic3
    root.after(500, lambda : pp("----------------------------------------"))

def que4():
    l1 = str(latv.get())
    l2 = str(lonv.get())
    root.after(500, lambda : pp("Generate a set of points which are 25 meters to the left and right of the given latitude and longitude, Use multi-threaded/ multi-processing to optimize the execution with the reasoning of the same"))
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
    root.after(500, lambda : pp("Left Longitude: "+str(leftlon)))
    root.after(500, lambda : pp("Left Latitude: "+str(leftlat)))
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
    root.after(500, lambda : pp("Right Longitude: "+str(rightlon)))
    root.after(500, lambda : pp("Rightt Latitude: "+str(rightlat)))

def movingTotal(n, c):
    l = range(1, n+1)
    p = []
    for i in range(0, n):
        if i+2==n:
            break
        p.append(sum([l[i], l[i+1], l[i+2]]))
    if c in p:
        return True
    else:
        return False
    
def que5():
    root.after(500, lambda : pp("Q: Design a data structure that can, efficiently with respect to time used, store and check if the total of any three successively added elements is equal to a given total."))
    n = int(str(tot.get()))
    v = int(str(vals.get()))
    b = movingTotal(n, v)
    print(b)
    root.after(500, lambda : pp("Result: "+str(b)))

ab=0
filename = ""

root = Tk()
root.configure(bg="#a0ff65")
root.geometry("1600x700+0+0")
root.title("TRANZMEO")


#------------------TIME--------------
localtime=time.asctime(time.localtime(time.time()))
#-----------------INFO TOP------------
lblinfo = Label(root, font=( 'aria' ,30, 'bold' ),text="TRANZMEO MACHINE TEST",bg="#a0ff65",fg="white",bd=10,anchor='w')
lblinfo.place(x=350,y=0)
lblinfo = Label(root, font=( 'aria' ,20, ),text=localtime,bg="#a0ff65",fg="white",anchor=W)
lblinfo.place(x=480,y=50)

lblin = Label(root, font=( 'aria' ,15, 'bold' ),bg="#a0ff65",text="TASK 1",fg="white",bd=10,anchor='w')
lblin.place(x=70,y=80)

btntrn=Button(root,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,10,'bold'),width=10, text="QUESTION 1", bg="light green", command=lambda:que1())
btntrn.place(x=150, y=120)

btntrn=Button(root,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,10,'bold'),width=10, text="QUESTION 2", bg="light green", command=lambda:que2())
btntrn.place(x=350, y=120)

btntrn=Button(root,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,10,'bold'),width=10, text="QUESTION 3", bg="light green", command=lambda:que3())
btntrn.place(x=550, y=120)


lblin = Label(root, font=( 'aria' ,15, 'bold' ),bg="#a0ff65",text="TASK 2",fg="white",bd=10,anchor='w')
lblin.place(x=70,y=180)

lblin = Label(root, font=( 'aria' ,15, 'bold' ),bg="#a0ff65",text="Latitude:",fg="white",bd=10,anchor='w')
lblin.place(x=50,y=210)

latv = Entry(root,font=('ariel' ,12,'bold') , bd=5 ,insertwidth=5 ,bg="white",justify='right')
latv.place(x=170,y=210)

lblin = Label(root, font=( 'aria' ,15, 'bold' ),bg="#a0ff65",text="Longitude:",fg="white",bd=10,anchor='w')
lblin.place(x=50,y=250)

lonv = Entry(root,font=('ariel' ,12,'bold') , bd=5 ,insertwidth=5 ,bg="white",justify='right')
lonv.place(x=170,y=250)

btntrn=Button(root,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,10,'bold'),width=10, text="QUESTION 1", bg="#a0ff65", command=lambda:que4())
btntrn.place(x=250, y=290)

lblin = Label(root, font=( 'aria' ,15, 'bold' ),bg="#a0ff65",text="Iterations:",fg="white",bd=10,anchor='w')
lblin.place(x=430,y=210)

tot = Entry(root,font=('ariel' ,12,'bold') , bd=5 ,insertwidth=5 ,bg="white",justify='right')
tot.place(x=550,y=210)

lblin = Label(root, font=( 'aria' ,15, 'bold' ),bg="#a0ff65",text="Value:",fg="white",bd=10,anchor='w')
lblin.place(x=430,y=250)


vals = Entry(root,font=('ariel' ,12,'bold') , bd=5 ,insertwidth=5 ,bg="white",justify='right')
vals.place(x=550,y=250)


btntrn=Button(root,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,10,'bold'),width=10, text="QUESTION 2", bg="#a0ff65", command=lambda:que5())
btntrn.place(x=570, y=290)


lbli = Label(root, font=( 'aria' ,15, 'bold' ),text="PREDICTED GRAPH",bg="#a0ff65",fg="white",bd=10,anchor='w')
lbli.place(x=290,y=370)



def qexit():
    root.destroy()





mylist = Listbox(root,width=70, height=20, bg="light green" )

mylist.place( x = 880, y = 170 )


btnexit=Button(root,padx=16,pady=8, bd=10 ,fg="black",font=('ariel' ,16,'bold'),width=10, text="EXIT", bg="light green",command=qexit)
btnexit.place(x=1000, y=500)


image2 = Image.open("bg1.jpg")
image2 = image2.resize((350, 250), Image.ANTIALIAS) ## The (550, 250) is (height, width)
pic2 = ImageTk.PhotoImage(image2)
inp_img=Label(root,image=pic2, borderwidth=2, relief="raised")
inp_img.place(x=230,y=400)

root.mainloop()

