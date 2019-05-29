from .Indicators import Indicator
#moddled after this video
#https://www.youtube.com/watch?v=MuEpGBAH7pw
class SAR(Indicator):
    def __init__(self, market, currency):
        super().__init__(market, currency)
        self.isPrint = True
        self.EP = []
        self.Acc = .02
        #(PSAR - EP) * Acc
        self.values = []
        self.PSAR = 0
        #uptrend is True/downtrend is false
        self.trend = False
        self.ptrend = False
        self.market = market
        #inital PSAR
        self.iPSAR = 0
        self.high = []
        self.low = []
    def update(self, value):
        #calculate EP
        #changes direction when the point that wouldve been psar is within the current low/hide
        self.values.insert(0, value)
        self.high.insert(0, self.market.high)
        self.low.insert(0, self.market.low)

        #getting inital values before running
        if len(self.high) < 3:    #first run through to update values
            self.EP.insert(0, self.market.low)
            #setting init PSAR = high, doesn't really matter it will correct itself
            self.PSAR = self.market.high
            return
        

        






        #getting iPSAR
        if self.trend == False:
            #iPSAR = PSAR - PSARMATH
            #in a downtrend, can not be lower then the 2 preceeding high points
            self.iPSAR = max(self.PSAR - self.PSARMATH(), self.high[1], self.high[2])
        if self.trend == True:
            #iPSAR = PSAR - PSARMATH
            #in an uptrend, it can now be greater then the previous 2 lows
            self.iPSAR = min(self.PSAR - self.PSARMATH(), self.low[1], self.low[2])


        #getting PSAR
        #4 cases
        if self.trend == False and self.high[0] < self.iPSAR:
            #PSAR = iPSAR
            self.PSAR = self.iPSAR
        if self.trend == True and self.low[0] > self.iPSAR:
            self.PSAR = self.iPSAR
        if self.trend == False and self.high[0] >= self.iPSAR:
            #take extreme point
            self.PSAR = self.EP[0]
        if self.trend == True and self.low[0] <= self.iPSAR:
            self.PSAR = self.EP[0]

        #updating trend
        if self.PSAR > value:
            self.ptrend = self.trend
            self.trend = False
        else:
            self.ptrend = self.trend
            self.trend = True
        
        #updating EP
        if self.trend == False:
            self.EP.insert(0, min(self.EP[0], self.low[0]))
        if self.trend == True:
            self.EP.insert(0, max(self.EP[0], self.high[0]))

        #updating Acc
        if self.trend == self.ptrend and self.EP[0] != self.EP[1] and self.Acc < .2:
            self.Acc += .02
        
        if self.trend != self.ptrend:
            self.Acc = .02
        

        
    def PSARMATH(self):
        return (self.PSAR - self.EP[0]) * self.Acc
    def getValue(self):
        return self.PSAR