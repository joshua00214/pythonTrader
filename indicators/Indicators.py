class Indicator:
    def __init__(self, currency):
        self.currency = currency

    def update(self, value):
        assert False #forces this to be abstract
    def getValue(self):
        assert False #forces this to be abstract
