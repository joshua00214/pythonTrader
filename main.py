#used for backtesting
from indicators.SMA import SMA
from indicators.EMA import EMA
import plotly
import plotly.graph_objs as go
import random
import math
from threading import Thread
from multiprocessing import Process, Manager
import sys
#will contain the ability to buy/sell, balance
class Market:
    #sets balance, and all holdings
    #balance is always realized, so may be inaccurate when shorting
    def __init__(self, balance = 100000, spread = 0.0005): #5 pip spread
        self.balance = balance
        self.holdings = {"EUR/USD": 0}
        self.buyPrices = {"EUR/USD": 0}
        self.sellPrices = {"EUR/USD": 0}
        self.spread = spread
        self.unrealizedBalance = balance
        #dictionarry of indicators with their names mapped to indicator objects
        self.indicators = {}
        self.date = None
        self.minute = None

        #THESE VARS ARE FOR PLOTTING
        #will be a dictionary of lists containing values for each currency pair.
        self.listSellPrices = {}
        self.listBuyPrices = {}
        #dict of indicator values as a list for each indicator name
        self.indicatorValues = {}
        self.listBalace = []
        self.times = []
        #2d array of buys/sells for plotting
        self.priceBuys = []
        self.timeBuys = [] #time is always x-axis
        self.priceSells = []
        self.timeSells = []
        self.listUnrealizedBalance = []

        #list of data to allow for a bruteforce algorithm is repeatidly call this
        self.data = [] #is declared here but initalized in start
    #buys the amount
    def buy(self, currency, amount):
        if self.balance > self.buyPrices[currency] * amount:
            self.balance -= self.buyPrices[currency] * amount
            self.holdings[currency] += amount
            self.updateUnrealizedBalance()
            self.priceBuys.append(self.buyPrices[currency])
            self.timeBuys.append(self.minute + " " + self.date)
            self.updateUnrealizedBalance()
        else:
            raise Exception("Not enough money to buy " + currency)
        
    #sells that amount
    def sell(self, currency, amount):
        
        if self.holdings[currency] >= amount:
            self.holdings[currency] -= amount
            self.balance += amount * self.sellPrices[currency]
        else:
            
            self.holdings[currency] -= amount
            self.balance += amount * self.sellPrices[currency] #comment me out to stop shorts
        self.updateUnrealizedBalance()

        self.priceSells.append(self.sellPrices[currency])
        self.timeSells.append(self.minute + " " + self.date)
        self.updateUnrealizedBalance()
        

    #updates buy/sell prices and the indicators and the unrealized profit.
    def updatePrice(self, sellPrice, date, minute, currency = "EUR/USD"):
        self.sellPrices[currency] = sellPrice
        self.buyPrices[currency] = sellPrice + self.spread
        
        for indicator in list(self.indicators.values()):
            
            if indicator.currency == currency:
                indicator.update(sellPrice)
            
        

        self.date = date
        self.minute = minute

        #TODO put these method calls in their own method, shouldn't be ran for every currency
        self.updateUnrealizedBalance()

        #remember not to plot for every currency we add
        self.plot()
        


    def updateUnrealizedBalance(self):
        for currency in list(self.holdings.keys()):

            if self.holdings[currency] < 0:
                self.unrealizedBalance = float(self.balance) - float(float(self.holdings[currency]) * float(-1) * float(self.buyPrices[currency]))
            if self.holdings[currency] > 0:
                self.unrealizedBalance = self.balance + (self.holdings[currency] * self.sellPrices[currency])

            if self.holdings[currency] == 0:
                self.unrealizedBalance = self.balance

    #indic must be a class that extends Indicators.Indicator 
    def addIndicator(self, name, indic, *args):
        self.indicators[name] = indic(*args)
    

    def getIndicator(self, name):
        return self.indicators[name]



    def getAllIndicators(self):
        return self.indicators


    #storing all data to plot at the end
    def plot(self):
        #storing currencies values
        for currency in self.sellPrices:
            if currency in self.listSellPrices.keys():
                self.listSellPrices[currency].append(self.sellPrices[currency])
            else:
                self.listSellPrices[currency] = [self.sellPrices[currency]]

        for currency in self.buyPrices:
            if currency in self.listBuyPrices.keys():
                self.listBuyPrices[currency].append(self.buyPrices[currency])
            else:
                self.listBuyPrices[currency] = [self.buyPrices[currency]]
        #stories indicators values
        for indicator in self.indicators:
            if indicator in self.indicatorValues.keys():
                self.indicatorValues[indicator].append(self.indicators[indicator].getValue())
            else:
                self.indicatorValues[indicator] = [self.indicators[indicator].getValue()]

        #the x-axis for all graphs will be the times, the hour when time != 0, and the date when time = 0
        self.times.append(self.minute + " " + self.date)

        self.listBalace.append(self.balance)
        self.listUnrealizedBalance.append(self.unrealizedBalance)


