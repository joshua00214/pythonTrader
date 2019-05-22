from .Indicators import Indicator

#EMA = price(t) * k + EMA(y)*(1-k)
'''
t = today
y = yesterday
N = number of days in the ema (maybe also use number of hours if this doesn't work)
k = 2/(N+1)
y = yesterday

'''
#note- length is proportinal to the time interval being used
class EMA(Indicator):
    def __init__(self,market,  currency, length):
        self.values = []
        self.averages = []
        self.length = length
        self.k = 2 / (length + 1)
        
        super().__init__(market, currency)
        self.isPrint = True
    def update(self, value):
        #adding next value to list of values
        


        self.values.insert(0, value)
        #keeping its length to correct amount
        if len(self.values) > self.length:
            self.values.pop()

        #calculating average
        #since EMA depends on preious ema, adding in a case for the begining of execution
        if len(self.averages) < 2:
            self.averages.insert(0, value)
            return
        #the formula for ema
        average = (value * self.k) + (self.averages[1] *(1 - self.k))
        #inserting the average
        self.averages.insert(0, average)
        if len(self.averages) > self.length:
            self.averages.pop()

    def getAverages(self):
        if len(self.averages) == self.length:
            return self.averages
        else:
            return []
    def getValue(self):
        if len(self.averages) == self.length:
            return self.averages[0]
        

    def getLength(self):
        return self.length