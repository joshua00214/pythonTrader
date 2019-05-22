from .Indicators import Indicator
from indicators.EMA import EMA
#MACD always has the 26 EMA and the 12 EMA
#NOTE  --- ALWAYS PLOT A SIGNAL LINE ITS A EMA WITH LENGTH 9
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
        if self.longEMA.getValue() is None:
            self.MACD = 0
            return 
        self.MACD = self.longEMA.getValue() - self.shortEMA.getValue()
        self.signalLine.update(self.MACD)
        #add this signal line
        if "signalLine" in self.market.indicatorValues.keys():
            self.market.indicatorValues["signalLine"].append(self.signalLine.getValue())
        else:
            self.market.indicatorValues["signalLine"] = [self.signalLine.getValue()]

    def getValue(self):
        if self.MACD != 0:
            return self.MACD