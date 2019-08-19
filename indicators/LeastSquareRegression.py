from .Indicators import Indicator
# this will take the past 5 values and create a lease square regression line on the graph, the x axis is the time() and the y axis is the 

class LSR(Indicator):
    def __init__(self, market, currency, length):
        self.time = 1
        self.prices = []
        self.length = length
        self.times = []
        self.values = []
        super().__init__(market, currency)
        self.isPrint = True
        self.slopes = []
    def update(self, value):
        #convert number to a number starting at the hundreths place and going out 4 digits
        svalue = str(value)
        svalue = svalue[3:]

        if len(svalue) == 2:
            svalue = svalue + "0"
            svalue = svalue + "0"
        if len(svalue) == 3:
            svalue = svalue +"0"

        nvalue = float(svalue)
        
        self.values.insert(0, nvalue)
        if len(self.values) > 5:
            self.values.pop()
        
        self.times.insert(0, self.time)
        if len(self.times) > 5:
            self.times.pop()
        self.time += 1
        #creating LSF
        if len(self.times) != 5 or len(self.values) != 5:
            return
        
        self.times.reverse()
        array = np.array([[1,1,1,1,1], self.times]) #this automatically stores it as transposed
        self.times.reverse()
        
        #array.transpose()
        #print(array.T)

        self.values.reverse()
        y = np.array(self.values)
        self.values.reverse()
        print(y)

    

        step1 = array.dot(array.T)
        print("STEP 1")
        print(step1)
        step2 = np.linalg.inv(step1)
        print("STEP 2")
        print(step2)
        step3 = np.dot(step2, array)
        print("STEP 3")
        print(step3)
        step4 = np.dot(step3,y )
        print("STEP 4")
        print(step4)
        
        self.slopes.insert(0, step4[1])




        
#returning angle measurement of slope first
    def getValue(self):
        if len(self.slopes) > 1:
            return self.slopes

    