import sys
import random
import statistics
import math
import plotly
import plotly.graph_objs as go
from indicators.RSI import RSI
import numpy as np
'''
m = 2
rsi = RSI(m, "EUR/USD", 14)
closes = [46.125, 47.125, 46.4375, 46.9375, 44.9375, 44.25, 44.625, 45.75, 47.8125, 47.5625, 47, 44.5625, 46.3125, 47.6875, 46.6875]
for i in closes:
    rsi.update(i)
print("the first value: " + str(rsi.getValue()))

rsi.update(45.6875)
print("AFTER UPDATE")


print("rs")
print(rsi.RS)
print("RSI:")
print(rsi.getValue())
rsi.update(43.0625) 
print("AFTER NEXT UPDATE")
print("rs")
print(rsi.RS)
print(rsi.getValue())
'''
'''
scat = go.Scatter(x = x, y=y, mode = "lines+markers", name = "test")
scat2 = go.Scatter(x = newX, y=newY, mode = "lines+markers", name = "regression")
plotly.offline.plot([scat, scat2], auto_open = True, filename = "test.html")
'''


values = []
time = 1
times = []
def getValue(value):
    #turn the value into 4 digits, update time and both lists, then create the least square fit
    global values
    global time
    global times
    svalue = str(value)
    svalue = svalue[3:]

    if len(svalue) == 2:
        svalue = svalue + "0"
        svalue = svalue + "0"
    if len(svalue) == 3:
        svalue = svalue +"0"

    nvalue = float(svalue)
    print(nvalue)
    values.insert(0, nvalue)
    if len(values) > 5:
        values.pop()
    
    times.insert(0, time)
    if len(times) > 5:
        times.pop()
    time += 1
    #creating LSF
    if len(times) != 5 or len(values) != 5:
        return
    
    times.reverse()
    array = np.array([[1,1,1,1,1], times]) #this automatically stores it as transposed
    times.reverse()
    
    #array.transpose()
    #print(array.T)

    values.reverse()
    y = np.array(values)
    values.reverse()
    print(y)

   

    step1 = array.dot(array.T)
    print("STEP 1")
    print(step1)
    step2 = np.linalg.inv(step1)
    print("STEP 2")
    print(step2)
    step3 = np.dot(step2, array)
    print("STEP 3")
    print(step3)
    step4 = np.dot(step3,y )
    print("STEP 4")
    print(step4)
    
    slopes.insert(0, step4[1])
   

    
    
    
    


getValue(1.14355)
getValue(1.14419)
getValue(1.1449)
getValue(1.14493)
getValue(1.14708)