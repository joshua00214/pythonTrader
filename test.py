from indicators.SMA import SMA
'''
import plotly
import plotly.graph_objs as go
'''
import time
import random
from threading import Thread
import _thread
from multiprocessing import Process, Queue, Manager
import main
'''
trace0 = go.Scatter(x=[1,5,1], y=[1, 5, 2], mode = "lines")
trace1 = go.Scatter(x=["21", "5"], y=[2,-5])
plotly.offline.plot([trace0, trace1] , auto_open=True)

abc = [1,2,3,4,5,6,7,8,9,10,11,12]
print(abc[0:10])
'''
'''
buy = [][]
buy[0].append(1)
buy[0][0].append(1)
print(buy)
'''

'''
def createInd(func, *args):
    print(func(*args).length)

f = open("test.txt")
while(True):
    txt = f.readline()
    if txt == None:
        print("none")
        break
    if txt == "":
        print("nothing")
        break
    print(txt)
    '''
'''
myList = [1,2,3,4]
for x in range(len(myList)):
    print(myList[x])
'''
'''
class Solution:
    def threeSum(self, nums):
        returnList = []
        #gathering all sums that equal zero
        #nums.sort()
        #nums = trueNums
        for x in range(len(nums)):
            for y in range(len(nums)):
                if x == y:
                    continue
                for z in range(len(nums)):
                    if y == z or x == z:
                        continue
                    if nums[x] + nums[y] == (-1) * nums[z]:
                        returnList.append([nums[x], nums[y], nums[z]])
                        
        #sorting the inner lists to find duplicates
        for item in returnList:
            item.sort()
         #making sure there are no duplicates
        copy=[]


        for item in returnList:
          
            addToCopy = True
            for copies in copy:
                if item[0] == copies[0] and item[1] == copies[1] and item[2] == copies[2]:
                    
                    addToCopy = False
            if addToCopy:
                
                copy.append(item)
        return copy


testThis = [-13,10,11,-3,8,11,-4,8,12,-13,5,-6,-4,-2,12,11,7,-7,-3,10,12,13,-3,-2,6,-1,14,7,-13,8,14,-10,-4,10,-6,11,-2,-3,4,-13,0,-14,-3,3,-9,-6,-9,13,-6,3,1,-9,-6,13,-4,-15,-11,-12,7,-9,3,-2,-12,6,-15,-10,2,-2,-6,13,1,9,14,5,-11,-10,14,-5,11,-6,6,-3,-8,-15,-13,-4,7,13,-1,-9,11,-13,-4,-15,9,-4,12,-4,1,-9,-5,9,8,-14,-1,4,14]
s = Solution()
newVal = s.threeSum(testThis)
print(newVal)

'''
'''
dict = {"EUR/USD": 21}

dict["EUR/USD"] -= 22
print(dict["EUR/USD"])
'''
'''
y = 2
def printer(a, q):
    y = 0
    while y < 3:
        x = random.randint(1, 100000)
        time.sleep(.1)
        print(a)
        y+= 1
    print(q)
    time.sleep(.5)
    print(str(a) + " is about to append")
    q.append(a)
    print(q)


print("starting")
#Thread(target = printer, args = (1,)).start()

#Thread(target = printer, args = (2,)).start()
if __name__ == "__main__":
    myThreads = []
    manager = Manager()
    ls = manager.list(range(10))
    for x in range(3):
        
        b =  Process(target = printer, args = (x,ls))
        b.start()
        myThreads.append(b)

    for thread in myThreads:
        thread.join()

    print("the very end")
    
    print(ls)
    '''


#TODO loop through and create all indicators with an index instead, by using a dictionarry of lists
'''
{
    smallSMA : [SMA, *args]
    name : [indicator to use (just send the class), variable length of args/]
}

'''
def start(balance, timeLength, file,isPlot, isPrint, dictOfIndicators):
    market = main.Market(balance)

    
    #market.addIndicator("smallSMA", SMA, "EUR/USD", small)
    #market.addIndicator("largeSMA", SMA, "EUR/USD", large)
    for indic in dictOfIndicators.keys():
        #each value is an array with 0th index the function and the rest as args
       # print(many(*dictOfIndicators[indic][1:]))
        market.addIndicator(indic, dictOfIndicators[indic][0], *dictOfIndicators[indic][1:] )
    


    market.isPlot = isPlot
    market.isPrint = isPrint

    
    return main.openFile(market,timeLength, file) #this eventually returns a market object up the chain
    #creating my indicators
def many(*args):
    print(*args)

indicators = {    "smallSMA" : [SMA, "EUR/USD", 100],    "largeSMA" : [SMA, "EUR/USD", 150]}

start(100000, 60, "EURUSD2018.csv", False, True, indicators)

