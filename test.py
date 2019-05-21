import sys
import random
import statistics
import math
import plotly
import plotly.graph_objs as go
if len(sys.argv) > 1:
    print(sys.argv[1])

x = [.0001 * i for i in range(5)]
y = [ 1.145789, 1.145795,1.145807,1.145852,1.145831]

z = []

for item in range(len(x)):
    z.append(x[item] * y[item])


def linearRegression(x, y):
    z = []
    for item in range(len(x)):
        z.append(x[item] * y[item])
    xSquared = []
    for item in x:
        xSquared.append(item*item)
    return ( (len(x) * sum(z))  - (sum(x) * sum(y))     ) / ( (len(x) * sum(xSquared)) - (sum(x) * sum(x))          )


b = statistics.mean(y) - (linearRegression(x, y)*statistics.mean(x))


newX = [i for i in range(10)]
newY = []
m = linearRegression(x, y)

for num in newX:
    newY.append(m*num + b)
rads = math.atan(m)
degrees = rads * (180/ math.pi)
print(degrees)
print(m)





scat = go.Scatter(x = x, y=y, mode = "lines+markers", name = "test")
scat2 = go.Scatter(x = newX, y=newY, mode = "lines+markers", name = "regression")
plotly.offline.plot([scat, scat2], auto_open = True, filename = "test.html")


