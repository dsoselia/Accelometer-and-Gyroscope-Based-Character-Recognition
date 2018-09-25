# -*- coding: utf-8 -*-

import ast

files = ['a.txt', 'i.txt']
#filename = 'a.txt'
lines = []
y_tr = []
lines_test = []
y_tst = []
letterCounter = 0
nTh = 0
for fname in files:
    with open(fname) as f:
        for line in f.readlines():
            if (nTh < 70 and nTh > 50):
                lines_test.append(ast.literal_eval(line))
                temp = [0] * len(files)
                temp[letterCounter] = 1
                y_tst.append([temp])
            else:
                lines.append(ast.literal_eval(line))
                temp = [0] * len(files)
                temp[letterCounter] = 1
                y_tr.append([temp])
            nTh += 1
        letterCounter += 1
        nTh = 0
vx = []
vy = []
vz = []
        
def get_np(j):
    i = 0
    while i < len(lines[j]):
      vx.append(lines[j][i]['AcX'])
      vy.append(lines[j][i]['AcY'])
      vz.append(lines[j][i]['AcZ'])
      i +=1
      
    import numpy as np
    np_arr = np.array([vx,vy, vz ])
    return np_arr

def get_np1(j):
    i = 0
    while i < len(lines_test[j]):
      vx.append(lines_test[j][i]['AcX'])
      vy.append(lines_test[j][i]['AcY'])
      vz.append(lines_test[j][i]['AcZ'])
      i +=1
      
    import numpy as np
    np_arr = np.array([vx,vy, vz ])
    return np_arr



from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np


model = Sequential()
model.add(LSTM(10, return_sequences=True, stateful=True, input_shape=(None, 3),
         batch_input_shape=(1, None, 3)))
model.add(LSTM(10))
#model.add(Dense(15, activation='relu'))
model.add(Dense(2, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# Generate dummy training data
#x_train = np.transpose(np_arr).reshape(1,np_arr.shape[1],3)
#x_train_2 = np.random.random((1, 10, 3))
#y_train = np.random.random((1, 2))
#y_train_2 = np.random.random((1, 2))


import random
j = 0
iter = 0
while(j < len(lines)):
    np_arr = get_np(j)
    x_train = np.transpose(np_arr).reshape(1,np_arr.shape[1],3)
    y_train = np.array(y_tr[j])
    model.fit(x_train, y_train, batch_size=1, nb_epoch=1, shuffle=False, verbose=1)
    print(j)
    j=random.randint(1, len(lines))
    if(iter % 50 == 0):
        model.save('my_model3.h5')
    iter+=1;
    
j = 0
accurate = 0
while(j < len(lines_test)):
    np_arr = get_np1(j)
    x_train = np.transpose(np_arr).reshape(1,np_arr.shape[1],3)
    y_train = np.array(y_tst[j])
    #model.fit(x_train, y_train, batch_size=1, nb_epoch=1, shuffle=False, verbose=1)
    if (np.argmax(y_train)==np.argmax(model.predict(x_train))):
        accurate+=1
        print('true')
    print(j)
    j+=1
print(accurate/float(len(lines_test)))
