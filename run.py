from indicators.SMA import SMA
import plotly
import plotly.graph_objs as go
import random
import math
from threading import Thread
from multiprocessing import Process, Manager
from main import start
file = "EURUSD2018.csv"
def myThreads(listToAdd, i):
    #initial value to compaire to
    indicators = {"smallSMA": [SMA,"EUR/USD", 100], "largeSMA": [SMA, "EUR/USD", 200]}
    #originial value to compare to
    value = start(100000, 15, file,False, False, indicators)
    #run through the market x times, comparing it to value and grabbing the best
    for x in range(5):
        a = random.randint(2, 500)
        b = random.randint(2, 500)
    
        if a > b:
            indicators["smallSMA"][2] = b
            indicators["largeSMA"][2] = a

           
        
        else:
            indicators["smallSMA"][2] = a
            indicators["largeSMA"][2] = b
            
        val = start(100000, 15,file,False, False,indicators)
        print("a: " + str(a) +  " b: " + str(b) + " val: " + str(val.balance) + " at number: " + str(x) + " thread #: " + str(i) + "small: " + str(val.getAllIndicators()["smallSMA"].getLength()))
        if val.balance > value.balance:
            value = val
    listToAdd[i] = value


if __name__ == "__main__":
    #manager syncs the list between all the processes
    manager = Manager()
    numOfThreads = 9
    bestMarkets = manager.list(range(numOfThreads))
    allThreads = []
    #creates 8 processes with the shared list of bestMarkets from each thread
    for x in range(numOfThreads):
        th = Process(target = myThreads, args = (bestMarkets, x))
        th.start()
        allThreads.append(th)
    #wait until each of the threads have finished
    for t in allThreads:
        t.join()

    print("PRINTING ALL ITEMS IN BEST")
    for item in bestMarkets:
        print(item)
    #finding the market that gave the best balance
    best = bestMarkets[0]
    for x in range(numOfThreads):
        if bestMarkets[x].balance > best.balance:
            best = bestMarkets[x]

    #prints the best moving averages of the market
    print("smallSMA and largeSMA: ")
    print(best.getIndicator("smallSMA").getLength())
    print(best.getIndicator("largeSMA").getLength())