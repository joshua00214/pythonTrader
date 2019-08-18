from indicators.SMA import SMA
from indicators.EMA import EMA
from indicators.RSI import RSI
from indicators.MACD import MACD
from indicators.SAR import SAR
import plotly
import plotly.graph_objs as go
import random
import math
from threading import Thread
from multiprocessing import Process, Manager
from main import start
import sys



file = "EURUSDFEB.csv"



def myThreads(listToAdd, i):
    #initial value to compaire to
    indicators = {"EMA": [EMA,"EUR/USD", 10]}

    d = 15
    e = 5
    p = 5
    data = [d, e, p]
    #originial value to compare to
    value = start(100000, 60, file,False, False, indicators, data)
    #run through the market x times, comparing it to value and grabbing the best
    for x in range(100):
        d = random.randint(1, 90) 
        e = random.randint(1, 90)
        p = random.randint(1, 500) 
        indicLength = random.randint(1, 50)
        indicators["EMA"][2] = indicLength
        data = [d, e, p]
        val = start(100000, 1440, file, False, False, indicators, data)
        print("thread: " + str(i) + " starting number: " + str(x) +" balance: " + str(val.balance))
        if val.balance > value.balance:
            value = val
    listToAdd[i] = value


if __name__ == "__main__":
    if len(sys.argv) != 2:
        indicators = {"SAR": [SAR, "EUR/USD"], "MACD": [MACD, "EUR/USD"], "RSI" : [RSI, "EUR/USD", 14]}
        
        data = []#d, e, p
        start(100000, 60, file,True, True, indicators, data)
        exit()
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
        pass


    #print("PRINTING ALL ITEMS IN BEST") just prints memory location, not needed
    #for item in bestMarkets:
    #    print(item)

    #finding the market that gave the best balance
    best = bestMarkets[0]
    for x in range(numOfThreads):
        if bestMarkets[x].balance > best.balance:
            best = bestMarkets[x]

    print("balance: ")
    print(best.balance)
    print("data: ")
    print(best.data)
    print("indicators: " )
    print(best.dictOfIndicators)