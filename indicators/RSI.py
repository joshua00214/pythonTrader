from .Indicators import Indicator
#http://cns.bu.edu/~gsc/CN710/fincast/Technical%20_indicators/Relative%20Strength%20Index%20(RSI).htm
#part of the calculation in this website must be down, they are not calculatoing avg
#correct
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
        self.avgGain = []
        self.avgLoss = []
        self.RSI = -1
        if length % 2 != 0:
            raise Exception("length of RSI indicator must be even to find an average percent gain/loss")
        super().__init__(market, currency)
        
    def update(self, price):
        self.forexPrices.insert(0, price)
        #RSI = 100 - (100 / (1 + RS))
        #avg_gain = total gain / n
        #avg_loss = total loss / n
        #first RS = (avg_gain/avgloss)
        #smoothed RS = ((previous avg gain * 13)) + currentGain) / 14   all over       ((prevous avg loss * 13 + current loss)/14)
        #n = number of rsi periods
        if len(self.forexPrices)  < self.length + 1:
            return
        if len(self.forexPrices)  > self.length + 1:
            self.forexPrices.pop()
        #testing in test.py, this will give the total gain and total loss accuratly
        totalGain = 0
        totalLoss = 0
        increases = []
        losses = []
        for i in range(self.length + 1):
            #allows me to loop back -> front
            if i == self.length:
                break
            if self.forexPrices[i] < self.forexPrices[i + 1]:
                losses.insert(0,self.forexPrices[i + 1] - self.forexPrices[i])
                totalLoss += self.forexPrices[i + 1] - self.forexPrices[i]
            if self.forexPrices[i] > self.forexPrices[i + 1]:
                increases.insert(0, self.forexPrices[i] - self.forexPrices[i+1])
                totalGain += self.forexPrices[i] - self.forexPrices[i + 1]
        self.avgGain.insert(0, totalGain/self.length)
        self.avgLoss.insert(0, totalLoss/self.length)
        currentGain = 0
        currentLoss = 0
        #index 0 is the most recent price, index 1 was previous price
        if self.forexPrices[0] > self.forexPrices[1]:
            currentGain += self.forexPrices[0] - self.forexPrices[1]
        if self.forexPrices[1] > self.forexPrices[0]:
            currentLoss += self.forexPrices[1] - self.forexPrices[0]
        if len(self.avgGain) <2 :
           self.RS = self.avgGain[0]/self.avgLoss[0]
        else:
            self.RS = (((self.avgGain[1] * 13) + currentGain) / 14)  /   (((self.avgLoss[1] * 13) + currentLoss)/14)
        self.RSI = 100 - (100 / (1 + self.RS))
#JUST FIGURED OUT I NEED CURRENT GAIN

        
        

    def getValue(self):
        if self.RSI == -1:
            return 0
        else:
            return self.RSI




            
        
