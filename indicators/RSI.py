from .Indicators import Indicator
#Standard to use 14
#when it is being overbought, itll go down
#when it is being oversold, itll go up
'''
a. BUY when the RSI is about to approach upwards into the overbought zone (at ~70); or

b. BUY when the RSI rises upwards and leaves the oversold zone (at ~30); or

c. SELL when the RSI declines downwards and leaves the overbought zone (at ~70); or

d. SELL when the RSI is about to approach downwards into the oversold zone (at ~30)
Avoid executing trades when RSI is between 45-55 or to be more conservative between 40-60.
'''
class RSI(Indicator):
    def __init__(self, market, currency, length):
        self.length = length
        self.forexPrices = []
        self.avgPercentGains = []
        self.avgPercentLosses = []
        self.RSI = -1
        if length % 2 != 0:
            raise Exception("length of RSI indicator must be even to find an average percent gain/loss")
        super().__init__(market, currency)
        
    def update(self, price):
        self.forexPrices.insert(0, price)
        #need + 1 on the length because the length of RSI refers to how many average gain
        # / loss it can get
        if len(self.forexPrices) > self.length + 1:
            self.forexPrices.pop()
        if len(self.forexPrices) != self.length + 1:
            #need a full list of prices to start calculating RSI
            return
        #calculater average % gain and average % loss
        percentGains = []
        percentLosses = []
        for item in range(len(self.forexPrices)):
            #can't compare first item to one before
            if item == 0:
                continue
            #percent change = new-old/old
            percentChange = (self.forexPrices[item] - self.forexPrices[item - 1]) / self.forexPrices[item-1]
            if percentChange > 0:
                percentGains.insert(0, percentChange)
            elif percentChange < 0:
                percentLosses.insert(0, (-1) * percentChange)
        avgPercentGain = sum(percentGains) / self.length
        avgPercentLost = sum(percentLosses) / self.length

        self.avgPercentGains.insert(0, avgPercentGain)
        self.avgPercentLosses.insert(0, avgPercentLost)

        #calculating RSI required the revious average so it needs a length of two
        if len(self.avgPercentGains) > 2:
            self.avgPercentGains.pop()
        if len(self.avgPercentLosses) > 2:
            self.avgPercentLosses.pop()
        
        if len(self.avgPercentGains) != 2 and len(self.avgPercentLosses) != 2:
            #exit if length != 2
            return

        #now calculate RSI

        #step 2, RSI = 100  -   (100    /   (1  +   (previous avg * (l - 1) + current)))
        
        self.RSI = 100   -   (100    /   (1  +   (   ((self.avgPercentGains[1] * (self.length - 1)) + self.avgPercentGains[0])  /   (((self.avgPercentLosses[1] * (self.length - 1)) + self.avgPercentLosses[0]))  )))

    def getValue(self):
        if self.RSI == -1:
            return 0
        else:
            return self.RSI




            
        
