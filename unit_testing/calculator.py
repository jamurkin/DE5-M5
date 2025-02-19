class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def do_sum(self):
        return self.a + self.b
    
    def do_product(self):
        return self.a * self.b
    
    def do_subtract(self):
        return self.a - self.b
    
    def do_divide(self):
        return self.a / self.b
