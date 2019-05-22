import sys
import random
import statistics
import math
import plotly
import plotly.graph_objs as go
if len(sys.argv) > 1:
    print(sys.argv[1])
test = [1,2,3]
for item in range(len(test)):
    print(item)


'''
scat = go.Scatter(x = x, y=y, mode = "lines+markers", name = "test")
scat2 = go.Scatter(x = newX, y=newY, mode = "lines+markers", name = "regression")
plotly.offline.plot([scat, scat2], auto_open = True, filename = "test.html")
'''


