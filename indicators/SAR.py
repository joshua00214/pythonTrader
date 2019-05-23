from .Indicators import Indicator

class SAR(Indicator):
    def __init__(self, market, currency):
        super().__init__(market, currency)
        self.isPrint = True
        self.SARS = []
        #need to store past value to determine if its an uptrend or downtrend
        self.values = []
        self.alpha = .02
        self.market = market
        self.uptrend = None
        self.high = None
        self.low = None
    def update(self, value):
        #calculate EP
        
        if self.high != None and self.low != None: #only use previous value if it exists, else return
             #previous high/low
            plow = self.low
            ptrend = self.uptrend
        else:
            self.high = self.market.high
            self.low = self.market.low
            return

        high = self.market.high
        self.low = self.market.low
        
        #calculating trend
        if self.low > plow:
            self.uptrend = True
        if self.low < plow:
            self.uptrend = False
        #if trend has changed then modify alpha and EP
        if self.uptrend != ptrend:
            
            self.alpha = .02
            if self.uptrend == True:
                self.EP = high
            elif self.uptrend == False:
                self.EP = self.low
        #           see if EP/alpha needs changed
        #I know how if statement == true looks, but I think its more readable
        if self.uptrend == True: 
            if high > self.EP:
                self.EP = high
                if self.alpha < .2:
                    self.alpha += .02
        if self.uptrend == False:
            if self.low < self.EP:
                self.EP = self.low
                if self.alpha < .2:
                    self.alpha += .02

            
        #the formula for SAR is,
        # SAR(n) = SAR(n-1) + (alpha)*(EP - SAR(n-1))
        #SAR(n) is todays SAR
        #SAR(n-1) is yesterdays
        #alpha is .02 and increases by .02 each time EP is changed to a max of .2
        #EP is the high/low of the period depending on uptrend/downtrend
        #UPTREND : current low is > previous low
        #DOWNTREND : current low is < previous low
        if len(self.SARS) > 0:
            
            SAR = self.SARS[0] + ((self.alpha)*(pastEP - self.SARS[0]))
        else:
            SAR = value
        self.SARS.insert(0, SAR)
    def getValue(self):
        if len(self.SARS) > 0:
            return self.SARS[0]