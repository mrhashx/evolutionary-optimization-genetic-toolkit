import numpy as np
import pandas as pd
value = np.array([10,25,18,60,48,55,34,74,31])
wieght = np.array([200,140,299,600,111,510,800,472,288])
W= 2500
def fitness_function(solution):
    alpha= 0.4
    violation = max(np.sum(wieght*solution)-W,0)
    fitness = np.sum(value * solution) - (alpha*violation)
    return fitness
class Individual:
    def __init__(self):
        self.ind = np.random.randint(0,2,(len(value),))
        self.fitness = int(fitness_function(self.ind))
    def __lt__(self,I):
        return self.fitness < I.fitness
    def Set_Posision(self,A):
        self.ind = A
    def Set_fitness(self):
        self.fitness = int(fitness_function(self.ind))
