from .Indicators import Indicator
#note- length is proportinal to the time interval being used
#standard to use 20 and 50 length
#appear to be such a late indicator
class SMA(Indicator):
    def __init__(self, market, currency, length):
        self.values = []
        self.averages = []
        self.length = length
       
        super().__init__(market, currency)
        self.isPrint = True
    def update(self, value):
        #adding next value to list of values
        self.values.insert(0, value)
        #keeping its length to correct amount
        if len(self.values) > self.length:
            self.values.pop()

        #calculating average
        sum = 0
        for value in self.values:
            sum += value
        average = float(float(sum)/self.length)

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