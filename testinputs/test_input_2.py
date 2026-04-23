class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, x):
        self.result += x
        return self.result
    
    def multiply(self, x):
        self.result *= x
        return self.result
    
    def reset(self):
        self.result = 0

calc = Calculator()
print(calc.add(10))
print(calc.multiply(2))
