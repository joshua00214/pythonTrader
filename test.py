import sys
import random
import statistics
import math
import plotly
import plotly.graph_objs as go
from indicators.RSI import RSI

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
scat = go.Scatter(x = x, y=y, mode = "lines+markers", name = "test")
scat2 = go.Scatter(x = newX, y=newY, mode = "lines+markers", name = "regression")
plotly.offline.plot([scat, scat2], auto_open = True, filename = "test.html")
'''


