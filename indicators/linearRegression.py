from .Indicators import Indicator
import statistics
#note- length is proportinal to the time interval being used

'''
there is no need to make a whole linearRegression file when I just need the slope to arctan it. 
'''
class linearRegression(Indicator):
    def __init__(self, currency, length):
        self.values = []
        self.length = length
        self.x = [i for i in range(length)]
        self.returnValue = 0;
        super().__init__(currency)
    
    def update(self, value):
        #adding value to list of values
        self.values.insert(0, value)
        if len(self.values > self.length):
            self.values.pop()
        #get the next value
        if len(self.values) == self.length:
            value = self.m()*1 + self.b()
            self.returnValue = value
        


    def getValue(self):
        return self.returnValue
    def m(self):
        #formula for m
        x = self.x
        y = self.values
        z = []
        for item in range(len(x)):
            z.append(x[item] * y[item])
        xSquared = []
        for item in x:
            xSquared.append(item*item)
        return (    (statistics.mean(x) * statistics.mean(y)) - statistics.mean(z)     )    /   (   (statistics.mean(x) * statistics.mean(x)) - statistics.mean(xSquared)  )

    def b(self):
        #formula for b
        m = self.m()
        y = self.values
        x = self.x
        return ( statistics.mean(y) - (m * statistics.mean(x))   )