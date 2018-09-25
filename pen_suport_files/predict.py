#!/usr/bin/env python3
import tkinter as tk
import serial
import ast
import numpy as np


# if you are still working under a Python 2 version, 
# comment out the previous line and uncomment the following line
# import Tkinter as tk

root = tk.Tk()

w = tk.Label(root, text="Hello there!", width=200, height=200, font = ('Courier', 200))
w.pack()
def upd(a = ''):
    w.config(text=a)
    root.update_idletasks()
    root.update()
 
#b = tk.Button(root, text ='clear', command = upd) 
#b.pack()
upd('a')
upd('b')

#root.mainloop()
from keras.models import load_model
'''
def get_np(line):
    i = 0
    vx = []
    vy = []
    vz = []
    ax = []
    ay = []
    az = []
    while i < len(line):
      vx.append(line[i]['AcX'])
      vy.append(line[i]['AcY'])
      vz.append(line[i]['AcZ'])
      ax.append(line[i]['GyX'])
      ay.append(line[i]['GyY'])
      az.append(line[i]['GyZ'])
      i +=1
    import numpy as np
    np_arr = np.array([vx,vy, vz, ax,ay, az])
    return np_arr
'''
def get_np(line):
    
    i = 0
    vx = []
    vy = []
    vz = []
    ax = []
    ay = []
    az = []
    while i < len(line):
      vx.append(line[i][0])
      vy.append(line[i][1])
      vz.append(line[i][2])
      ax.append(line[i][3])
      ay.append(line[i][4])
      az.append(line[i][5])
      i +=1
    import numpy as np
    np_arr = np.array([vx,vy, vz, ax,ay, az])
    return np_arr
def string_to_object(str_1):
    str_1 = str_1[:-1]
    str_1 = str_1.split(';')
    char = []
    for data in str_1:
        moment = []
        values =  data.split(',')
        for val in values:
            moment.append(int(val))
        char.append(moment)
    return char
'''
def upd(a):
    return 0
'''
model = load_model('abcdeg_l.h5')
files = ['a.txt', 'b.txt', 'c.txt', 'd.txt', 'e.txt', 'g.txt']
str1=''
def get(line):
    global str1
    line = string_to_object(line)
    print(line)
    np_arr = get_np(line)
    x_train = np.transpose(np_arr).reshape(1,np_arr.shape[1],6)
    x_train = x_train / 10000.0
        #model.fit(x_train, y_train, batch_size=1, nb_epoch=1, shuffle=False, verbose=1)
    predi = model.predict(x_train)
    print(predi)
    if (np.amax(predi) < 0.8):
	    print("UNSURE")
    print(files[np.argmax(predi)][0])
    str1+=files[np.argmax(predi)][0]
    if (len(str1)>5):
        str1=files[np.argmax(predi)][0]
    upd(str1)


ser = serial.Serial("/dev/tty.usbserial-00000000",115200)
print(ser.name)

while True:
    s=str(ser.readline())
    s=s[2:-4]+"\n"
    #print(s)
    upd('...')
    get(s)