#will open to file and call the run method for every new price, and update the price in the market
#TODO allow it to work across multiple currencies
#should not need to be edited
def openFile(market, timeLength, file):
    #opening all files
    data = open(("data\\" + file))
    print("opening file")
    #make data a dict of lists, [file object, next line to be read] then go thru loop for each one? filenames will
    #need to be the currency of the market for easy readability

    x = 0
    line = data.readline()
    #TODO add avaliability for other currencies
   
    while(line != ""):
        #adding each new price to market object
        
        
        if(timeLength - x == 0):
            
            listFromLine = line.split(",")
            
            sell = float(listFromLine[5]) #grabbing the closing price in the file
            
            date = listFromLine[0]
            minute = listFromLine[1]
            market.updatePrice(sell, date, minute)
                
            
            #running the run method
            run(market)
            x = 0
        x += 1
        line = data.readline()
        #assert x < 100
        
    
    return end(market)
    

#starts the execution of the code
#timeLength is in minutes, because file gives value every 1 minute

#TODO loop through and create all indicators with an index instead, by using a dictionarry of lists
'''
{
    smallSMA : [SMA, *args]
    name : [indicator to use (just send the class), variable length of args/]
}
'''
#TODO but start, openFile, and end inside of market with a link to the run method
#TODO add list of data that can be sent to market
#should not need edited
def start(balance, timeLength, file,isPlot, isPrint, dictOfIndicators, data = []):
    market = Market(balance)

    market.data = data
    #market.addIndicator("smallSMA", SMA, "EUR/USD", small)
    #market.addIndicator("largeSMA", SMA, "EUR/USD", large)
    for indic in dictOfIndicators.keys():
        #each value is an array with 0th index the function and the rest as args
       # print(many(*dictOfIndicators[indic][1:]))
        market.addIndicator(str(indic), dictOfIndicators[indic][0], *dictOfIndicators[indic][1:] )
        
        '''
    print("PRINTING ALL INDICATORS")
    print(market.getAllIndicators())
    exit()
'''
    market.isPlot = isPlot
    market.isPrint = isPrint

    
    return openFile(market,timeLength, file) #this eventually returns a market object up the chain
    #creating my indicators
    


