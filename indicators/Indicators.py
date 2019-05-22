class Indicator:
    def __init__(self, currency):
        self.currency = currency
        #default to printwith is false
        self.isPrint = False

    def update(self, value):
        assert False #forces this to be abstract
    def getValue(self):
        assert False #forces this to be abstract
