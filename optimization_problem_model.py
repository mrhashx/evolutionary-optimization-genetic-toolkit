import numpy as np
class model:
    def __init__(self):
        self.value = np.random.randint(10,90,size=(2,2)).reshape(-1,1)
        self.wieght = np.random.randint(100,900,size=(2,2)).reshape(-1,1)
        self.size, self.total_wieght = len(self.value), 10000
    def fitness_function(self,solution):
        alpha= 100
        violation = max(np.sum(self.wieght*solution)/self.size-1,0)
        f = np.sum(self.value * (1-solution))+(alpha*violation)
        return f 