#runs each iteration
x = 0 #for debuggins
def run(market):
    global x
    x += 1
    #based off the EMA as S&R file
    ema = market.getAllIndicators()["EMA"]
    #will state if its above/below for 3(m) length at an epsilon of 1.5(n) pips
    m = 3 #the duration
    n = .00015 #this is the epsilon of the pips
    l = .0001 #this is where I cut my losses when its going the wrong way.
    isAbove = market.data[0]
    isBelow = market.data[1]
    if len(ema.getAverages()) == ema.getLength():

        #                       storing based on past m duration
        #need this behavior because isAbove and isBelow could both be false - it could be closer
        #than the epsilon
        isAboveChanged = False
        if ema.getValue() > market.sellPrices["EUR/USD"] + n:
            isAbove.insert(0, True)
            isAboveChanged = True
        isBelowChanged = False
        if ema.getValue() < market.sellPrices["EUR/USD"] - n:
            isBelow.insert(0, True)
            isBelowChanged = True
        #if isAbove or isBelow havent changed then insert a False
        if isBelowChanged == False: #I think this is more readable
            isBelow.insert(0, False)
        if isAboveChanged == False:
            isAbove.insert(0, False)
        #if isAbove or isBelow are longer then length then pop a value
        if len(isAbove) > m:
            isAbove.pop()
        if len(isBelow) > m:
            isBelow.pop()
        #                   check to see if I need to stop any positions
        if market.holdings["EUR/USD"] > 0 and ema.getValue() > market.sellPrices["EUR/USD"] + l:
            market.sell("EUR/USD", market.holdings["EUR/USD"]) #closing a long position
        
        if market.holdings["EUR/USD"] < 0 and ema.getValue() < market.sellPrices["EUR/USD"] - l:
            market.buy("EUR/USD",(-1) * market.holdings["EUR/USD"]) #closing a short position
        #                   buy/sell if the EMA has been above/below long enough
        
        if len(isBelow) == m and len(isAbove) == m:
            #if all the isBelows are True, then buy
            isBuy = True
            for below in isBelow:
                if below == False:
                    isBuy = False
                    break
            if isBuy and market.holdings["EUR/USD"] <=0:
                market.buy("EUR/USD", market.balance * .1)#going long
            #if all the isAboves are True, then sell
            isSell = True
            for above in isAbove:
                if above == False:
                    isSell = False
                    break
            if isSell and market.holdings["EUR/USD"] >= 0:
                market.sell("EUR/USD", market.balance * .1)#going short





    
   
    


#should not need edited
def end(market):
    #clearing all holdings at the end
    if market.holdings["EUR/USD"] < 0:
        
        market.buy("EUR/USD",((-1) * market.holdings["EUR/USD"]))
       
    if market.holdings["EUR/USD"] > 0:
        market.sell("EUR/USD",market.holdings["EUR/USD"])
    market.updateUnrealizedBalance()
    #updatePrice is here to plot the new values
    market.updatePrice(market.sellPrices["EUR/USD"], market.date, market.minute)
    

    #TODO improve plotting behavior for other currency pairs
    #plotting price/indicators
    
    if(market.isPlot):
        traces = []
        trace0 = go.Scatter(x =market.times ,y=market.listSellPrices["EUR/USD"] , name = "sellPrice", mode = "lines+markers")
        trace3 = go.Scatter(x =market.times ,y=market.listBuyPrices["EUR/USD"] , name = "buyPrice", mode = "lines+markers")
        
        
        Buys = go.Scatter(x = market.timeBuys, y=market.priceBuys, mode = "lines+markers", name = "Buys")
        Sells = go.Scatter(x = market.timeSells, y=market.priceSells, mode = "lines+markers", name = "Sells")


        traces.append(trace0)
        
        
        traces.append(trace3)
        traces.append(Buys)
        traces.append(Sells)
        for indica in market.getAllIndicators():
            traces.append(go.Scatter(x = market.times, y= market.indicatorValues[indica], mode = "lines+markers", name = str(indica)))
        
        print(plotly.offline.plot(traces, auto_open = True, filename = "EURUSD.html"))


        
        balance_trade = go.Scatter(x = market.times, y=market.listBalace, mode = "lines+markers", name = "Balace")
        ubalance_trade = go.Scatter(x = market.times, y=market.listUnrealizedBalance, mode = "lines+markers", name = "UnrealizedBalance")
        
  
        print(plotly.offline.plot([balance_trade, ubalance_trade], auto_open = True, filename = "balance.html"))

   
    if market.isPrint:
       
        print("final balance: " + str(market.balance))
        print("\n \n \n")
        print("buys and sell times: " + str(len(market.timeBuys)) + " " + str(len(market.timeSells)))
        print(market.timeBuys)
        print(market.priceBuys)
        print(market.timeSells)
        print(market.priceSells)
    return market
#x = market.listSellPrices["EUR/USD"]
#y= market.times



#start(100000, 60, 356, 390, "EURUSD2018.csv")
file = "EURUSD2018.csv"
#start(100000, 60, 343, 432, file)

#start(100000, 60)

#this allows a brute force of the best variables by using multi-threading
#listToAdd is gonna be a list of market objects

