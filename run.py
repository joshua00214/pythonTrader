from indicators.SMA import SMA
from indicators.EMA import EMA
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
    indicators = {"EMA": [EMA,"EUR/USD", 4]}
    isAbove = []
    isBelow = []
    n = 1.5 * .0001
    m = 3 
    l = 1 * .0001
    data = [isAbove, isBelow, n, m, l]
    #originial value to compare to
    value = start(100000, 15, file,False, False, indicators, data)
    #run through the market x times, comparing it to value and grabbing the best
    for x in range(1000):
        n = random.randint(1, 20) * .0001
        m = random.randint(1, 20)
        l = random.randint(1, 20) * .0001
        data = [isAbove, isBelow, n, m, l]
        val = start(100000, 15, file, False, False, indicators, data)
        print("thread: " + str(i) + " starting number: " + str(x) + " n,m,l: " + str(data[2]) + " " + str(data[3])+ " " + str(data[4]) + " balance: " + str(val.balance))
        if val.balance > value.balance:
            value = val
    listToAdd[i] = value


if __name__ == "__main__":
    if sys.argv[1] == "True":
        indicators = {"EMA": [EMA,"EUR/USD", 4]}
        isAbove = []
        isBelow = []
        data = [isAbove, isBelow, 1 * .0001, 20, 7 * .0001]
        start(100000, 15, file,True, True, indicators, data)
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

    print("PRINTING ALL ITEMS IN BEST")
    for item in bestMarkets:
        print(item)
    #finding the market that gave the best balance
    best = bestMarkets[0]
    for x in range(numOfThreads):
        if bestMarkets[x].balance > best.balance:
            best = bestMarkets[x]

    print("balance: ")
    print(best.balance)
    print("data: ")
    print(best.data)