from .Indicators import Indicator
from indicators.EMA import EMA
#MACD always has the 26 EMA and the 12 EMA
#NOTE  --- ALWAYS PLOT A SIGNAL LINE ITS A EMA WITH LENGTH 9
#Buy signal when macd > signal line
#appears to give a very long peek into the future
class MACD(Indicator):
    def __init__(self, market, currency):
        
        self.shortEMA = EMA(market, currency, 12)
        self.longEMA = EMA(market, currency, 26)
        self.signalLine = EMA(market, currency, 9)
        self.MACD = 0
        self.market = market
        super().__init__(market, currency)
        self.isPrint = True
        
    def update(self, price):
        self.shortEMA.update(price)
        self.longEMA.update(price)
        #this needs to come first to fill the market.indicatorValues["signalLine"] with a bunch of Nones up first to match with the date
        if "signalLine" in self.market.indicatorValues.keys():
            self.market.indicatorValues["signalLine"].append(self.signalLine.getValue())
        else:
            self.market.indicatorValues["signalLine"] = [self.signalLine.getValue()]
        if self.longEMA.getValue() is None:
            self.MACD = 0
            return 
        
        #MACD IS SHORT - LONG
        self.MACD =self.shortEMA.getValue() - self.longEMA.getValue() 
        self.signalLine.update(self.MACD)
        #add this signal line
        

    def getValue(self):
        #i know i know dont yell at me
        if self.MACD != 0:
            return self.MACD
        
